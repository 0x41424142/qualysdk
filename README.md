# qualysdk - A Python SDK for Interacting With Qualys APIs
![Logo](https://raw.githubusercontent.com/0x41424142/qualysdk/main/imgs/qualysdkLogo.png)

[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black) ![Development Status](https://img.shields.io/badge/in%20development-8A2BE2?style=for-the-badge)  ![PyPI - Latest Version](https://img.shields.io/pypi/v/qualysdk?style=for-the-badge&logo=pypi&logoColor=yellow) ![Python Versions](https://img.shields.io/pypi/pyversions/qualysdk?style=for-the-badge&logo=python&logoColor=yellow) ![GitHub Stars](https://img.shields.io/github/stars/0x41424142/qualysdk?style=for-the-badge) ![GitHub License](https://img.shields.io/github/license/0x41424142/qualysdk?style=for-the-badge)


![Black Formatter Status](https://github.com/0x41424142/qualysdk/actions/workflows/black.yml/badge.svg?event=push) ![CodeQL Scan Status](https://github.com/0x41424142/qualysdk/actions/workflows/codeql.yml/badge.svg?branch=main) [![CodeFactor](https://www.codefactor.io/repository/github/0x41424142/qualysdk/badge)](https://www.codefactor.io/repository/github/0x41424142/qualysdk)


This SDK attempts to make it much easier to interact with Qualys's various API endpoints, across as many modules as I can find time to code.

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_host_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Pull 4 pages of hosts, with "All/AGs" details & tags:
hosts = get_host_list(auth, details="All/AGs", show_tags=True, page_count=4)
>>>[VMDRHost(12345), ...]
```

## Current Supported Modules 


|Module| Status |
|--|--|
| GAV (Global AssetView) |✅ See GAV [documentation page](https://qualysdk.jakelindsay.uk/gav/) for supported calls ||
| VMDR | ✅ See VMDR [documentation page](https://qualysdk.jakelindsay.uk/vmdr/) for supported calls |
| PM (Patch Management) | See Patch Management [documentation page](https://qualysdk.jakelindsay.uk/patch/) for supported calls |
| WAS | ✅ See WAS [documentation page](https://qualysdk.jakelindsay.uk/was/) for supported calls |
| TC (TotalCloud) | ✅ See TotalCloud [documentation page](https://qualysdk.jakelindsay.uk/totalcloud/) for supported calls. |
|Connectors | Not Started |
|Cloud Agent | ✅ See Cloud Agent [documentation page](https://qualysdk.jakelindsay.uk/cloudagent/) for supported calls |
|CS (Container Security) | ✅ See CS [documentation page](https://qualysdk.jakelindsay.uk/containersecurity/) for supported calls |
|ADMIN (Administration) | Not Started |
|Asset Management & Tagging| Not Started |
| SQL Data Uploads | ✅ See SQL [documentation page](https://qualysdk.jakelindsay.uk/sql/) for supported uploads/DBs |


# Documentation/Get Started


For more detailed information on the package, including how to get up and running, please see the [documentation](https://qualysdk.jakelindsay.uk).

# Disclaimer

This SDK tool is an independent project and is not an official product of Qualys. It has been developed and maintained solely by the names listed in the GitHub contributors list. Qualys has neither endorsed nor approved this SDK.

Users of this SDK are advised to use it at their own risk and discretion.

For official tools and support, please refer to the official Qualys resources and documentation.

