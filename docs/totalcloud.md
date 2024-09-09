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



## List Connectors API

```get_connectors``` returns a list of AWS in the subscription.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```pageNo``` | ```int``` | Page number to start pulling from, or page to pull if ```page_count``` is set to 1 | ❌ |
| ```pageSize``` | ```int``` | Number of records to pull per page | ❌ |
| ```sort``` | ```Literal["asc", "desc"]``` | Sort last synced date in ascending or descending order | ❌ |


```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_connectors

auth = BasicAuth(<username>, <password>, platform='qg1')
get_connectors(auth)
>>>[Connector(name="myConnector", ...), ...]
```
