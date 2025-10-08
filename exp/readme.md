# Experimental Archive Search Scripts

This directory contains experimental Python scripts designed to test and compare different strategies for searching file patterns within large TAR and ZIP archives, like those from mobile device extractions.

The goal is to evaluate a faster, indexed search method against the current baseline implementation.

## Scripts

### `tar_search_baseline.py`
- **What it does:** Replicates the current `iLEAPP` framework's file search behavior. It performs a linear scan through the archive for each pattern.
- **Purpose:** Serves as the control for performance and accuracy comparison.

### `tar_search_improved.py`
- **What it does:** Implements an optimized search strategy. It first builds a set of in-memory indexes (by filename, extension, and path heuristics) in a single pass over the archive. It then uses these indexes to dramatically reduce the number of files that need to be checked for each pattern.
- **Purpose:** To demonstrate a significant speedup in search time with minimal impact on accuracy.

## Running the Experiment

Both scripts are run from the root of the `iLEAPP` repository.

### 1. Generate the Pattern List

The scripts rely on a `path_list.txt` file, which contains all file search patterns used by the `iLEAPP` modules. If this file doesn't exist, generate it by running:
```bash
python ileapp.py -p
```

### 2. Run a Script

Execute either script by passing the path to a TAR or ZIP archive as an argument.

**For the baseline test:**
```bash
python exp/tar_search_baseline.py /path/to/your/archive.tar
```

**For the improved test:**
```bash
python exp/tar_search_improved.py /path/to/your/archive.zip
```

## Output

Each script will create a timestamped output directory inside `exp/` (e.g., `_out_baseline/` or `_out_improved/`). These directories will contain:
-   `_match_summary.csv`: A summary of match counts and timings for each pattern.
-   `_match_detail.csv`: A detailed list of every file path that was found, linked by a pattern ID.

The console output will provide a real-time progress log and a final summary of total matches, timings, and (for the improved script) statistics on the index and buckets.
