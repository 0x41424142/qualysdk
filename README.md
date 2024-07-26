# qualyspy - A Python Package for Interacting With Qualys APIs
```
··············································
:   ____             _                       :
:  /___ \_   _  __ _| |_   _ ___ _ __  _   _ :
: //  / | | | |/ _` | | | | / __| '_ \| | | |:
:/ \_/ /| |_| | (_| | | |_| \__ | |_) | |_| |:
:\___,_\ \__,_|\__,_|_|\__, |___| .__/ \__, |:
:                      |___/    |_|    |___/ :
··············································
 ```

This package attempts to make it much easier to interact with Qualys's various API endpoints, across as many modules as I can find time to code.

[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![Development Status](https://img.shields.io/badge/in%20development-8A2BE2) ![Black Formatter Status](https://github.com/0x41424142/qualyspy/actions/workflows/black.yml/badge.svg?event=push) ![CodeQL Scan Status](https://github.com/0x41424142/qualyspy/actions/workflows/codeql.yml/badge.svg?branch=main)

## Uber Class Example
```py
from qualyspy import TokenAuth, GAVUber

auth = TokenAuth(<username>, <password>, platform='qg1')
uber = GAVUber(auth)

assets = uber.get(
    "query_assets", 
    filter='operatingSystem:"Linux"', 
    lastModifiedDate="2024-06-21"
    )
>>>[AssetID(012345678), ...]
```
## Non-Uber Class Example
```py
from qualyspy.auth import BasicAuth
from qualyspy.vmdr import get_host_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Pull 4 pages of hosts, with "All/AGs" details & tags:
hosts = get_host_list(auth, details="All/AGs", show_tags=True, page_count=4)
>>>[VMDRHost(12345), ...]
```

## Current Supported Modules 
|Module| Status |
|--|--|
| GAV (Global AssetView) |✅|
| VMDR | In Progress (```query_kb```, ```get_host_list```, ```get_hld```, ```get_ag_list```, ```add/edit/remove_ag```, ```get_ip_list```, ```add/update_ips```, ```get_scan_list```, ```pause_scan```, ```cancel_scan```, ```resume_scan```, ```delete_scan```, ```launch_scan```, ```fetch_scan``` implemented) |
| PM (Patch Management) | In Planning |
| WAS | Not Started |
| TC (TotalCloud) | Not Started |
|Connectors | Not Started |
|Cloud Agent | Not Started |
|CS (Container Security) | Not Started
|ADMIN (Administration) | Not Started
|Tagging| Not Started


# Documentation/Get Started

For more detailed information on the package, including how to get up and running, please see the [documentation](https://qualyspy.jakelindsay.uk).


# TODO:

- Continue adding VMDR APIs.

- Start work on PM module.

- Write testing files.

- Break up README.md: Move module-specific sections to their respective folders, cleaning up the main README.md.
