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
| ```get_webapp_details``` | Returns all attributes of a single web app. |
| ```get_webapps_verbose``` | Combines the functionality of ```get_webapps``` and ```get_webapp_details``` to return a list of web apps with all attributes. Great for SQL data uploads.|
| ```create_webapp``` | Creates a new web app in the subscription. |


## Count Webapps API

```count_webapps``` returns the number of web apps in the subscription that match the given kwargs.

>**Head's Up!** This method is useful for quickly getting a count of webapps that match a certain criteria. It does NOT return the webapps themselves, or any attributes of the webapps.

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

## Get Webapp Details API

```get_webapp_details``` returns all attributes of a single web app.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```webappId``` | ```Union[str, int]``` | Web app ID | ✅ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_webapp_details, get_webapps

# First, get the ID of the webapp you want to get details for:
auth = BasicAuth(<username>, <password>)
webapps = get_webapps(auth, name="My Awesome Site", id=12345678)
webapp_id = webapps[0].id

# Get the details for the webapp:
webapp = get_webapp_details(auth, webappId=webapp_id)
>>>WebApp(
    id=12345678, 
    name="My Awesome Site", 
    url="https://example.com", 
    riskScore=100,
    owner_firstName="John",
    owner_lastName="Doe",
    ...
)
```

## Get Webapps Verbose API

```get_webapps_verbose``` combines the functionality of ```get_webapps``` and ```get_webapp_details``` to return a list of web apps with all attributes. 

This method uses threading to speed up the process. Number of threads can be set with the ```thread_count``` parameter.


|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```thread_count``` | ```int``` | Number of threads to use for the request | ❌ |
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
from qualysdk.was import get_webapps_verbose

auth = BasicAuth(<username>, <password>)

# Get all webapps with all attributes:
webapps = get_webapps_verbose(auth)
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

# Get all webapps with all attributes 
# that have "prod" in the name, using 10 threads:
webapps = get_webapps_verbose(
    auth,
    name="prod",
    name_operator="CONTAINS",
    thread_count=10
)
>>>[
    WebApp(
        id=12345678, 
        name="My Awesome Site (prod)", 
        url="https://example.com", 
        ...
    ), 
    WebApp(
        id=98765432, 
        name="My Other Site (prod)",
        ...
    ),
    ...
]
```

## Create Webapp API

```create_webapp``` creates a new web app in the subscription.

>**Head's Up!:** More optional attributes will be supported in the future.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```name``` | ```str``` | Web app name | ✅ |
| ```url``` | ```str``` | Web app URL | ✅ |
| ```authRecord_id``` | ```Union[str, int]``` | Auth record ID | ❌ |
| ```uris``` | ```Union[str, list[str]]``` | a single URI string or a list of URI strings | ❌ |
| ```tag_ids``` | ```Union[int, list[int]]``` | a single tag ID or a list of tag IDs | ❌ |
| ```domains``` | ```Union[str, list[str]]``` | a single domain string or a list of domain strings | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import create_webapp

auth = BasicAuth(<username>, <password>)

# Create a new webapp with 
# minimal attributes:
new_webapp = create_webapp(
    auth,
    name="My New Site",
    url="https://newsite.com"
)

# Create a new webapp with
# URIs, tags, and an auth record:
new_webapp = create_webapp(
    auth,
    name="My New Site",
    url="https://newsite.com",
    uris=["https://newsite.com/admin", "https://newsite.com/blog", "https://newsite.com/contact"],
    authRecord_id=12345678 # Only one auth record be be specified in the API call
    tag_ids=[12345, 54321]
)
>>>WebApp(
    id=12345678, 
    name="My New Site", 
    url="https://newsite.com", 
    uris=["https://newsite.com/admin", "https://newsite.com/blog", "https://newsite.com/contact"],
    tags=[WASTag(id=12345, name='Prod'), WASTag(id=54321, name='News')],
    ...
)
```
