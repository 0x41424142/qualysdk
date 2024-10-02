# Web Application Scanning APIs

WAS APIs return data on web apps in your subscription, as well as manage them.

After running:
```py
from qualysdk.was import *
```
You can use any of the endpoints currently supported:

## WAS Endpoints

|API Call| Description |
|--|--|
| ```count_webapps``` | Returns the number of web apps in the subscription that match given kwargs. |
| ```get_webapps``` | Returns a list of web apps in the subscription that match given kwargs. |


## Count Webapps API

```count_webapps``` returns the number of web apps in the subscription that match the given kwargs.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ```Union[str, int]``` | Web app ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Web app name | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the name filter | ❌ |
| ```url``` | ```str``` | Web app URL | ❌ |
| ```url_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the URL filter | ❌ |
| ```tags_name``` | ```str``` | Tag name | ❌ |
| ```tags_name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the tag name filter | ❌ |
| ```tags_id``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tag ID filter | ❌ |
| ```createdDate``` | ```str``` | Date created | ❌ |
| ```createdDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the created date filter | ❌ |
| ```updatedDate``` | ```str``` | Date updated | ❌ |
| ```updatedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the updated date filter | ❌ |
| ```isScheduled``` | ```bool``` | If the webapp has a scan scheduled | ❌ |
| ```isScheduled_operator``` | ```Literal["EQUALS", "NOT EQUALS"]``` | Operator for the isScheduled filter | ❌ |
| ```isScanned``` | ```bool``` | If the webapp has been scanned | ❌ |
| ```isScanned_operator``` | ```Literal["EQUALS", "NOT EQUALS"]``` | Operator for the isScanned filter | ❌ |
| ```lastScan_status``` | ```Literal["SUBMITTED", "RUNNING", "FINISHED", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "ERROR", "CANCELLED"]``` | Status of the last scan | ❌ |
| ```lastScan_status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the lastScan_status filter | ❌ |
| ```lastScan_date``` | ```str``` | Date of the last scan in UTC date/time format | ❌ |
| ```lastScan_date_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the lastScan_date filter | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import count_webapps

auth = BasicAuth(<username>, <password>)

# Get the number of webapps that have a lastScan.status of "RUNNING":
webapps = count_webapps(auth, lastScan_status="RUNNING")
>>>5

# Get the number of webapps by searching by multiple tags:
webapps = count_webapps(auth, tags_id="12345,54321", tags_id_operator="IN")
>>>20

# Get the number of webapps where the name contains "prod":
webapps = count_webapps(auth, name="prod", name_operator="CONTAINS")
>>>10
```

## List Webapps API

```get_webapps``` returns a list of web apps in the subscription that match the given kwargs.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to return. If 'all', returns all pages | ❌ |
| ```id``` | ```Union[str, int]``` | Web app ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Web app name | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the name filter | ❌ |
| ```url``` | ```str``` | Web app URL | ❌ |
| ```url_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the URL filter | ❌ |
| ```tags_name``` | ```str``` | Tag name | ❌ |
| ```tags_name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the tag name filter | ❌ |
| ```tags_id``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tag ID filter | ❌ |
| ```createdDate``` | ```str``` | Date created | ❌ |
| ```createdDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the created date filter | ❌ |
| ```updatedDate``` | ```str``` | Date updated | ❌ |
| ```updatedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the updated date filter | ❌ |
| ```isScheduled``` | ```bool``` | If the webapp has a scan scheduled | ❌ |
| ```isScheduled_operator``` | ```Literal["EQUALS", "NOT EQUALS"]``` | Operator for the isScheduled filter | ❌ |
| ```isScanned``` | ```bool``` | If the webapp has been scanned | ❌ |
| ```isScanned_operator``` | ```Literal["EQUALS", "NOT EQUALS"]``` | Operator for the isScanned filter | ❌ |
| ```lastScan_status``` | ```Literal["SUBMITTED", "RUNNING", "FINISHED", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "ERROR", "CANCELLED"]``` | Status of the last scan | ❌ |
| ```lastScan_status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the lastScan_status filter | ❌ |
| ```lastScan_date``` | ```str``` | Date of the last scan in UTC date/time format | ❌ |
| ```lastScan_date_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the lastScan_date filter | ❌ |
| ```verbose``` | ```bool``` | If True, returns all tags for the webapp | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_webapps

auth = BasicAuth(<username>, <password>)
# Get the webapps that have a lastScan.status of "RUNNING". Include tags:
webapps = get_webapps(auth, lastScan_status="RUNNING", verbose=True)
>>>[
    WebApp(
        id=12345678, 
        name="My Awesome Site", 
        url="https://example.com", 
        ...
    ), 
    WebApp(
        id=98765432, 
        ...
    ),
    ...
]
```