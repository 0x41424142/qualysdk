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
| ```create_tag``` | Creates a new tag, optionally with a parent tag and child tags. |
| ```delete_tag``` | Deletes one or more tags. |
| ```update_tag``` | Updates a tag. |


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

## Create Tag API

```create_tag``` creates a new tag, optionally with a parent tag and child tags.

If no `ruleType` is provided, the tag will be static.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```name``` | ```str``` | The name of the tag to create | ✅ |
| ```ruleType``` | ```Literal["STATIC", "GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]``` | The type of rule the tag uses. If not provided, the tag will be static. | ❌ |
| ```ruleText``` | ```str``` | If `ruleType` is set, this string contains the logic for the rule. | ❌ |
| ```children``` | ```List[str]``` | A list of child tag names to create. | ❌ |
| ```parentTagId``` | ```int``` | The ID of the parent tag to create the tag under. | ❌ |
| ```criticalityScore``` | ```int``` | The criticality that assets with this tag should be assigned. | ❌ |
| ```color``` | ```str``` (hex code, such as `#FFFFFF`) | The color of the tag. | ❌ |
| ```description``` | ```str``` | A description of the tag. | ❌ |
| ```provider``` | ```Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]``` | The cloud provider the tag is for. | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.tagging import create_tag

auth = BasicAuth(<username>, <password>, platform='qg1')

# Create a new static tag:
create_tag(
    auth,
    name='My Static Tag',
    color='#FF0000',
    description='This is a static tag'
)

# Create a new dynamic tag identifying all Windows servers:
create_tag(
    auth,
    name='My Dynamic Tag',
    ruleType='GLOBAL_ASSET_VIEW',
    ruleText="operatingSystem:Windows and hardware.category:Server",
    color='#00FF00',
    description='This is a dynamic tag for Windows servers'
)

# create a new tag with a parent tag and child tags:
create_tag(
    auth,
    name='My Parent Tag',
    color='#0000FF',
    description='This is a parent tag',
    children=[
        'My Child Tag 1',
        'My Child Tag 2'
    ],
    parentTagId=123456789
)
```

## Delete Tag API

```delete_tag``` deletes one or more tags.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```tag_id``` | ``` Union[list[Union[str,int], Union[str,int]]``` | The ID(s) of a tag to delete. Multiple values can be provided as a list of strings | ✅ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.tagging import delete_tag

auth = BasicAuth(<username>, <password>, platform='qg1')

# Delete a single tag:
delete_tag(
    auth,
    tag_id=123456789
)
>>>1
# Delete multiple tags:
delete_tag(
    auth,
    tag_id=[
        123456789,
        987654321
    ]
)
>>>2

# Delete all tags with a name containing "prod":
from qualysdk.tagging import get_tags

tags = get_tags(
    auth,
    name='prod',
    name_operator='CONTAINS'
)

delete_tag(
    auth,
    tag_id=[tag.id for tag in tags]
)
>>>5
```

## Update Tag API

```update_tag``` updates a tag.

Note - you should not add and remove children tags in the same command. You should run two separate commands to do this.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```tag_id``` | ``` Union[str, int]``` | The ID of a tag to update. | ✅ |
| ```name``` | ```str``` | The new name of the tag | ❌ |
| ```ruleType``` | ```Literal["STATIC", "GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]``` | The type of rule the tag uses. If not provided, the tag will be static. | ❌ |
| ```ruleText``` | ```str``` | If `ruleType` is set, this string contains the logic for the rule. | ❌ |
| ```add_children``` | ```List[str]``` | A list of child tag names to add. | ❌ |
| ```remove_children``` | ```List[int]``` | A list of child tag IDs to remove. | ❌ |
| ```criticalityScore``` | ```int``` | The criticality that assets with this tag should be assigned. | ❌ |
| ```color``` | ```str``` (hex code, such as `#FFFFFF`) | The color of the tag. | ❌ |
| ```description``` | ```str``` | A description of the tag. | ❌ |
| ```provider``` | ```Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]``` | The cloud provider the tag is for. | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.tagging import update_tag

auth = BasicAuth(<username>, <password>, platform='qg1')

# Update a tag's name, description, and color:
update_tag(
    auth,
    tag_id=123456789,
    name='My Updated Tag',
    description='This is an updated tag',
    color='#FF00FF'
)
>>>123456789

# Change a tag from static to dynamic,
# looking for Windows Servers:
update_tag(
    auth,
    tag_id=123456789,
    ruleType='GLOBAL_ASSET_VIEW',
    ruleText="operatingSystem:Windows and hardware.category:Server",
    color='#00FFFF',
    description='This is a dynamic tag for Windows servers'
)
>>>123456789

# Update a tag to remove some 
# pre-existing children tags
# as well as adding a parent tag:
update_tag(
    auth,
    tag_id=123456789,
    remove_children=[987654321, 123456799],
    parentTagId=123459789
)
>>>123456789
```

## ```qualysdk-tag``` CLI tool

The ```qualysdk-tag``` CLI tool is a command-line interface for the tagging portion of the SDK. It allows you to quickly pull down results from tagging APIs and save them to an XLSX file and optionally print to stdout.

### Usage

```bash
usage: qualysdk-tag [-h] -u USERNAME -p PASSWORD [-P {qg1,qg2,qg3,qg4}] {count_tags,get_tags,get_tag_details,create_tag,delete_tag} ...

CLI script to quickly perform tagging operations using qualysdk

positional arguments:
  {count_tags,get_tags,get_tag_details,create_tag,delete_tag}
                        Action to perform
    count_tags          Count how many tags match the given criteria.
    get_tags            Get the tags that match the given criteria.
    get_tag_details     Get all details of a single tag.
    create_tag          Create a new tag. NOTE: For creating children tags, use --kwarg children with a comma-separated string, like: "child1,child2,etc"
    delete_tag          Delete a tag. NOTE: For deleting multiple tags, use --kwarg tagId with a comma-separated string, like: 'id1,id2,etc'

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

### Create Tag

```bash
usage: qualysdk-tag create_tag [-h] [-o OUTPUT] -n NAME [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output (json) file to write results to
  -n, --name NAME      Name of the tag to create
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```

#### Example Tag Creation

Below shows how to create a dynamic tag with children tags underneath.

```bash
qualysdk-tag -u <username> -p <password> create_tag -n "My servers tag" --kwarg ruleType GLOBAL_ASSET_VIEW --kwarg ruleText "hardware.category:Server" --kwarg color "#FFFF00" --kwarg children "CHILD1,CHILD2,CHILD3"
```

### Delete Tag

```bash
usage: qualysdk-tag delete_tag [-h] [-o OUTPUT] -t TAGID

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output (json) file to write results to
  -t, --tagId TAGID    ID(s) of the tag to delete. Multiple values can be provided as a comma-separated string
```

### Update Tag

```bash
usage: qualysdk-tag update_tag [-h] [-o OUTPUT] -t TAGID [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output (json) file to write results to
  -t, --tagId TAGID    ID of the tag to update
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times. For add_children, supply a comma-separated string of names. for remove_children, supply
                       a comma-separated string of ids.
```

#### Example Tag Update

Below shows how to update a tag to add children tags and remove children tags.

Note that you should not add AND remove children tags in the same command. You should run two separate commands to do this.

```bash
qualysdk-tag -u <username> -p <password> update_tag -t 12345678 --kwarg name "MY TAG UPDATED VIA API" --kwarg parentTagId 98765432 --kwarg description "My updated tag" --kwarg add_children "Child1,Child2" --kwarg remove_children 62041845
```