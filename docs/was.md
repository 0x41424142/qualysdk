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

