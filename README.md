# qualysdk - A Python SDK for Interacting With Qualys APIs
![Logo](https://raw.githubusercontent.com/0x41424142/qualysdk/main/imgs/qualysdkLogo.png)

[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black) ![Development Status](https://img.shields.io/badge/in%20development-8A2BE2?style=for-the-badge)  ![PyPI - Latest Version](https://img.shields.io/pypi/v/qualysdk?style=for-the-badge&logo=pypi&logoColor=yellow) ![Python Versions](https://img.shields.io/pypi/pyversions/qualysdk?style=for-the-badge&logo=python&logoColor=yellow) ![GitHub Stars](https://img.shields.io/github/stars/0x41424142/qualysdk?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/qualysdk?style=for-the-badge&logo=pypi&logoColor=yellow)


![Black Formatter Status](https://github.com/0x41424142/qualysdk/actions/workflows/black.yml/badge.svg?event=push) ![CodeQL Scan Status](https://github.com/0x41424142/qualysdk/actions/workflows/codeql.yml/badge.svg?branch=main)


This SDK attempts to make it much easier to interact with Qualys's various API endpoints, across as many modules as I can find time to code.

## Uber Class Example
```py
from qualysdk import TokenAuth, GAVUber

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
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_host_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Pull 4 pages of hosts, with "All/AGs" details & tags:
hosts = get_host_list(auth, details="All/AGs", show_tags=True, page_count=4)
>>>[VMDRHost(12345), ...]
```

## Current Supported Modules 

>**Head's Up!:** SQL DB uploading is currently in development! 🎉

|Module| Status |
|--|--|
| GAV (Global AssetView) |✅|
| VMDR | In Progress (```query_kb```, ```get_kb_qvs```, ```get_host_list```, ```get_hld```, ```get_ag_list```, ```add/edit/remove_ag```, ```get_ip_list```, ```add/update_ips```, ```get_scan_list```, ```pause_scan```, ```cancel_scan```, ```resume_scan```, ```delete_scan```, ```launch_scan```, ```fetch_scan```, ```get_scanner_list```, ```get_static_searchlists```, ```get_report_list```, ```launch/cancel/fetch/delete_report```, ```get_template_list```, ```get_scheduled_report_list```, ```launch_scheduled_report```, ```get_user_list```, ```add/edit_user```, ```get_activity_log```, ```purge_hosts``` implemented) |
| PM (Patch Management) | Not Started |
| WAS | In Planning |
| TC (TotalCloud) | Started |
|Connectors | Not Started |
|Cloud Agent | In Progress (```purge_agent```, ```bulk_purge_agent```, ```list_agents``` implemnted) |
|CS (Container Security) | Not Started
|ADMIN (Administration) | Not Started
|Tagging| Not Started


# Documentation/Get Started


For more detailed information on the package, including how to get up and running, please see the [documentation](https://qualysdk.jakelindsay.uk).

# Disclaimer

This SDK tool is an independent project and is not an official product of Qualys. It has been developed and maintained solely by the names listed in the GitHub contributors list. Qualys has neither endorsed nor approved this SDK.

Users of this SDK are advised to use it at their own risk and discretion.

For official tools and support, please refer to the official Qualys resources and documentation.

# TODO:

- Multithread ```gav.get_all_assets```.

- Start work on TotalCloud/WAS modules.

- Continue SQL integration.
