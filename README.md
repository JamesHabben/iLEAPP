# iLEAPP

iOS Logs, Events, And Plists Parser  
Details in blog post here: https://abrignoni.blogspot.com/2019/12/ileapp-ios-logs-events-and-properties.html

Supports iOS/iPadOS 11, 12, 13 and 14, 15, 16.
Select parsing directly from a compressed .tar/.zip file, or a decompressed directory, or an iTunes/Finder backup folder.

## Features

Parses:  
⚙️ Mobile Installation Logs  
⚙️ iOS 12+ Notifications  
⚙️ Build Info (iOS version, etc.)  
⚙️ Wireless cellular service info (IMEI, number, etc.)  
⚙️ Screen icons list by screen and in grid order.  
⚙️ ApplicationState.db support for app bundle ID to data container GUID correlation.   
⚙️ User and computer names that the iOS device connected to. Function updated by Jack Farley (@JackFarley248, http://farleyforensics.com/).  
etc...

## Requirements

Python 3.9 to latest version (older versions of 3.x will also work with the exception of one or two modules)
If on macOS (Intel) make sure Xcode is installed and have command line tools updated to be able to use Python 3.11. 

### Dependencies

Dependencies for your python environment are listed in `requirements.txt`. Install them using the below command. Ensure 
the `py` part is correct for your environment, eg `py`, `python`, or `python3`, etc. 

`py -m pip install -r requirements.txt`  
or  
 `pip3 install -r requirements.txt`

To run on **Linux**, you will also need to install `tkinter` separately like so:

`sudo apt-get install python3-tk`

To install on Windows follow the guide, courtesy of Hexordia, here:
https://www.hexordia.com/s/ILEAPP-Walkthrough.pdf

Windows installation and walkthrough video, by Hexordia, here:
https://www.youtube.com/watch?v=7qvVFfBM2NU

## Compile to executable

Compile to an executable (.exe file) to run this on a system without python installed. This must be built first from 
a system that has python installed. Python 3.10 and up (3.10 is not the same as 3.1) works 
different from 3.9 and below.

### Print Python Version
Run this at a command prompt:
```commandline
python --version
```

### Python version 3.10 and up
Run one of these lines in the base folder of this script package:

```
pyinstaller ileapp.spec

pyinstaller ileappGUI.spec
```
### Python version 3.9 and below
Run one of these lines in the base folder of this script package:
```
pyinstaller --onefile ileapp.spec

pyinstaller --onefile --noconsole ileappGUI.spec
```

## Usage

### CLI

```
$ python ileapp.py -t <zip | tar | fs | gz> -i <path_to_extraction> -o <path_for_report_output>
```

### GUI

```
$ python ileappGUI.py 
```

### Help

```
$ python ileapp.py --help
```

## Contributing artifact plugins

Each plugin is a Python source file which should be added to the `scripts/artifacts` folder which will be loaded dynamically each time ILEAPP is run.

The plugin source file must contain a dictionary named `__artifacts_v2__` at the very beginning of the module, which defines the artifacts that the plugin processes. The keys in the `__artifacts_v2__` dictionary should be IDs for the artifact(s) which must be unique within ILEAPP. The values should be dictionaries containing the following keys:

- `name`: The name of the artifact as a string.
- `description`: A description of the artifact as a string.
- `author`: The author of the plugin as a string.
- `version`: The version of the artifact as a string.
- `date`: The date of the last update to the artifact as a string.
- `requirements`: Any requirements for processing the artifact as a string.
- `category`: The category of the artifact as a string.
- `notes`: Any additional notes as a string.
- `paths`: A tuple of strings containing glob search patterns to match the path of the data that the plugin expects for the artifact.
- `function`: The name of the function which is the entry point for the artifact's processing as a string.

For example:

```python
__artifacts_v2__ = {
    "cool_artifact_1": {
        "name": "Cool Artifact 1",
        "description": "Extracts cool data from database files",
        "author": "@username",
        "version": "0.1",
        "date": "2022-10-25",
        "requirements": "none",
        "category": "Really cool artifacts",
        "notes": "",
        "paths": ('*/com.android.cooldata/databases/database*.db',),
        "function": "get_cool_data1"
    },
    "cool_artifact_2": {
        "name": "Cool Artifact 2",
        "description": "Extracts cool data from XML files",
        "author": "@username",
        "version": "0.1",
        "date": "2022-10-25",
        "requirements": "none",
        "category": "Really cool artifacts",
        "notes": "",
        "paths": ('*/com.android.cooldata/files/cool.xml',),
        "function": "get_cool_data2"
    }
}
```

The functions referenced as entry points in the `__artifacts__` dictionary must take the following arguments:

* An iterable of the files found which are to be processed (as strings)
* The path of ILEAPP's output folder(as a string)
* The seeker (of type FileSeekerBase) which found the files
* A Boolean value indicating whether or not the plugin is expected to wrap text

For example:

```python
def get_cool_data1(files_found, report_folder, seeker, wrap_text):
    pass  # do processing here
```

Plugins are generally expected to provide output in ILEAPP's HTML output format, TSV, and optionally submit records to 
the timeline. Functions for generating this output can be found in the `artifact_report` and `ilapfuncs` modules. 
At a high level, an example might resemble:

```python
__artifacts_v2__ = {
    "cool_artifact_1": {
        "name": "Cool Artifact 1",
        "description": "Extracts cool data from database files",
        "author": "@username",  # Replace with the actual author's username or name
        "version": "0.1",  # Version number
        "date": "2022-10-25",  # Date of the latest version
        "requirements": "none",
        "category": "Really cool artifacts",
        "notes": "",
        "paths": ('*/com.android.cooldata/databases/database*.db',),
        "function": "get_cool_data1"
    }
}

import datetime
from scripts.artifact_report import ArtifactHtmlReport
import scripts.ilapfuncs

def get_cool_data1(files_found, report_folder, seeker, wrap_text):
    # let's pretend we actually got this data from somewhere:
    
    rows = [
     ((datetime.datetime.now(), 'datetime'), "Cool data col 1, value 1", "Cool data col 1, value 2", "Cool data col 1, value 3"),
     ((datetime.datetime.now(), 'datetime'), "Cool data col 2, value 1", "Cool data col 2, value 2", "Cool data col 2, value 3"),
    ]
    
    headers = ["Timestamp", "Data 1", "Data 2", "Data 3"]
    
    # HTML output:
    report = ArtifactHtmlReport("Cool stuff")
    report_name = "Cool DFIR Data"
    report.start_artifact_report(report_folder, report_name)
    report.add_script()
    report.write_artifact_data_table(headers, rows, files_found[0])  # assuming only the first file was processed
    report.end_artifact_report()
    
    # TSV output:
    scripts.ilapfuncs.tsv(report_folder, headers, rows, report_name, files_found[0])  # assuming first file only
    
    # Timeline:
    scripts.ilapfuncs.timeline(report_folder, report_name, rows, headers)
```
### Special Data Handlers

The report generation has the capability to apply handlers on certain types of data. The handlers allow for the 
output data to have additional formatting or functions applied to it inside the report. The date type that drove 
this feature was datetimes. The handling built into the reporting allows for the viewer of the report to choose 
a timezone to display the time in. This can be expanded to include other data types as well.

Here are the current date types with special handlers
- `datetime` designates this as a timestamp that can be adjusted by the timezone display setting
- `date` designates as a date that can be adjusted by the date format setting
- `time` designates as a time that can be adjusted by the time format setting and by timezone setting
- `phonenumber` designates as a phone number that can be formatted to that expected by the region it's from

Use the special handlers by passing a value and a string inside a Tuple
```python
row = (
    (created_date, 'datetime'), # tuple using 'datetime' handler
    first_name,
    last_name,
    (mobile_num, 'phonenumber') # tuple using 'phonenumber' handler
)
```

## Acknowledgements

This tool is the result of a collaborative effort of many people in the DFIR community.
