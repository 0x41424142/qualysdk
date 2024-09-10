# TotalCloud APIs

TotalCloud APIs return data relating to various cloud providers in your subscription, as well as manage them.

After running:
```py
from qualysdk.totalcloud import *
```
You can use any of the endpoints currently supported:

## TotalCloud Endpoints

|API Call| Description |
|--|--|
| ```get_connectors``` | Get a list of connectors in your Qualys subscription by provider. |
| ```get_connector_details``` | Get details about a specific connector by provider. |
| ```get_aws_base_account``` | Get the base account for an AWS connector. |
| ```get_control_metadata``` | Get details on controls Qualys checks for in your cloud provider. |



## List Connectors API

```get_connectors``` returns a list of AWS/Azure/GCP connectors in the subscription.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal["aws", "azure", "gcp"]``` | The cloud provider to get connectors for | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```pageNo``` | ```int``` | Page number to start pulling from, or page to pull if ```page_count``` is set to 1 | ❌ |
| ```pageSize``` | ```int``` | Number of records to pull per page | ❌ |
| ```filter``` | ```str``` | Filter the results. See below for acceptable search tokens | ❌ |
| ```sort``` | ```Literal["lastSyncedOn:asc", "lastSyncedOn:desc"]``` | Sort last synced date in ascending or descending order | ❌ |


#### ```filter``` Search Tokens


|Token| Description |
|--|--|
| ```name``` | Filter by connector name |
| ```description``` | Filter by connector description |
| ```state``` | Filter by connector state. Acceptable values are: ```SUCCESS```, ```PENDING```, ```REGIONS_DISCOVERED```, ```ERROR``` |
| ```lastSynced``` | Filter by last synced date. Must be in UTC time |


```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_connectors

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get all AWS connectors that are successfully synced:
get_connectors(auth, "aws", filter='state:SUCCESS')
>>>[AWSConnector(name="myConnector", ...), ...]
```


## Connector Details API

```get_connector_details``` returns details about a specific connector in AWS/Azure/GCP.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal["aws", "azure", "gcp"]``` | The cloud provider to get connectors for | ✅ |
| ```connectorId``` | ```str``` | The ID of the connector to get details for | ✅ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_connector_details

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get details for a specific Azure connector:
get_connector_details(auth, provider='azure', connectorId='12345678-1234-1234-1234-123456789012')
>>>AzureConnector(name="myConnector", connectorId="12345678-1234-1234-1234-123456789012", ...)
```

## Get AWS Base Account API

```get_aws_base_account``` returns the base account details for AWS.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |

```py
from json import dumps
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_aws_base_account

auth = BasicAuth(<username>, <password>, platform='qg1')
print(dumps(get_aws_base_account(auth), indent=2))
>>>{
    'globalAccountId': '123456789012', 
    'chinaAccountId': '210987654321', 
    'govAccountId': '001122334455', 
    'customerGlobalAccount': 'false', 
    'customerChinaAccount': 'false', 
    'customerGovAccount': 'false'
}
```

## Get Control Metadata API

```get_control_metadata``` returns details on controls Qualys checks for in your cloud provider. Think of it like the TotalCloud knowledge base, where misconfigurations Qualys checks for are stored.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```pageNo``` | ```int``` | Page number to start pulling from, or page to pull if ```page_count``` is set to 1 | ❌ |
| ```pageSize``` | ```int``` | Number of records to pull per page | ❌ |
| ```filter``` | ```str``` | Filter the results. See below for acceptable search tokens | ❌ |

#### ```filter``` Search Tokens

|Token| Description |
|--|--|
| ```control.name``` | Filter by control name. Ex: ```filter="control.name:MFA"``` |
| ```resource.type``` | Filter by resource type. Ex: ```filter="resource.type:BUCKET"``` |
| ```service.type``` | Filter by service type as seen from Qualys's inventory UI. Ex: ```filter="service.type:EC2"``` |
| ```cid``` | Filter by control ID. Ex: ```filter="cid:1"``` |
| ```provider``` | Filter by cloud provider |
| ```control.criticality``` | Filter by control criticality. Ex: ```filter="control.criticality:HIGH"```  |
| ```control.type``` | Filter by control type |
| ```policy.name``` | Filter by policy name |
| ```createdDate``` | Filter by created date |
| ```modifiedDate``` | Filter by modified date |
| ```isCustomizable``` | Filter by whether the control is customizable |
| ```qflow.name``` | Filter by QFlow name |
| ```qflow.id``` | Filter by QFlow ID |

```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_control_metadata

auth = BasicAuth(<username>, <password>, platform='qg1')

# Get all controls for AWS:
get_control_metadata(auth, filter='provider:AWS')
>>>[Control(name="Some Control", ...), ...]

# Get all controls for BUCKET resources:
get_control_metadata(auth, filter='resource.type:BUCKET')
>>>[Control(name="Some Control", ...), ...]
```
