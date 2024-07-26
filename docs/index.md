# qualyspy - A Python Package for Interacting With Qualys APIs

This package attempts to make it much easier to interact with Qualys's various API endpoints, across as many modules as I can find time to code.

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






