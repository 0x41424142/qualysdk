# Cloud Agent APIs

Cloud agent APIs return data on cloud agents in your subscription, as well as manage them.

After running:
```py
from qualysdk.cloud_agent import *
```
You can use any of the endpoints currently supported:

## Cloud Agent Endpoints

|API Call| Description |
|--|--|
| ```purge_agent``` | Purges a cloud agent from the subscription. |
| ```bulk_purge_agent``` | Purges multiple cloud agents from the subscription. |

## Purge Agent API

```purge_agent``` purges a cloud agent from the subscription. Returns a ```str``` indicating success or an error message.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```asset_id``` | ```str``` | Singular asset ID | ✅ | 

```py
from qualysdk.auth import BasicAuth
from qualysdk.cloud_agent import purge_agent

auth = BasicAuth(<username>, <password>, platform='qg1')
purge_agent(auth, asset_id='123456789')
>>>SUCCESS
```

## Bulk Purge Agent API

```bulk_purge_agent``` purges multiple cloud agents from the subscription. Returns a ```str``` indicating success pr an error message.

>**Head's Up!:** It is **HIGHLY** recommended to only use the ```asset_ids``` parameter for accuracy.

|Parameter | Possible Values | Description | Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```asset_ids``` | ```List[str]``` | List of asset IDs | ❌, but recommended! | 
| ```names``` | ```List[str]``` | List of asset names | ❌ | 
| ```created``` | ```str``` | Date string or datetime object formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```updated``` | ```str``` | Date string or datetime object formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```created_operator``` | ```Literal['GREATER_THAN', 'LESS_THAN']``` | Operator for created date | ❌ |
| ```updated_operator``` | ```Literal['GREATER_THAN', 'LESS_THAN']``` | Operator for updated date | ❌ |
| ```tagName``` | ```list[str]``` | List of tag names | ❌ |
| ```agentUuid``` | ```list[str]``` | List of agent UUIDs | ❌ |


```py
from qualysdk.auth import BasicAuth
from qualysdk.cloud_agent import bulk_purge_agent

auth = BasicAuth(<username>, <password>, platform='qg1')
bulk_purge_agent(auth, asset_ids=['123456789', '987654321'])
>>>SUCCESS
```