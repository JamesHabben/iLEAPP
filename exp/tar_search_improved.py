#!/usr/bin/env python3
"""
Improved search demo (bucketed candidates + SQLite family fast-path).

- Reads patterns from a sibling file_path.txt (one per line), ordered de-dup.
- Builds per-bucket indexes from a single pass over the TAR:
    * sandbox:      */Containers/Data/Application/<GUID>/*
    * appgroup:     */Containers/Shared/AppGroup/<GROUP>/*
    * photos:       */PhotoData/*  (and common Photos.sqlite locations)
    * mobile_lib:   */mobile/Library/*
    * biome:        */mobile/Library/Biome/*
    * global:       everything
- For each pattern:
    * Try exact-match fast-path (no wildcards).
    * Route to a bucket based on the pattern text (heuristics).
    * If basename fixed → start from basename bucket.
    * If extension obvious → start from ext bucket(s).
    * If dir part has no wildcards → prefilter by directory prefix.
    * If basename endswith .db* or .sqlite* → expand to .db/.db-wal/.db-shm
      and attempt quick hits before falling back to glob.
    * Run fnmatch-based regex only on the reduced candidate list.
- Extracts matching members to exp/_out_improved/<timestamp>/ preserving path.
- Writes per-pattern timings to matches.csv

Run:
    python exp/improved_tar_search.py /path/to/image.tar[.gz]
"""

import csv
import fnmatch
import os
import re
import sys
import tarfile
import time
import zipfile
from abc import ABC, abstractmethod
from collections import defaultdict, OrderedDict
from pathlib import Path, PurePosixPath
from typing import Iterable, List, Dict, Tuple, Optional

# -------- utilities --------

WILDCARD_CHARS = set("*?[]")

def has_wildcards(s: str) -> bool:
    return any(c in s for c in WILDCARD_CHARS)

def normcase_posix(s: str) -> str:
    # Use POSIX-style matching (tar member names are posix).
    # Keep case as-is except lowercasing on Windows-like if desired; we’ll just keep as-is.
    # fnmatch's regex is case-sensitive unless os is Windows. We'll enforce case-sensitive.
    return s

def compile_glob(pattern: str) -> re.Pattern:
    # Match the behavior of FileSeekerTar: it matches against "root/" + path
    # We'll compile a regex using fnmatch.translate on normcased pattern.
    pat = normcase_posix(pattern)
    return re.compile(fnmatch.translate(pat))

def ordered_dedupe(seq: Iterable[str]) -> List[str]:
    return list(OrderedDict((x, None) for x in seq).keys())

def read_patterns(pattern_file: Path) -> List[str]:
    lines = []
    with pattern_file.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            lines.append(s)
    return ordered_dedupe(lines)

def safe_join(base: Path, rel: str) -> Path:
    # Ensure we never escape the output root when writing files
    rel_path = PurePosixPath(rel)
    # Prevent absolute paths / parent traversal
    rel_clean = PurePosixPath(*[p for p in rel_path.parts if p not in ("", ".", "..")])
    out = base / Path(rel_clean.as_posix())
    out.parent.mkdir(parents=True, exist_ok=True)
    return out

# --- Archive Abstraction ---

class ArchiveMember:
    """A unified representation of a file within an archive."""
    def __init__(self, name: str, is_file: bool, original_obj):
        self.name = name            # POSIX-style path within the archive
        self.is_file = is_file
        self.original_obj = original_obj # The raw tar/zip object for extraction

class Archive(ABC):
    """An abstract interface for reading members from an archive (TAR, ZIP, etc.)."""
    @abstractmethod
    def get_members(self) -> List[ArchiveMember]:
        """Returns a list of all members in the archive."""
        pass

    @abstractmethod
    def extract_member(self, member: ArchiveMember, out_root: Path):
        """Extracts a single member to a file in the output root."""
        pass

    @abstractmethod
    def close(self):
        """Closes any open file handles."""
        pass

# --- Concrete Implementations ---

class TarArchive(Archive):
    def __init__(self, path: Path):
        self._tar = tarfile.open(path, "r:*")

    def get_members(self) -> List[ArchiveMember]:
        members = []
        for member_info in self._tar.getmembers():
            members.append(
                ArchiveMember(
                    name=member_info.name,
                    is_file=member_info.isfile(),
                    original_obj=member_info
                )
            )
        return members

    def extract_member(self, member: ArchiveMember, out_root: Path):
        target_path = safe_join(out_root, member.name)
        try:
            with self._tar.extractfile(member.original_obj) as fsrc:
                if fsrc is None: return
                with open(target_path, "wb") as fdst:
                    while True:
                        chunk = fsrc.read(1024 * 1024)
                        if not chunk: break
                        fdst.write(chunk)
        except Exception:
            pass # Skip special files that can't be extracted

    def close(self):
        self._tar.close()

class ZipArchive(Archive):
    def __init__(self, path: Path):
        self._zip = zipfile.ZipFile(path, 'r')

    def get_members(self) -> List[ArchiveMember]:
        members = []
        for member_info in self._zip.infolist():
            is_file = not member_info.filename.endswith('/')
            members.append(
                ArchiveMember(
                    name=member_info.filename,
                    is_file=is_file,
                    original_obj=member_info
                )
            )
        return members

    def extract_member(self, member: ArchiveMember, out_root: Path):
        target_path = safe_join(out_root, member.name)
        try:
            with self._zip.open(member.original_obj) as fsrc:
                with open(target_path, "wb") as fdst:
                     while True:
                        chunk = fsrc.read(1024 * 1024)
                        if not chunk: break
                        fdst.write(chunk)
        except Exception:
            pass

    def close(self):
        self._zip.close()

# -------- indexer --------

class ArchiveIndex:
    """
    Build one-pass indexes over archive member names to allow candidate pruning.
    """
    def __init__(self, archive: Archive):
        self.archive = archive
        self.members: List[ArchiveMember] = []
        self.names: List[str] = []
        self.name_set: set[str] = set()

        # global maps
        self.basename_map: Dict[str, List[int]] = defaultdict(list)  # basename -> [idx]
        self.ext_map: Dict[str, List[int]] = defaultdict(list)       # .ext or '' -> [idx]
        self.dir_map: Dict[str, List[int]] = defaultdict(list)       # full dir -> [idx]

        # buckets (store indices)
        self.bucket_indices: Dict[str, List[int]] = {
            "sandbox": [],
            "appgroup": [],
            "photos": [],
            "mobile_lib": [],
            "biome": [],
            "global": [],  # all
        }

        self._build()

    def _build(self):
        for m in self.archive.get_members():
            # Only regular files are extractable (skip dirs/links)
            if not m.is_file:
                continue
            name = m.name  # posix path in tar
            self.members.append(m)
            self.names.append(name)
            self.name_set.add(name)

            idx = len(self.names) - 1

            base = os.path.basename(name)
            
            if base.endswith("-shm"):
                ext = "-shm"
            elif base.endswith("-wal"):
                ext = "-wal"
            else:
                _, ext = os.path.splitext(base)
            d = os.path.dirname(name)

            self.basename_map[base].append(idx)
            self.ext_map[ext].append(idx)
            self.dir_map[d].append(idx)

            # Bucketing heuristics
            path = "/" + name  # leading slash to ease 'in' checks with anchored substrings
            if "/Containers/Data/Application/" in path:
                self.bucket_indices["sandbox"].append(idx)
            if "/Containers/Shared/AppGroup/" in path:
                self.bucket_indices["appgroup"].append(idx)
            if "/PhotoData/" in path or base == "Photos.sqlite" or base.startswith("Photos.sqlite"):
                self.bucket_indices["photos"].append(idx)
            if "/mobile/Library/" in path:
                self.bucket_indices["mobile_lib"].append(idx)
            if "/mobile/Library/Biome/" in path:
                self.bucket_indices["biome"].append(idx)

            self.bucket_indices["global"].append(idx)

    # helpers to slice/resolve
    def indices_to_names(self, idxs: Iterable[int]) -> List[str]:
        return [self.names[i] for i in idxs]

    def basename_candidates(self, base: str, scope: Optional[Iterable[int]] = None) -> List[int]:
        idxs = self.basename_map.get(base, [])
        if scope is None:
            return idxs
        scope_set = set(scope)
        return [i for i in idxs if i in scope_set]

    def ext_candidates(self, exts: Iterable[str], scope: Optional[Iterable[int]] = None) -> List[int]:
        pool = []
        for e in exts:
            pool.extend(self.ext_map.get(e, []))
        if scope is None:
            return pool
        scope_set = set(scope)
        return [i for i in pool if i in scope_set]

# -------- candidate selection --------

def suggest_bucket_for_pattern(pat: str) -> str:
    p = "/" + pat  # ease substring checks
    if "/Containers/Data/Application/" in p:
        return "sandbox"
    if "/Containers/Shared/AppGroup/" in p:
        return "appgroup"
    if "/PhotoData/" in p or "Photos.sqlite" in p:
        return "photos"
    if "/mobile/Library/Biome/" in p:
        return "biome"
    if "/mobile/Library/" in p:
        return "mobile_lib"
    return "global"

def split_dir_base(pattern: str) -> Tuple[str, str]:
    # Split without normalizing wildcards
    d, b = os.path.split(pattern)
    return d or "", b or ""

def db_family_from_basename(base: str) -> Optional[Tuple[str, List[str]]]:
    """
    If basename endswith `.db*` or `.sqlite*`, return (stem, [concrete_basenames])
    e.g., "foo.db*" -> ("foo.db", ["foo.db", "foo.db-wal", "foo.db-shm"])
           "bar.sqlite*" -> ("bar.sqlite", ["bar.sqlite", "bar.sqlite-wal", "bar.sqlite-shm"])
    Otherwise, None.
    """
    lb = base.lower()
    if lb.endswith(".db*"):
        stem = base[:-1]  # keep ".db"
        return stem, [stem, f"{stem}-wal", f"{stem}-shm"]
    if lb.endswith(".sqlite*"):
        stem = base[:-1]  # keep ".sqlite"
        return stem, [stem, f"{stem}-wal", f"{stem}-shm"]
    return None

def startswith_dir(name: str, fixed_dir: str) -> bool:
    # Match names that are under fixed_dir (posix)
    if not fixed_dir:
        return True
    # Normalize: ensure fixed_dir ends with '/'
    d = fixed_dir if fixed_dir.endswith("/") else fixed_dir + "/"
    return name.startswith(d)

def filter_by_fixed_dir(names: List[str], fixed_dir: str) -> List[str]:
    if not fixed_dir:
        return names
    d = fixed_dir if fixed_dir.endswith("/") else fixed_dir + "/"
    return [n for n in names if n.startswith(d)]

# -------- main searcher --------

class ImprovedSearcher:
    def __init__(self, archive_path: Path, out_root: Path):
        self.archive_path = archive_path
        self.out_root = out_root

        # Detect archive type and instantiate the correct reader
        if str(archive_path).lower().endswith('.zip'):
            self.archive: Archive = ZipArchive(archive_path)
            print("Processing ZIP file...")
        else:  # Default to TAR for .tar, .gz, etc.
            self.archive: Archive = TarArchive(archive_path)
            print("Processing TAR file...")

        # Time index building
        index_start = time.perf_counter()
        self.index = ArchiveIndex(self.archive)
        self.index_build_time = time.perf_counter() - index_start
        
        # Cache pattern -> list[str] paths (like self.searched in framework)
        self.memo: Dict[str, List[str]] = {}

    def close(self):
        try:
            self.archive.close()
        except Exception:
            pass

    def _exact_match(self, pat: str) -> Optional[List[str]]:
        # Legacy behavior matches against "root/" + name,
        # but for exact paths (no wildcards), users put real tar paths. Honor that.
        if has_wildcards(pat):
            return None
        return [pat] if pat in self.index.name_set else []

    def _choose_scope(self, pat: str) -> List[int]:
        bucket = suggest_bucket_for_pattern(pat)
        return self.index.bucket_indices[bucket]

    def _ext_hints(self, base: str) -> List[str]:
        lb = base.lower()
        if lb.endswith(".db*"):
            return [".db", "-wal", "-shm"]
        if lb.endswith(".sqlite*"):
            return [".sqlite", "-wal", "-shm"]
        if lb.endswith(".plist"):
            return [".plist"]
        if lb.endswith(".sqlite"):
            return [".sqlite"]
        return []

    def search(self, pattern: str) -> List[str]:
        if pattern in self.memo:
            return self.memo[pattern]

        # 0) exact match
        exact = self._exact_match(pattern)
        if exact is not None:
            self.memo[pattern] = exact
            return exact

        # 1) select initial bucket scope
        scope = self._choose_scope(pattern)
        scope_names = self.index.indices_to_names(scope)

        # 2) try SQLite "family" fast-path (by basename)
        dir_part, base = split_dir_base(pattern)
        dbfam = db_family_from_basename(base)
        if dbfam:
            stem, concrete_bases = dbfam
            # If directory has no wildcards, we can attempt direct O(1) exact hits
            if not has_wildcards(dir_part):
                hits = []
                for cb in concrete_bases:
                    candidate = os.path.join(dir_part, cb)
                    if candidate in self.index.name_set:
                        hits.append(candidate)
                if hits:
                    self.memo[pattern] = ordered_dedupe(hits)
                    return self.memo[pattern]
            else:
                # Directory has wildcards; try narrowing by basename in-scope
                hits = []
                scope_set = set(scope)  # limit lookups to bucket
                
                # Original logic for fixed stem (will fail on wildcard stem and fall through, which is correct)
                for cb in concrete_bases:
                    idxs = self.index.basename_candidates(cb, scope_set)
                    if not idxs:
                        continue
                    names = self.index.indices_to_names(idxs)
                    # If there is any fixed dir portion (even parent segments), filter by that prefix
                    if dir_part and not dir_part.startswith("*"):
                        names = filter_by_fixed_dir(names, dir_part.replace("\\", "/"))
                    hits.extend(names)
                
                if hits:
                    # Still need to ensure they actually match the whole glob (in case user’s pattern has more)
                    regex = compile_glob(normcase_posix("root/" + pattern))
                    matched = [n for n in ordered_dedupe(hits) if regex.match("root/" + n)]
                    if matched:
                        self.memo[pattern] = matched
                        return matched
                # else: fall through to general candidate filtering

        # 3) general candidate prefiltering
        candidates = scope_names

        # 3a) fixed basename?
        if base and not has_wildcards(base):
            idxs = self.index.basename_candidates(base, scope)
            candidates = self.index.indices_to_names(idxs)

        # 3b) extension hints?
        elif base:
            ext_candidates = self._ext_hints(base)
            if ext_candidates:
                idxs = self.index.ext_candidates(ext_candidates, scope)
                candidates = self.index.indices_to_names(idxs)

        # 3c) fixed directory?
        if dir_part and not has_wildcards(dir_part):
            candidates = filter_by_fixed_dir(candidates, dir_part.replace("\\", "/"))

        # 4) run fnmatch-derived regex only on candidates
        regex = compile_glob(normcase_posix("root/" + pattern))
        matches = [n for n in candidates if regex.match("root/" + n)]

        self.memo[pattern] = ordered_dedupe(matches)
        return self.memo[pattern]

# -------- runner --------

def main():
    if len(sys.argv) < 2:
        print("Usage: python exp/improved_tar_search.py /path/to/image.[tar.gz|zip]")
        sys.exit(2)

    archive_path = Path(sys.argv[1])
    if not archive_path.exists():
        print(f"Archive not found: {archive_path}")
        sys.exit(1)

    patterns_path = Path(__file__).with_name("path_list.txt")
    if not patterns_path.exists():
        print(f"Missing {patterns_path} (expected next to this script).")
        sys.exit(1)

    patterns = read_patterns(patterns_path)
    print(f"Loaded {len(patterns)} unique patterns from {patterns_path.name}")

    run_stamp = time.strftime("%Y%m%d-%H%M%S")
    out_root = Path(__file__).with_name("_out_improved") / run_stamp
    out_root.mkdir(parents=True, exist_ok=True)
    print(f"Extraction dir: {out_root}")

    searcher = ImprovedSearcher(archive_path, out_root)

    totals = 0
    rows: List[Tuple[str, int, float]] = []
    t0 = time.perf_counter()

    try:
        for i, pat in enumerate(patterns, 1):
            p0 = time.perf_counter()
            hits = searcher.search(pat)
            # extract
            for n in hits:
                # find member index quickly via name -> index (linear fallback if rare)
                # Build a quick map on first use
                # (For simplicity, a dict comp over name->idx is fine here; overhead is tiny vs search time)
                pass
            p1 = time.perf_counter()
            # Do extraction after measuring search timing, to isolate matching cost
            for n in hits:
                idx = searcher.index.names.index(n)  # O(N) but hits list is usually tiny
                member = searcher.index.members[idx]
                # searcher.archive.extract_member(member, out_root)
            dt = p1 - p0
            cnt = len(hits)
            totals += cnt
            rows.append((pat, cnt, dt))
            print(f"[{i:>4}/{len(patterns)}] {pat} -> {cnt} hits in {dt:.3f}s")
    finally:
        searcher.close()

    elapsed = time.perf_counter() - t0

    # Assign sequential IDs to patterns for linking
    pattern_to_id = {pat: idx for idx, pat in enumerate(patterns, 1)}

    # Collect detailed matches (including aux for DB patterns)
    detail_rows = []
    for pat in patterns:
        hits = searcher.memo.get(pat, [])  # Actual searched hits
        pat_id = pattern_to_id[pat]
        
        # Add actual hits
        for hit in hits:
            detail_rows.append((pat_id, hit))
        
    # Write improved_match_summary.csv (with ID)
    summary_csv_path = out_root / "improved_match_summary.csv"
    with summary_csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pattern_id", "pattern", "match_count", "seconds"])
        for pat, cnt, secs in rows:
            pat_id = pattern_to_id[pat]
            w.writerow([pat_id, pat, cnt, f"{secs:.6f}"])

    # Write improved_match_detail.csv
    detail_csv_path = out_root / "improved_match_detail.csv"
    with detail_csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pattern_id", "file_path"])
        for pat_id, path in sorted(detail_rows):
            w.writerow([pat_id, path])

    print("\n=== Improved summary ===")
    print(f"Patterns searched : {len(patterns)}")
    print(f"Total matches     : {totals}")
    print(f"Total time        : {elapsed:.3f}s")
    print(f"Index build time  : {searcher.index_build_time:.3f}s")
    print(f"Wrote summary CSV : {summary_csv_path}")
    print(f"Wrote detail CSV  : {detail_csv_path}")

    print("\n--- Bucket stats ---")
    for bucket_name, indices in searcher.index.bucket_indices.items():
        print(f"- {bucket_name:<12}: {len(indices):>8} files")



if __name__ == "__main__":
    main()
