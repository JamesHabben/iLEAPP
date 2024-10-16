__artifacts_v2__ = {
    "get_confaccts": {
        "name": "Account Configuration",
        "description": "Extracts account configuration information from the device",
        "author": "@AlexisBrignoni",
        "version": "0.2",
        "date": "2022-08-09",
        "requirements": "none",
        "category": "Accounts",
        "notes": "",
        "paths": ('**/com.apple.accounts.exists.plist',),
        "output_types": "all"
    }
}

import plistlib
from scripts.ilapfuncs import artifact_processor

@artifact_processor
def get_confaccts(files_found, report_folder, seeker, wrap_text, timezone_offset):
    data_list = []
    file_found = str(files_found[0])
    with open(file_found, "rb") as fp:
        pl = plistlib.load(fp)
        for key, val in pl.items():
            data_list.append((key, val))
    
    data_headers = ('Key', 'Values')
    return data_headers, data_list, file_found
