# TotalCloud APIs

TotalCloud APIs return data relating to various cloud providers in your subscription, as well as manage them.

>**Head's Up!:** Currently, the TotalCloud module only supports AWS.

After running:
```py
from qualysdk.totalcloud import *
```
You can use any of the endpoints currently supported:

## Cloud Agent Endpoints

|API Call| Description |
|--|--|
| ```get_connectors``` | Get a list of AWS connectors in your Qualys subscription. |
| ```get_connector_details``` | Get details about a specific connector. |
| ```get_aws_base_account``` | Get the base account for an AWS connector. |



## List Connectors API

```get_connectors``` returns a list of AWS in the subscription.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```pageNo``` | ```int``` | Page number to start pulling from, or page to pull if ```page_count``` is set to 1 | ❌ |
| ```pageSize``` | ```int``` | Number of records to pull per page | ❌ |
| ```filter``` | ```str``` | Filter the results. See below for acceptable search tokens | ❌ |
| ```sort``` | ```Literal["lastSyncedOn:asc", "lastSyncedOn:desc"]``` | Sort last synced date in ascending or descending order | ❌ |


### ```filter``` Search Tokens


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
# Get all connectors that are successfully synced:
get_connectors(auth, filter='state:SUCCESS')
>>>[Connector(name="myConnector", ...), ...]
```

## Connector Details API

```get_connector_details``` returns details about a specific connector.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```connectorId``` | ```str``` | The ID of the connector to get details for | ✅ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_connector_details

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get details for a specific connector:
get_connector_details(auth, connectorId='12345678-1234-1234-1234-123456789012')
>>>Connector(name="myConnector", connectorId="12345678-1234-1234-1234-123456789012", ...)
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