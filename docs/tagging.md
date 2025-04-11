# Tagging APIs

Tagging APIs return data on Qualys tags and tag categories.

After running:
```py
from qualysdk.tagging import *
```
You can use any of the endpoints currently supported:

## Tagging Endpoints

|API Call| Description |
|--|--|
| ```count_tags``` | Returns the number of tags in the subscription that match given kwargs. |
| ```get_tags``` | Returns a list of tags in the subscription that match given kwargs. |
| ```get_tag_details``` | Returns details about a single tag. |


## Count Tags API

```count_tags``` returns the number of tags in the subscription that match the given kwargs.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ``` Union[str, int]``` | The ID(s) of a tag to return | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | The operator to use for the id | ❌ |
| ```name``` | ```str``` | The name of a tag to return | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | The operator to use for the name | ❌ |
| ```parent``` | ```Union[str, int]``` | The ID of a parent tag to return | ❌ |
| ```parent_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | The operator to use for the parent | ❌ |
| ```ruleType``` | ```Literal["GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]``` | The type of rule the tag uses | ❌ |
| ```ruleType_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | The operator to use for the ruleType | ❌ |
| ```provider``` | ```Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]``` | The cloud provider the tag is for | ❌ |
| ```provider_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | The operator to use for the provider | ❌ |
| ```color``` | ```str``` | The color of the tag as a hex code, such as #FFFFFF | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.tagging import count_tags

auth = BasicAuth(<username>, <password>, platform='qg1')

# Get the total count of tags:
tags = count_tags(auth)
>>> 1234

# get all tags that have a name containing "prod"
tags = count_tags(
    auth, 
    name='prod', 
    name_operator='CONTAINS'
)
>>> 123

# get all tags that have a name containing "dev"
# and are for AWS or Azure:

tags = count_tags(
    auth, 
    name='dev', 
    name_operator='CONTAINS', 
    provider='AWS,AZURE', 
    provider_operator='IN'
)
>>> 12
```

## Get Tags API

```get_tags``` returns a list of tags in the subscription that match the given kwargs.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```id``` | ``` Union[str, int]``` | The ID(s) of a tag to return | ❌ |
| ```id_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | The operator to use for the id | ❌ |
| ```name``` | ```str``` | The name of a tag to return | ❌ |
| ```name_operator``` | ```Literal["CONTAINS", "EQUALS", "NOT EQUALS"]``` | The operator to use for the name | ❌ |
| ```parent``` | ```Union[str, int]``` | The ID of a parent tag to return | ❌ |
| ```parent_operator``` | ```Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]``` | The operator to use for the parent | ❌ |
| ```ruleType``` | ```Literal["GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]``` | The type of rule the tag uses | ❌ |
| ```ruleType_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | The operator to use for the ruleType | ❌ |
| ```provider``` | ```Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]``` | The cloud provider the tag is for | ❌ |
| ```provider_operator``` | ```Literal["EQUALS", "NOT EQUALS", "IN"]``` | The operator to use for the provider | ❌ |
| ```color``` | ```str``` | The color of the tag as a hex code, such as #FFFFFF | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.tagging import get_tags
auth = BasicAuth(<username>, <password>, platform='qg1')

# Get all tags:
tags = get_tags(auth)

# Get all tags that have a name containing "prod"
tags = get_tags(
    auth, 
    name='prod', 
    name_operator='CONTAINS'
)
>>>[
  Tag(
    id=1234,
    name='prod',
    parent=None,
    ruleType='GROOVY',
    provider=None,
    color='#FF0000'
  ),
  ...
]
```

## Get Tag Details API

```get_tag_details``` returns details about a single tag.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```tag_id``` | ``` Union[str, int]``` | The ID(s) of a tag to return | ✅ |

```py
from qualysdk import BaseList
from qualysdk.auth import BasicAuth
from qualysdk.tagging import get_tags, get_tag_details

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get some tags:
tags = get_tags(
  auth,
  name="Production_",
  name_operator='CONTAINS",
)
# for each of the tags, get their details:
tag_list = BaseList()
for tag in tags:
  details = get_tag_details(
    auth,
    tag.id
  )
  tag_list.append(details)
>>>[
  Tag(
    id=123456789, 
    name='Production_on_prem_servers', 
    ...
  ),
  Tag(
    id=987654321, 
    name='Production_cloud_servers',
  ),
  ...
]

```

## ```qualysdk-tag``` CLI tool

The ```qualysdk-tag``` CLI tool is a command-line interface for the tagging portion of the SDK. It allows you to quickly pull down results from tagging APIs and save them to an XLSX file and optionally print to stdout.

### Usage

```bash
usage: qualysdk-tag [-h] -u USERNAME -p PASSWORD [-P {qg1,qg2,qg3,qg4}] {count_tags,get_tags,get_tag_details} ...

CLI script to quickly perform tagging operations using qualysdk

positional arguments:
  {count_tags,get_tags,get_tag_details}
                        Action to perform
    count_tags          Count how many tags match the given criteria.
    get_tags            Get the tags that match the given criteria.
    get_tag_details     Get all details of a single tag.

options:
  -h, --help            show this help message and exit
  -u, --username USERNAME
                        Qualys username
  -p, --password PASSWORD
                        Qualys password
  -P, --platform {qg1,qg2,qg3,qg4}
                        Qualys platform
```

### Count Tags

```bash
usage: qualysdk-tag count_tags [-h] [-o OUTPUT] [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output (json) file to write results to
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```

### Get Tags

```bash
usage: qualysdk-tag get_tags [-h] [-o OUTPUT] [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output (xlsx) file to write results to
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```

### Get Tag Details

```bash
usage: qualysdk-tag get_tag_details [-h] [-o OUTPUT] -t TAGID

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output (json) file to write results to
  -t, --tagId TAGID    ID of the tag to pull details for
```