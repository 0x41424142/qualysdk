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
| ```update_webapp``` | Updates a web app in the subscription. |
| ```delete_webapp``` | Deletes a web app in the subscription. |
| ```purge_webapp``` | Purges scan data for a web app in the subscription. |
| ```get_selenium_script``` | Returns the Selenium script associated with a web app |
| ```count_authentication_records``` | Returns the number of authentication records in the subscription that match given kwargs. |
| ```get_authentication_records``` | Returns a list of authentication records in the subscription that match given kwargs. |
| ```get_authentication_record_details``` | Returns all attributes of a single authentication record. |
| ```create_authentication_record``` | Creates a new authentication record in the subscription. |
| ```delete_authentication_record``` | Deletes an authentication record in the subscription. |
| ```count_findings``` | Returns the number of findings in the subscription that match given kwargs. |
| ```get_findings``` | Returns a list of findings in the subscription that match given kwargs. |
| ```get_finding_details``` | Returns all attributes of a single finding. |
| ```get_findings_verbose``` | Combines the functionality of ```get_findings``` and ```get_finding_details``` to return a list of findings with all attributes. Great for SQL data uploads. |
| ```count_scans``` | Returns the number of scans in the subscription that match given kwargs. |
| ```get_scans``` | Returns a list of scans in the subscription that match given kwargs. |
| ```get_scan_details``` | Returns all attributes of a single scan. |
| ```get_scans_verbose``` | Combines the functionality of ```get_scans``` and ```get_scan_details``` to return a list of scans with all attributes. Great for SQL data uploads. |
| ```launch_scan``` | Launches a scan in the subscription. |
| ```cancel_scan``` | Cancels a scan in the subscription. |
| ```get_scan_status``` | Returns the status of a scan and the results/status of trying to authenticate to the target. |

## Count Webapps API

```count_webapps``` returns the number of web apps in the subscription that match the given kwargs.

>**Head's Up!** This method is useful for quickly getting a count of webapps that match certain criteria. It does NOT return the webapps themselves, or any attributes of the webapps.

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
| ```uris``` | ```Union[str, list[str]]``` | Single URI string or a list of URI strings | ❌ |
| ```tag_ids``` | ```Union[int, list[int]]``` | Single tag ID or a list of tag IDs | ❌ |
| ```domains``` | ```Union[str, list[str]]``` | Single domain string or a list of domain strings | ❌ |
| ```scannerTag_ids``` | ```Union[int, list[int]]``` | Single tag ID or a list of tag IDs associated with scanner appliances to assign | ❌ |

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
    authRecord_id=12345678 # Only one auth record can be specified in the API call
    tag_ids=[12345, 54321],
    ...
)
>>>WebApp(
    id=12345678, 
    name="My New Site", 
    url="https://newsite.com", 
    uris=["https://newsite.com/admin", "https://newsite.com/blog", "https://newsite.com/contact"],
    tags=[WASTag(id=12345, name='Prod'), WASTag(id=54321, name='News')],
    ...
)

# Create a new webapp with
# 2 default scanner tags:
new_webapp = create_webapp(
    auth,
    name="My New Site",
    url="https://newsite.com",
    scannerTag_ids=[12345, 54321],
    ...
)
```

## Update Webapp API

```update_webapp``` updates a web app in the subscription. 

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```webappId``` | ```Union[str, int]``` | Web app ID | ✅ |
| ```name``` | ```str``` | Web app name | ❌ |
| ```url``` | ```str``` | Web app URL | ❌ |
| ```attributes``` | ```dict["add": {key: value}, "remove": list[str]]``` | Attributes to add or remove. | ❌ |
| ```defaultProfile_id``` | ```int``` | Default profile ID | ❌ |
| ```urlExcludelist``` | ```list[str]``` | List of URLs to exclude | ❌ |
| ```urlAllowlist``` | ```list[str]``` | List of URLs to allow | ❌ |
| ```postDataExcludelist``` | ```list[str]``` | List of post data paths to exclude | ❌ |
| ```useSitemap``` | ```bool``` | If True, use the sitemap | ❌ |
| ```headers``` | ```list["Header_name: Header_value"]``` | List of headers | ❌ |
| ```authRecord_id``` | ```dict["add": int, "remove": int]``` | Auth record ID to add or remove | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import update_webapp

auth = BasicAuth(<username>, <password>)
webapp_id = 12345678

# Update the name of a webapp:
updated_webapp = update_webapp(
    auth,
    webappId=webapp_id,
    name="My Updated Site"
)

# Remove current auth record and add a new one:
updated_webapp = update_webapp(
    auth,
    webappId=webapp_id,
    authRecord_id={"add": 98765432, "remove": 12345678}
)

# Add new headers:
updated_webapp = update_webapp(
    auth,
    webappId=webapp_id,
    headers=["X-Frame-Options: DENY", "Content-Security-Policy: default-src 'self'"]
)

# Add/remove custom attributes:
updated_webapp = update_webapp(
    auth,
    webappId=webapp_id,
    attributes={"add": {"custom_attribute": "custom_value"}, "remove": ["old_custom_attribute1", "old_custom_attribute2"]}
)

# add URLs to the exclude list:
updated_webapp = update_webapp(
    auth,
    webappId=webapp_id,
    urlExcludelist=["https://example.com/admin", "https://example.com/blog"]
)
```

## Delete Webapp API

```delete_webapp``` deletes a web app in the subscription.

Returns a list of webapp IDs that were deleted as a dictionary: ```{"id": <id>}```

>**Head's Up!:** Using this API may only remove the WAS-specific asset in the subscription. It may still be active in other Qualys modules, such as Global AssetView's web application view.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```removeFromSubscription``` | ```bool=True``` | If ```True```, removes the webapp from the subscription. If ```False```, removes webapp from WAS only | ❌ |
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
from qualysdk.was import delete_webapp

auth = BasicAuth(<username>, <password>)

# Delete a webapp by ID:
delete_webapp(auth, id=12345678)

# Delete multiple webapps by ID:
delete_webapp(auth, id="12345678,98765432", id_operator="IN")

# Delete all webapps that have the "deprecated" tag:
delete_webapp(auth, tags_name="deprecated", tags_name_operator="EQUALS")
>>>[{"id": 12345678}, {"id": 98765432}, ...]
```

## Purge Webapp Scan Data API

```purge_webapp``` purges scan data for a web app in the subscription.

Returns a list of webapp IDs that were purged as a dictionary: ```{"id": <id>}```

>**Head's Up!:** Using this API may de-activate the WAS-specific asset in the subscription. It may still be active in other Qualys modules.

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
from qualysdk.was import purge_webapp

auth = BasicAuth(<username>, <password>)

# Purge scan data for a webapp by ID:
purge_webapp(auth, id=12345678)

# Purge scan data for multiple webapps by ID:
purge_webapp(auth, id="12345678,98765432", id_operator="IN")

# Purge scan data for all webapps that have the "deprecated" tag:
purge_webapp(auth, tags_name="deprecated", tags_name_operator="EQUALS")
>>>[{"id": 12345678}, {"id": 98765432}, ...]
```

## Download a Web App's Associated Selenium Script API

```get_selenium_script``` returns the Selenium script associated with a web app.

>**Head's Up!** Currently, code to create a dataclass object out of the response to this API has not been written. This is a stub. If you have written the code yourself, please submit a [pull request!](https://github.com/0x41424142/qualysdk/pulls) This method will still return data, but it will be the raw data underneath the API response's ```data``` XML tag.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ```Union[str, int]``` | Web app ID | ✅ |
| ```crawlingScripts_id``` | ```Union[str, int]``` | Crawling script ID | ✅ |


```py
from qualysdk import BasicAuth
from qualysdk.was import get_selenium_script

auth = BasicAuth(<username>, <password>)

# STUB!
```

## Count Authentication Records API

```count_authentication_records``` returns the number of authentication records in the subscription that match the given kwargs.

>**Head's Up!** This method is useful for quickly getting a count of authentication records that match certain criteria. It does NOT return the authentication records themselves, or any attributes of the authentication records.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ```Union[str, int]``` | Auth record ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Auth record name | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the name filter | ❌ |
| ```tags``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tags filter | ❌ |
| ```tags_name``` | ```str``` | Tag name | ❌ |
| ```tags_name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the tag name filter | ❌ |
| ```tags_id``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tag ID filter | ❌ |
| ```createdDate``` | ```str``` | Date created | ❌ |
| ```createdDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the created date filter | ❌ |
| ```updatedDate``` | ```str``` | Date updated | ❌ |
| ```updatedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the updated date filter | ❌ |
| ```isUsed``` | ```bool``` | If the auth record is in use | ❌ |
| ```isUsed_operator``` | ```Literal["EQUALS", "NOT EQUALS"]``` | Operator for the isUsed filter | ❌ |
| ```lastScan_authStatus``` | ```Literal["NONE", "NOT_USED", "PARTIAL", "FAILED", "SUCCESSFUL"]``` | Status of the last scan | ❌ |
| ```lastScan_authStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the lastScan_authStatus filter | ❌ |
| ```lastScan_date``` | ```str``` | Date of the last scan in UTC date/time format | ❌ |
| ```lastScan_date_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the lastScan_date filter | ❌ |
| ```contents``` | ```Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]``` | Auth record contents | ❌ |
| ```contents_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the contents filter | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import count_authentication_records

auth = BasicAuth(<username>, <password>)

# Get the number of Selenium auth records that have a lastScan.authStatus of "FAILED":
failed_selenium = count_authentication_records(
    auth,
    lastScan_authStatus="FAILED",
    contents="FORM_SELENIUM"
)
>>>5

# Get all OAuth2 auth records:
oauth2 = count_authentication_records(
    auth,
    contents="OAUTH2_AUTH_CODE,OAUTH2_IMPLICIT,OAUTH2_PASSWORD,OAUTH2_CLIENT_CREDS",
    contents_operator="IN"
)
>>>50
```

## List Authentication Records API

```get_authentication_records``` returns a list of authentication records in the subscription that match the given kwargs.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to return. If 'all', returns all pages | ❌ |
| ```id``` | ```Union[str, int]``` | Auth record ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Auth record name | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the name filter | ❌ |
| ```tags``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tags filter | ❌ |
| ```tags_name``` | ```str``` | Tag name | ❌ |
| ```tags_name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the tag name filter | ❌ |
| ```tags_id``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tag ID filter | ❌ |
| ```createdDate``` | ```str``` | Date created | ❌ |
| ```createdDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the created date filter | ❌ |
| ```updatedDate``` | ```str``` | Date updated | ❌ |
| ```updatedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the updated date filter | ❌ |
| ```isUsed``` | ```bool``` | If the auth record is in use | ❌ |
| ```isUsed_operator``` | ```Literal["EQUALS", "NOT EQUALS"]``` | Operator for the isUsed filter | ❌ |
| ```lastScan_authStatus``` | ```Literal["NONE", "NOT_USED", "PARTIAL", "FAILED", "SUCCESSFUL"]``` | Status of the last scan | ❌ |
| ```lastScan_authStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the lastScan_authStatus filter | ❌ |
| ```lastScan_date``` | ```str``` | Date of the last scan in UTC date/time format | ❌ |
| ```lastScan_date_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the lastScan_date filter | ❌ |
| ```contents``` | ```Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]``` | Auth record type | ❌ |
| ```contents_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the contents filter | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_authentication_records

auth = BasicAuth(<username>, <password>)

# Get all authentication records:
auth_records = get_authentication_records(auth)
>>>[
    WebAppAuthRecord(
        id=12345678,
        name="My Auth Record",
        owner_id=98765432,
        owner_firstName="John",
        owner_lastName="Doe",
        createdDate=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        updatedDate=datetime.datetime(2022, 2, 1, 0, 0, tzinfo=datetime.timezone.utc),
    ),
    ...
]

# Get all authentication records that have a lastScan.authStatus of "FAILED":
failed_auth_records = get_authentication_records(auth, lastScan_authStatus="FAILED")
>>>[
    WebAppAuthRecord(
        id=12345678,
        name="My Failed Auth Record",
        owner_id=98765432,
        owner_firstName="John",
        owner_lastName="Doe",
        createdDate=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        updatedDate=datetime.datetime(2022, 2, 1, 0, 0, tzinfo=datetime.timezone.utc),
    ),
    ...
]
```

## Get Authentication Record Details API

```get_authentication_record_details``` returns all attributes of a single auth record.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```recordId``` | ```Union[str, int]``` | Auth record ID | ✅ |

>**Head's Up!:** Server, Form, and OAuth2 passwords are automatically redacted when calling ```sql.upload_was_authentication_records``` and the record's ```secured``` attribute is set to ```True``` or the record's ```name``` attribute equals ```"password"```.

```py
from qualysdk import BasicAuth
from qualysdk.was import get_authentication_record_details, get_authentication_records

# First, get some IDs of the auth records you want to get details for:
auth = BasicAuth(<username>, <password>)
authrecords = get_authentication_records(auth)
authrecord_id = webapps[0].id

# Get the details for the webapp. Some fields have been removed for space:
webapp = get_authentication_record_details(auth, authrecord_id)
>>>WebAppAuthRecord(
    id=12345678, 
    name='My site', 
    owner_id=987654321, 
    owner_username='username',
    owner_firstName='Eddie', 
    owner_lastName='Van Halen', 
    formRecord_type='STANDARD', 
    formRecord_sslOnly=False, 
    formRecord_authVault=False, 
    formRecord_seleniumCreds=False, 
    formRecord_fields_count=2, 
    formRecord_fields_list=[
        WebAppAuthFormRecord(id=12345678, name='username', secured=False, value='username'), 
        WebAppAuthFormRecord(id=12345678, name='password', secured=False, value='Some Password')
    ], 
    tags_count=1, 
    tags_list=[WASTag(id=12345678, name='Main websites')], 
    comments_count=0, 
    comments_list=[], 
    createdDate=datetime.datetime(2024, 1, 1, 1, 10, 0, tzinfo=datetime.timezone.utc), 
    updatedDate=datetime.datetime(2024, 1, 1, 1, 30, 0, tzinfo=datetime.timezone.utc), 
    createdBy_id=12345678, 
    createdBy_username='username', 
    createdBy_firstName='Layne', 
    createdBy_lastName='Staley', 
    updatedBy_id=88888888, 
    updatedBy_username='username', 
    updatedBy_firstName='James', 
    updatedBy_lastName='Hetfield'
)
```

## Get Authentication Records Verbose API

```get_authentication_records_verbose``` combines the functionality of ```get_authentication_records``` and ```get_authentication_record_details``` to return a list of auth records with all attributes. 

This method uses threading to speed up the process. Number of threads can be set with the ```thread_count``` parameter.


|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```thread_count``` | ```int``` | Number of threads to use for the request | ❌ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to return. If 'all', returns all pages | ❌ |
| ```id``` | ```Union[str, int]``` | Auth record ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Auth record name | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the name filter | ❌ |
| ```tags``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tags filter | ❌ |
| ```tags_name``` | ```str``` | Tag name | ❌ |
| ```tags_name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the tag name filter | ❌ |
| ```tags_id``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tag ID filter | ❌ |
| ```createdDate``` | ```str``` | Date created | ❌ |
| ```createdDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the created date filter | ❌ |
| ```updatedDate``` | ```str``` | Date updated | ❌ |
| ```updatedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the updated date filter | ❌ |
| ```isUsed``` | ```bool``` | If the auth record is in use | ❌ |
| ```isUsed_operator``` | ```Literal["EQUALS", "NOT EQUALS"]``` | Operator for the isUsed filter | ❌ |
| ```lastScan_authStatus``` | ```Literal["NONE", "NOT_USED", "PARTIAL", "FAILED", "SUCCESSFUL"]``` | Status of the last scan | ❌ |
| ```lastScan_authStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the lastScan_authStatus filter | ❌ |
| ```lastScan_date``` | ```str``` | Date of the last scan in UTC date/time format | ❌ |
| ```lastScan_date_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the lastScan_date filter | ❌ |
| ```contents``` | ```Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]``` | Auth record type | ❌ |
| ```contents_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the contents filter | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_authentication_records_verbose

auth = BasicAuth(<username>, <password>)

# Get all auth records with all attributes:
authrecords = get_authentication_records_verbose(auth)
>>>[
    WebAppAuthRecord(
        id=12345678, 
        name="some auth record", 
        formRecord_type="SELENIUM",
        ...
    ), 
    WebAppAuthRecord(
        id=98765432, 
        ...
    ),
    ...
]

# Get all auth records with all attributes 
# that have "prod" in the name, using 10 threads:
authrecords = get_authentication_records_verbose(
    auth,
    name="prod",
    name_operator="CONTAINS",
    thread_count=10
)
>>>[
    WebAppAuthRecord(
        id=12345678, 
        name="some prod auth record",
        ...
    ), 
    ...
]
```

## Create Authentication Record API

```create_authentication_record``` creates a new authentication record in the subscription. You can create ```formRecord```, ```serverRecord```, and ```oauth2Record``` types. Each type requires different attributes, which are detailed below. 

>**Head's Up!:** The options for this API endpoint are quite complex. When in doubt, refer to the error messages the SDK raises. It may take a few tries to get the right combination of arguments.

### Form Record

Below are the possible arguments for creating a form record:

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```name``` | ```str``` | Auth record name | ✅ |
| ```recordType``` | ```str``` = ```formRecord``` | Record type | ✅ |
| ```subType``` | ```Literal["STANDARD", "CUSTOM", "SELENIUM"]``` | Record sub-type | ✅ |
| ```fields``` | ```list[dict["name": str, "value": str]]``` | List of fields | ✅ |
| ```sslOnly``` | ```bool``` | If the authentication record should only be sent on a secure connection | ❌ |
| ```authVault``` | ```bool``` | If the authentication record should be stored in the auth vault | ❌ |
| ```seleniumCreds``` | ```bool``` | If the authentication record is for a Selenium script | ❌ |
| ```seleniumScript``` | ```dict[str, str]```, like: ```{"name": "my_script", "data": <script_as_XML_string>}``` | Selenium script data | ❌ |
| ```tags``` | ```list[Union[str, int]]``` | List of tag IDs | ❌ |
| ```comments``` | ```list[str]``` | List of comments | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import create_authentication_record

auth = BasicAuth(<username>, <password>)

# EXAMPLE formRecord with basic username/password fields:

new_auth_record = create_authentication_record(
    auth,
    name="My New Auth Record",
    recordType="formRecord",
    subType="STANDARD",
    fields=[
        {"name": "username", "value": "my_username"},
        {"name": "password", "value": "my_password"},
    ],
    tags=[12345, 54321],
    comments=["This is my new auth record"],
    sslOnly=True,
)

# SELENIUM EXAMPLE:
new_auth_record = create_authentication_record(
    auth,
    name="My Selenium Auth Record",
    recordType="formRecord",
    subType="SELENIUM",
    fields=[
        {"name": "username", "value": "my_username"},
        {"name": "password", "value": "my_password"},
    ],
    seleniumCreds=True,
    seleniumScript={"name": "my_script", "data": """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head profile="http://selenium-ide.openqa.org/profiles/test-case">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<link rel="selenium.base" href="https://community.qualys.com/" />
<title>seleniumScriptOK</title>
</head>
<body>
<table cellpadding="1" cellspacing="1" border="1">..."""},
)
```

### Server Record

Below are the possible arguments for creating a server record:

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```name``` | ```str``` | Auth record name | ✅ |
| ```recordType``` | ```str``` = ```serverRecord``` | Record type | ✅ |
| ```sslOnly``` | ```bool``` | If the authentication record should only be sent on a secure connection | ❌ |
| ```certificate``` | ```dict["name": str, "contents": str, "passphrase": str]``` | Certificate data | ❌ |
| ```tags``` | ```list[Union[str, int]]``` | List of tag IDs | ❌ |
| ```comments``` | ```list[str]``` | List of comments | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import create_authentication_record

auth = BasicAuth(<username>, <password>)

# EXAMPLE serverRecord with a certificate:
new_auth_record = create_authentication_record(
    auth,
    name="My New Server Auth Record",
    recordType="serverRecord",
    certificate={"name": "my_cert", "contents": "-----BEGIN CERTIFICATE-----\nMIID...-----END CERTIFICATE-----", "passphrase": "my_passphrase"},
    tags=[12345, 54321],
    comments=["This is my new server auth record"],
    sslOnly=True,
)
```

### OAuth2 Record

Below are the possible arguments for creating an OAuth2 record:

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```name``` | ```str``` | Auth record name | ✅ |
| ```recordType``` | ```str``` = ```oauth2Record``` | Record type | ✅ |
| ```subType``` | ```Literal["AUTH_CODE", "IMPLICIT", "PASSWORD", "CLIENT_CREDS"]``` | Record sub-type | ✅ |
| ```clientId``` | ```str``` | OAuth2 client ID | ✅ |
| ```clientSecret``` | ```str``` | OAuth2 client secret | ✅ |
| ```accessTokenUrl``` | ```str``` | OAuth2 access token URL | ✅ |
| ```scope``` | ```str``` | OAuth2 scope | ❌ |
| ```accessTokenExpiredMsgPattern``` | ```str``` | OAuth2 access token expired message pattern | ❌ |
| ```seleniumCreds``` | ```bool``` | If the authentication record is for a Selenium script | ❌ |
| ```seleniumScript``` | ```dict[str, str]```, like: ```{"name": "my_script", "data": <script_as_XML_string>}``` | Selenium script data | ❌ |
| ```tags``` | ```list[Union[str, int]]``` | List of tag IDs | ❌ |
| ```comments``` | ```list[str]``` | List of comments | ❌ |


```py
from qualysdk import BasicAuth
from qualysdk.was import create_authentication_record

auth = BasicAuth(<username>, <password>)

# EXAMPLE OAuth2 record:
new_auth_record = create_authentication_record(
    auth,
    name="My New OAuth2 Auth Record",
    recordType="oauth2Record",
    subType="CLIENT_CREDS",
    clientId="my_client_id",
    clientSecret="my_client_secret",
    accessTokenUrl="https://example.com/token",
    scope="scope",
    tags=[12345, 54321],
    comments=["This is my new OAuth2 auth record"],
)
```

## Delete Authentication Record API

```delete_authentication_record``` deletes an authentication record in the subscription.

Returns a list of auth record IDs that were deleted as a dictionary: ```{"id": <id>}```

>**Head's Up!:** Using this API may only remove the WAS-specific asset in the subscription. It may still be active in other Qualys modules, such as Global AssetView's web application view.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ```Union[str, int]``` | Auth record ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Auth record name | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the name filter | ❌ |
| ```tags``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tags filter | ❌ |
| ```tags_name``` | ```str``` | Tag name | ❌ |
| ```tags_name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | Operator for the tag name filter | ❌ |
| ```tags_id``` | ```Union[str, int]``` | Tag ID | ❌ |
| ```tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the tag ID filter | ❌ |
| ```createdDate``` | ```str``` | Date created | ❌ |
| ```createdDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the created date filter | ❌ |
| ```updatedDate``` | ```str``` | Date updated | ❌ |
| ```updatedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the updated date filter | ❌ |
| ```lastScan_date``` | ```str``` | Date of the last scan in UTC date/time format | ❌ |
| ```lastScan_date_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the lastScan_date filter | ❌ |
| ```lastScan_authStatus``` | ```Literal["NONE", "NOT_USED", "PARTIAL", "FAILED", "SUCCESSFUL"]``` | Status of the last scan | ❌ |
| ```lastScan_authStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the lastScan_authStatus filter | ❌ |
| ```isUsed``` | ```bool``` | If the auth record is in use | ❌ |
| ```contents``` | ```Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]``` | Auth record type | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import delete_authentication_record

auth = BasicAuth(<username>, <password>)

# Delete an auth record by ID:
delete_authentication_record(auth, id=12345678)

# Delete all auth record with the PURGE tag:
delete_authentication_record(auth, tags_name="PURGE", tags_name_operator="EQUALS")
>>>[{"id": 12345678}, {"id": 98765432}, ...]
```

## Count Findings API

```count_findings``` returns the number of findings in the subscription that match the given kwargs.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ```Union[str, int]``` | Finding ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```uniqueId``` | ```str``` | Unique ID of the finding | ❌ |
| ```qid``` | ```int``` | Qualys ID of the finding | ❌ |
| ```qid_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the QID filter | ❌ |
| ```name``` | ```str``` | Name of the finding | ❌ |
| ```name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the name filter | ❌ |
| ```type``` | ```Literal["VULNERABILITY", "SENSITIVE_CONTENT", "INFORMATION_GATHERED"]``` | Type of the finding | ❌ |
| ```type_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the type filter | ❌ |
| ```url``` | ```str``` | URL of the finding's webapp | ❌ |
| ```url_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the URL filter | ❌ |
| ```webApp_tags_id``` | ```int``` | A tag ID on the webapp | ❌ |
| ```webApp_tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_tags_id filter | ❌ |
| ```webApp_tags_name``` | ```str``` | A tag name on the webapp | ❌ |
| ```webApp_tags_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_tags_name filter | ❌ |
| ```status``` | ```Literal["NEW", "ACTIVE", "REOPENED", "PROTECTED", "FIXED"]``` | Status of the finding | ❌ |
| ```status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the status filter | ❌ |
| ```patch``` | ```int``` | Patch ID for WAF module | ❌ |
| ```patch_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the patch filter | ❌ |
| ```webApp_id``` | ```int``` | Webapp ID | ❌ |
| ```webApp_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_id filter | ❌ |
| ```webApp_name``` | ```str``` | Webapp name | ❌ |
| ```webApp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_name filter | ❌ |
| ```severity``` | ```Literal[1, 2, 3, 4, 5]``` | Severity of the finding | ❌ |
| ```severity_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the severity filter | ❌ |
| ```externalRef``` | ```str``` | External reference of the finding | ❌ |
| ```externalRef_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the externalRef filter | ❌ |
| ```ignoredDate``` | ```str``` | Date the finding was ignored | ❌ |
| ```ignoredDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ignoredDate filter | ❌ |
| ```ignoredReason``` | ```Literal["FALSE_POSITIVE", "RISK_ACCEPTED", "NOT_APPLICABLE"]``` | Reason the finding was ignored | ❌ |
| ```ignoredReason_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the ignoredReason filter | ❌ |
| ```group``` | ```Literal["XSS", "SQL", "INFO", "PATH", "CC", "SSN_US", "CUSTOM"]``` | Group of the finding | ❌ |
| ```group_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the group filter | ❌ |
| ```owasp_name``` | ```str``` | OWASP name of the finding | ❌ |
| ```owasp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the owasp_name filter | ❌ |
| ```owasp_code``` | ```int``` | OWASP code of the finding | ❌ |
| ```owasp_code_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the owasp_code filter | ❌ |
| ```wasc_name``` | ```str``` | WASC name of the finding | ❌ |
| ```wasc_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the wasc_name filter | ❌ |
| ```wasc_code``` | ```int``` | WASC code of the finding | ❌ |
| ```wasc_code_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the wasc_code filter | ❌ |
| ```cwe_id``` | ```int``` | CWE ID of the finding | ❌ |
| ```cwe_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the cwe_id filter | ❌ |
| ```firstDetectedDate``` | ```str``` | Date the finding was first detected | ❌ |
| ```firstDetectedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the firstDetectedDate filter | ❌ |
| ```lastDetectedDate``` | ```str``` | Date the finding was last detected | ❌ |
| ```lastDetectedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the lastDetectedDate filter | ❌ |
| ```lastTestedDate``` | ```str``` | Date the finding was last tested | ❌ |
| ```lastTestedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the lastTestedDate filter | ❌ |
| ```timesDetected``` | ```int``` | Number of times the finding was detected | ❌ |
| ```timesDetected_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the timesDetected filter | ❌ |
| ```fixedDate``` | ```str``` | Date the finding was fixed | ❌ |
| ```fixedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the fixedDate filter | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import count_findings

auth = BasicAuth(<username>, <password>)

# Get the number of findings with a severity of 5:
count = count_findings(auth, severity=5)

# Get XSS findings that are severity 4 or 5,
# and have been detected 5+ times
# on assets with the PROD tag:

count = count_findings(
    auth,
    group="XSS",
    severity="4,5",
    severity_operator="IN",
    timesDetected=4,
    timesDetected_operator="GREATER",
    webApp_tags_name="PROD",
)
>>> 5
```

## List Findings API

```get_findings``` returns a list of findings in the subscription that match the given kwargs.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to return. If 'all', returns all pages | ❌ |
| ```verbose``` | ```bool``` | Whether to return verbose output | ❌ |
| ```id``` | ```Union[str, int]``` | Finding ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```uniqueId``` | ```str``` | Unique ID of the finding | ❌ |
| ```qid``` | ```int``` | Qualys ID of the finding | ❌ |
| ```qid_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the QID filter | ❌ |
| ```name``` | ```str``` | Name of the finding | ❌ |
| ```name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the name filter | ❌ |
| ```type``` | ```Literal["VULNERABILITY", "SENSITIVE_CONTENT", "INFORMATION_GATHERED"]``` | Type of the finding | ❌ |
| ```type_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the type filter | ❌ |
| ```url``` | ```str``` | URL of the finding's webapp | ❌ |
| ```url_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the URL filter | ❌ |
| ```webApp_tags_id``` | ```int``` | A tag ID on the webapp | ❌ |
| ```webApp_tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_tags_id filter | ❌ |
| ```webApp_tags_name``` | ```str``` | A tag name on the webapp | ❌ |
| ```webApp_tags_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_tags_name filter | ❌ |
| ```status``` | ```Literal["NEW", "ACTIVE", "REOPENED", "PROTECTED", "FIXED"]``` | Status of the finding | ❌ |
| ```status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the status filter | ❌ |
| ```patch``` | ```int``` | Patch ID for WAF module | ❌ |
| ```patch_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the patch filter | ❌ |
| ```webApp_id``` | ```int``` | Webapp ID | ❌ |
| ```webApp_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_id filter | ❌ |
| ```webApp_name``` | ```str``` | Webapp name | ❌ |
| ```webApp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_name filter | ❌ |
| ```severity``` | ```Literal[1, 2, 3, 4, 5]``` | Severity of the finding | ❌ |
| ```severity_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the severity filter | ❌ |
| ```externalRef``` | ```str``` | External reference of the finding | ❌ |
| ```externalRef_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the externalRef filter | ❌ |
| ```ignoredDate``` | ```str``` | Date the finding was ignored | ❌ |
| ```ignoredDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ignoredDate filter | ❌ |
| ```ignoredReason``` | ```Literal["FALSE_POSITIVE", "RISK_ACCEPTED", "NOT_APPLICABLE"]``` | Reason the finding was ignored | ❌ |
| ```ignoredReason_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the ignoredReason filter | ❌ |
| ```group``` | ```Literal["XSS", "SQL", "INFO", "PATH", "CC", "SSN_US", "CUSTOM"]``` | Group of the finding | ❌ |
| ```group_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the group filter | ❌ |
| ```owasp_name``` | ```str``` | OWASP name of the finding | ❌ |
| ```owasp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the owasp_name filter | ❌ |
| ```owasp_code``` | ```int``` | OWASP code of the finding | ❌ |
| ```owasp_code_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the owasp_code filter | ❌ |
| ```wasc_name``` | ```str``` | WASC name of the finding | ❌ |
| ```wasc_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the wasc_name filter | ❌ |
| ```wasc_code``` | ```int``` | WASC code of the finding | ❌ |
| ```wasc_code_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the wasc_code filter | ❌ |
| ```cwe_id``` | ```int``` | CWE ID of the finding | ❌ |
| ```cwe_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the cwe_id filter | ❌ |
| ```firstDetectedDate``` | ```str``` | Date the finding was first detected | ❌ |
| ```firstDetectedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the firstDetectedDate filter | ❌ |
| ```lastDetectedDate``` | ```str``` | Date the finding was last detected | ❌ |
| ```lastDetectedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the lastDetectedDate filter | ❌ |
| ```lastTestedDate``` | ```str``` | Date the finding was last tested | ❌ |
| ```lastTestedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the lastTestedDate filter | ❌ |
| ```timesDetected``` | ```int``` | Number of times the finding was detected | ❌ |
| ```timesDetected_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the timesDetected filter | ❌ |
| ```fixedDate``` | ```str``` | Date the finding was fixed | ❌ |
| ```fixedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the fixedDate filter | ❌ |


```py
from qualysdk import BasicAuth
from qualysdk.was import get_findings

auth = BasicAuth(<username>, <password>)

# Get all findings, with all details:
findings = get_findings(auth, verbose=True)
>>>[
    WASFinding(
        id=123456789, 
        uniqueId='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 
        qid=86002, 
        detectionScore=0, 
        name='SSL Certificate - Information', 
        type='INFORMATION_GATHERED', 
        potential=True, 
        findingType='QUALYS', 
        severity=1,
        ...
    ),
    ...
]

# Get all XSS & SQL findings 
# with a severity of 4 or 5
# that have been detected 
# 5+ times on assets with the PROD tag:
findings = get_findings(
    auth,
    group="XSS,SQL",
    group_operator="IN",
    severity="4,5",
    severity_operator="IN",
    timesDetected=4,
    timesDetected_operator="GREATER",
    webApp_tags_name="PROD",
)
```

## Get Finding Details API

```get_finding_details``` returns the details of a single finding in the subscription.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```findingId``` | ```Union[str, int]``` | Finding # or unique ID | ✅ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_finding_details

auth = BasicAuth(<username>, <password>)
finding = get_finding_details(auth, findingId=123456789)
finding2 = get_finding_details(auth, findingId="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
```

## Get Findings Verbose API

```get_findings_verbose``` returns a list of findings in the subscription with all attributes. This method uses threading to speed up the process. Number of threads can be set with the ```thread_count``` parameter.

>**Head's Up!:** Unlike the other ```get_<thing>_verbose``` methods, this method is not always faster than the non-verbose version. It is recommended to use the non-verbose version unless you need data specifically related to SSL/TLS certificates.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```thread_count``` | ```int``` | Number of threads to use for the request | ❌ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to return. If 'all', returns all pages | ❌ |
| ```verbose``` | ```bool``` | Whether to return verbose output | ❌ |
| ```id``` | ```Union[str, int]``` | Finding ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```uniqueId``` | ```str``` | Unique ID of the finding | ❌ |
| ```qid``` | ```int``` | Qualys ID of the finding | ❌ |
| ```qid_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the QID filter | ❌ |
| ```name``` | ```str``` | Name of the finding | ❌ |
| ```name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the name filter | ❌ |
| ```type``` | ```Literal["VULNERABILITY", "SENSITIVE_CONTENT", "INFORMATION_GATHERED"]``` | Type of the finding | ❌ |
| ```type_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the type filter | ❌ |
| ```url``` | ```str``` | URL of the finding's webapp | ❌ |
| ```url_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the URL filter | ❌ |
| ```webApp_tags_id``` | ```int``` | A tag ID on the webapp | ❌ |
| ```webApp_tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_tags_id filter | ❌ |
| ```webApp_tags_name``` | ```str``` | A tag name on the webapp | ❌ |
| ```webApp_tags_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_tags_name filter | ❌ |
| ```status``` | ```Literal["NEW", "ACTIVE", "REOPENED", "PROTECTED", "FIXED"]``` | Status of the finding | ❌ |
| ```status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the status filter | ❌ |
| ```patch``` | ```int``` | Patch ID for WAF module | ❌ |
| ```patch_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the patch filter | ❌ |
| ```webApp_id``` | ```int``` | Webapp ID | ❌ |
| ```webApp_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_id filter | ❌ |
| ```webApp_name``` | ```str``` | Webapp name | ❌ |
| ```webApp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_name filter | ❌ |
| ```severity``` | ```Literal[1, 2, 3, 4, 5]``` | Severity of the finding | ❌ |
| ```severity_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the severity filter | ❌ |
| ```externalRef``` | ```str``` | External reference of the finding | ❌ |
| ```externalRef_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the externalRef filter | ❌ |
| ```ignoredDate``` | ```str``` | Date the finding was ignored | ❌ |
| ```ignoredDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ignoredDate filter | ❌ |
| ```ignoredReason``` | ```Literal["FALSE_POSITIVE", "RISK_ACCEPTED", "NOT_APPLICABLE"]``` | Reason the finding was ignored | ❌ |
| ```ignoredReason_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the ignoredReason filter | ❌ |
| ```group``` | ```Literal["XSS", "SQL", "INFO", "PATH", "CC", "SSN_US", "CUSTOM"]``` | Group of the finding | ❌ |
| ```group_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the group filter | ❌ |
| ```owasp_name``` | ```str``` | OWASP name of the finding | ❌ |
| ```owasp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the owasp_name filter | ❌ |
| ```owasp_code``` | ```int``` | OWASP code of the finding | ❌ |
| ```owasp_code_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the owasp_code filter | ❌ |
| ```wasc_name``` | ```str``` | WASC name of the finding | ❌ |
| ```wasc_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the wasc_name filter | ❌ |
| ```wasc_code``` | ```int``` | WASC code of the finding | ❌ |
| ```wasc_code_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the wasc_code filter | ❌ |
| ```cwe_id``` | ```int``` | CWE ID of the finding | ❌ |
| ```cwe_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the cwe_id filter | ❌ |
| ```firstDetectedDate``` | ```str``` | Date the finding was first detected | ❌ |
| ```firstDetectedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the firstDetectedDate filter | ❌ |
| ```lastDetectedDate``` | ```str``` | Date the finding was last detected | ❌ |
| ```lastDetectedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the lastDetectedDate filter | ❌ |
| ```lastTestedDate``` | ```str``` | Date the finding was last tested | ❌ |
| ```lastTestedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the lastTestedDate filter | ❌ |
| ```timesDetected``` | ```int``` | Number of times the finding was detected | ❌ |
| ```timesDetected_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the timesDetected filter | ❌ |
| ```fixedDate``` | ```str``` | Date the finding was fixed | ❌ |
| ```fixedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the fixedDate filter | ❌ |


```py
from qualysdk import BasicAuth
from qualysdk.was import get_findings_verbose

auth = BasicAuth(<username>, <password>)
findings = get_findings_verbose(auth, severity=5)
```

## Count Scans API

```count_scans``` returns the number of scans in the subscription that match given kwargs.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ```Union[str, int]``` | Scan ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Scan name | ❌ |
| ```name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the name filter | ❌ |
| ```reference``` | ```str``` | Scan reference | ❌ |
| ```reference_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the reference filter | ❌ |
| ```type``` | ```Literal["DISCOVERY", "VULNERABILITY"]``` | Scan type | ❌ |
| ```type_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the type filter | ❌ |
| ```mode``` | ```Literal["ONDEMAND", "SCHEDULED", "API"]``` | Scan mode | ❌ |
| ```mode_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the mode filter | ❌ |
| ```status``` | ```Literal["SUBMITTED", "RUNNING", "FINISHED", "ERROR", "CANCELLED", "PROCESSING"]``` | Scan status | ❌ |
| ```status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the status filter | ❌ |
| ```webApp_id``` | ```int``` | Webapp ID | ❌ |
| ```webApp_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_id filter | ❌ |
| ```webApp_name``` | ```str``` | Webapp name | ❌ |
| ```webApp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_name filter | ❌ |
| ```webApp_tags_id``` | ```int``` | Webapp tag ID | ❌ |
| ```webApp_tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_tags_id filter | ❌ |
| ```resultsStatus``` | ```Literal["NOT_USED", "TO_BE_PROCESSED", "NO_HOST_ALIVE", "NO_WEB_SERVICE", "SERVICE_ERROR", "TIME_LIMIT_REACHED", "SCAN_INTERNAL_ERROR", "SCAN_RESULTS_INVALID", "SUCCESSFUL", "PROCESSING", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "SUBMITTED", "RUNNING", "CANCELED", "CANCELING", "ERROR", "DELETED", "CANCELED_WITH_RESULTS"]``` | Results status | ❌ |
| ```resultsStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the resultsStatus filter | ❌ |
| ```authStatus``` | ```Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]``` | Authentication status | ❌ |
| ```authStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the authStatus filter | ❌ |
| ```launchedDate``` | ```str``` | Scan launch date in UTC: YYYY-MM-DDTHH:MM:SSZ | ❌ |
| ```launchedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the launchedDate filter | ❌ |


```py
from qualysdk import BasicAuth
from qualysdk.was import count_scans

auth = BasicAuth(<username>, <password>)
count = count_scans(
    auth,
    type="VULNERABILITY",
    mode="API,SCHEDULED",
    mode_operator="IN",
    status="RUNNING,FINISHED",
    status_operator="IN",
    webApp_tags_id=123456789,
    authStatus="NOT_USED"    
)
>>> 5
```

## List Scans API

```get_scans``` returns a list of scans in the subscription that match given kwargs.
| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to return. If 'all', returns all pages | ❌ |
| ```id``` | ```Union[str, int]``` | Scan ID | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | Operator for the ID filter | ❌ |
| ```name``` | ```str``` | Scan name | ❌ |
| ```name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the name filter | ❌ |
| ```reference``` | ```str``` | Scan reference | ❌ |
| ```reference_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the reference filter | ❌ |
| ```type``` | ```Literal["DISCOVERY", "VULNERABILITY"]``` | Scan type | ❌ |
| ```type_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the type filter | ❌ |
| ```mode``` | ```Literal["ONDEMAND", "SCHEDULED", "API"]``` | Scan mode | ❌ |
| ```mode_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the mode filter | ❌ |
| ```status``` | ```Literal["SUBMITTED", "RUNNING", "FINISHED", "ERROR", "CANCELLED", "PROCESSING"]``` | Scan status | ❌ |
| ```status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the status filter | ❌ |
| ```webApp_id``` | ```int``` | Webapp ID | ❌ |
| ```webApp_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_id filter | ❌ |
| ```webApp_name``` | ```str``` | Webapp name | ❌ |
| ```webApp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_name filter | ❌ |
| ```webApp_tags_id``` | ```int``` | Webapp tag ID | ❌ |
| ```webApp_tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_tags_id filter | ❌ |
| ```resultsStatus``` | ```Literal["NOT_USED", "TO_BE_PROCESSED", "NO_HOST_ALIVE", "NO_WEB_SERVICE", "SERVICE_ERROR", "TIME_LIMIT_REACHED", "SCAN_INTERNAL_ERROR", "SCAN_RESULTS_INVALID", "SUCCESSFUL", "PROCESSING", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "SUBMITTED", "RUNNING", "CANCELED", "CANCELING", "ERROR", "DELETED", "CANCELED_WITH_RESULTS"]``` | Results status | ❌ |
| ```resultsStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the resultsStatus filter | ❌ |
| ```authStatus``` | ```Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]``` | Authentication status | ❌ |
| ```authStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the authStatus filter | ❌ |
| ```launchedDate``` | ```str``` | Scan launch date in UTC: YYYY-MM-DDTHH:MM:SSZ | ❌ |
| ```launchedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the launchedDate filter | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_scans

auth = BasicAuth(<username>, <password>)
scans = get_scans(
    auth,
    type="VULNERABILITY",
    mode="API,SCHEDULED",
    mode_operator="IN",
    status="RUNNING,FINISHED",
    status_operator="IN",
    webApp_tags_id=123456789,
    authStatus="NOT_USED"    
)
>>>[
    WASScan(
        id=123456789, 
        name='Test Scan', 
        reference='test_scan', 
        type='VULNERABILITY', 
        mode='API', 
        status='RUNNING', 
        launchedDate='2023-10-01T12:00:00Z',
        ...
    ),
    ...
]
```

## Get Scan Details API

```get_scan_details``` returns the details of a single scan in the subscription.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```scanId``` | ```Union[str, int]``` | Scan # | ✅ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_scan_details, get_scans

auth = BasicAuth(<username>, <password>)

# Get some scans:
scans = get_scans(auth, type="VULNERABILITY")

# Get details for the first scan:
scan = get_scan_details(auth, scanId=scans[0].id)
>>> WASScan(
    id=123456789, 
    name='Test Scan', 
    reference='test_scan', 
    type='VULNERABILITY', 
    mode='API', 
    status='RUNNING', 
    launchedDate='2023-10-01T12:00:00Z',
    ...
)
```

## Get Scans Verbose API

```get_scans_verbose``` combines the ```get_scan_details``` and ```get_scans``` methods to return a list of scans with all attributes. This method uses threading to speed up the process. Number of threads can be set with the ```thread_count``` parameter.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```thread_count``` | ```int=5``` | Number of threads to use for the request | ❌ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to return. If 'all', returns all pages | ❌ |
| ```type``` | ```Literal["DISCOVERY", "VULNERABILITY"]``` | Scan type | ❌ |
| ```type_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the type filter | ❌ |
| ```mode``` | ```Literal["ONDEMAND", "SCHEDULED", "API"]``` | Scan mode | ❌ |
| ```mode_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the mode filter | ❌ |
| ```status``` | ```Literal["SUBMITTED", "RUNNING", "FINISHED", "ERROR", "CANCELLED", "PROCESSING"]``` | Scan status | ❌ |
| ```status_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the status filter | ❌ |
| ```webApp_id``` | ```int``` | Webapp ID | ❌ |
| ```webApp_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_id filter | ❌ |
| ```webApp_name``` | ```str``` | Webapp name | ❌ |
| ```webApp_name_operator``` | ```Literal["EQUALS", "NOT EQUALS", "CONTAINS"]``` | Operator for the webApp_name filter | ❌ |
| ```webApp_tags_id``` | ```int``` | Webapp tag ID | ❌ |
| ```webApp_tags_id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the webApp_tags_id filter | ❌ |
| ```resultsStatus``` | ```Literal["NOT_USED", "TO_BE_PROCESSED", "NO_HOST_ALIVE", "NO_WEB_SERVICE", "SERVICE_ERROR", "TIME_LIMIT_REACHED", "SCAN_INTERNAL_ERROR", "SCAN_RESULTS_INVALID", "SUCCESSFUL", "PROCESSING", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "SUBMITTED", "RUNNING", "CANCELED", "CANCELING", "ERROR", "DELETED", "CANCELED_WITH_RESULTS"]``` | Results status | ❌ |
| ```resultsStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the resultsStatus filter | ❌ |
| ```authStatus``` | ```Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]``` | Authentication status | ❌ |
| ```authStatus_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | Operator for the authStatus filter | ❌ |
| ```launchedDate``` | ```str``` | Scan launch date in UTC: YYYY-MM-DDTHH:MM:SSZ | ❌ |
| ```launchedDate_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]``` | Operator for the launchedDate filter | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_scans_verbose

auth = BasicAuth(<username>, <password>)
scans = get_scans_verbose(auth, type="VULNERABILITY")
>>>[
    WASScan(
        id=123456789, 
        name='Test Scan', 
        reference='test_scan', 
        type='VULNERABILITY', 
        mode='API', 
        status='RUNNING', 
        launchedDate='2023-10-01T12:00:00Z',
        ...
    ),
    ...
]
```

## Launch Scan API

```launch_scan``` launches a scan on webapps either by specifying webapp IDs or tags.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```name``` | ```str``` | Name of the scan | ✅ |
| ```scan_type``` | ```Literal["DISCOVERY", "VULNERABILITY"]``` | Scan type | ✅ |
| ```profile_id``` | ```int``` | Scan profile ID | ✅ |
| ```web_app_ids``` | ```Union[str, int, list[str, int]]``` | Webapp ID(s) to scan | ⚠️ required if `included_tag_ids` not specified |
| ```included_tag_ids``` | ```Union[str, int, list[str, int]]``` | Tag ID(s) to scan | ⚠️ required if `web_app_ids` not specified |
| ```included_tag_options``` | ```Literal["ALL", "ANY"]``` | Whether to scan all or any tags | ❌ |
| ```scanner_appliance_type``` | ```Literal["EXTERNAL", "INTERNAL"]``` | Scanner appliance type | ❌ |
| ```auth_record_option``` | ```Union[str, int]``` | Authentication record ID | ❌ |
| ```profile_option``` | ```Literal["DEFAULT", "ANY", "ALL"]``` | Profile option | ❌ |
| ```scanner_option``` | ```Union[str, int]``` | Scanner appliance ID | ❌ |
| ```send_mail``` | ```bool``` | Whether to send an email | ❌ |
| ```send_one_mail``` | ```bool``` | Whether to send one email | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import launch_scan

auth = BasicAuth(<username>, <password>)

# Launch a scan on a single webapp:
launch_scan(
    auth,
    name="Test Scan",
    scan_type="VULNERABILITY",
    profile_id=123456789,
    web_app_ids=123456789
)
>>> 123456789 # Scan ID

# Launch a scan on all webapps with a specific tag:
launch_scan(
    auth,
    name="Test Scan",
    scan_type="DISCOVERY",
    profile_id=123456789,
    included_tag_ids=123456789
)
>>> 123456789
```

## Cancel Scan API

```cancel_scan``` cancels a scan, optionally retaining the results up to the point of cancellation.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```scanId``` | ```Union[str, int]``` | Scan ID | ✅ |
| ```retain_results``` | ```bool``` | Whether to retain results. Defaults to `False` | ❌ |

```py
from qualysdk import BasicAuth
from qualysdk.was import cancel_scan, get_scans

auth = BasicAuth(<username>, <password>)

# Find some scans to cancel:
scans = get_scan_details(auth, status="RUNNING", type="VULNERABILITY")

# Cancel the scan(s), saving the results so far:
for scan in scans:
    cancel_scan(auth, scan.id, retain_results=True)
>>>"SUCCESS"
```

## Get Scan Status API

```get_scan_status``` returns the status of a scan as well as the status/result of trying to authenticate to the target webapp.

| Parameter | Possible Values | Description | Required |
| -- | -- | -- | -- |
| ```auth``` | ```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```scanId``` | ```Union[str, int]``` | Scan ID | ✅ |

```py
from qualysdk import BasicAuth
from qualysdk.was import get_scan_status

auth = BasicAuth(<username>, <password>)
scanId = 123456789

status = get_scan_status(auth, scanId)
>>>{
  "@{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation": "https://qualysapi.qg3.apps.qualys.com/qps/xsd/3.0/was/wasscan.xsd",
  "responseCode": "SUCCESS",
  "count": "1",
  "data": {
    "WasScan": {
      "id": "123456789",
      "status": "RUNNING",
      "consolidatedStatus": "RUNNING"
    }
  }
}
```

## ```qualysdk-was``` CLI tool

The ```qualysdk-was``` CLI tool is a command-line interface for the WAS portion of the SDK. It allows you to quickly pull down results from WAS APIs and save them to an XLSX file.

### Usage

```bash
usage: qualysdk-was [-h] -u USERNAME -p PASSWORD [-P {qg1,qg2,qg3,qg4}] {get_findings,get_scans} ...

CLI script to quickly perform Web Application Scanning (WAS) operations using qualysdk

positional arguments:
  {get_findings,get_scans}
                        Action to perform
    get_findings        Get a list of WAS findings.
    get_scans           Get a list of WAS scans.

options:
  -h, --help            show this help message and exit
  -u, --username USERNAME
                        Qualys username
  -p, --password PASSWORD
                        Qualys password
  -P, --platform {qg1,qg2,qg3,qg4}
                        Qualys platform
```

### Get Findings

```bash
usage: qualysdk-was get_findings [-h] [-o OUTPUT] [--kwarg key value]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output xlsx file to write results to
  --kwarg key value     Specify a keyword argument to pass to the get_findings function. Can be used multiple times

# Example with a few kwargs:
qualysdk-was -u <username> -p <password> -P qg1 get_findings --kwarg verbose true --kwarg group XSS --output xss_findings.xlsx
>>>Data written to xss_findings.xlsx.
```

### Get Scans

```bash
usage: qualysdk-was get_scans [-h] [-o OUTPUT] [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output xlsx file to write results to
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```