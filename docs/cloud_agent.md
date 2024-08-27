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
| ```list_agents``` | Lists all cloud agents in the subscription that match given kwargs. |


## List Agents API

```list_agents``` returns a list of cloud agents in the subscription that match the given kwargs.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```asset_id``` | ```str``` | Singular asset ID | ❌ |
| ```qwebHostId``` | ```int``` | QWEB Host ID | ❌ |
| ```lastVulnScan``` | ```str``` | Date string formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```lastComplianceScan``` | ```str``` | Date string formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```informationGatheredUpdated``` | ```str``` | Date string formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```os``` | ```str``` | Operating System | ❌ |
| ```dnsHostName``` | ```str``` | DNS Hostname | ❌ |
| ```address``` | ```str``` | IP Address | ❌ |
| ```vulnsUpdated``` | ```str``` | Date string formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```name``` | ```str``` | Host's Qualys Name | ❌ |
| ```created``` | ```str``` | Date string formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```type``` | ```str``` | Host Type | ❌ |
| ```netbiosName``` | ```str``` | NetBIOS Name | ❌ |
| ```netbiosNetworkID``` | ```str``` | NetBIOS Network ID | ❌ |
| ```networkGuid``` | ```str``` | Network GUID | ❌ |
| ```trackingMethod``` | ```Literal['NONE', 'IP', 'DNSNAME', 'NETBIOS', 'INSTANCE_ID', 'QAGENT']``` | Tracking Method | ❌ |
| ```port``` | ```int``` | Query ports | ❌ |
| ```installedSoftware``` | ```str``` | Query installed software | ❌ |
| ```tagName``` | ```str``` | Query by tag name | ❌ |
| ```tagId``` | ```int``` | Query by tag ID | ❌ |
| ```update``` | ```str``` | Date string formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```activationKey``` | ```str``` | Activation Key | ❌ |
| ```agentConfigurationName``` | ```str``` | Agent Configuration Name | ❌ |
| ```agentConfigurationId``` | ```float``` | Agent Configuration ID | ❌ |
| ```agentVersion``` | ```str``` | Agent Version | ❌ |
| ```lastCheckedIn``` | ```str``` | Date string formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```lastVulnScan_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for last vuln scan | ❌ |
| ```lastComplianceScan_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for last compliance scan | ❌ |
| ```informationGatheredUpdated_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for information gathered updated | ❌ |
| ```vulnsUpdated_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for vulns updated | ❌ |
| ```created_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for created | ❌ |
| ```agentConfigurationName_operator``` | ```Literal['EQUALS', 'CONTAINS']``` | Operator for agent configuration name | ❌ |
| ```agentVersion_operator``` | ```Literal['EQUALS', 'LESSER', 'GREATER']``` | Operator for agent version | ❌ |
| ```lastCheckedIn_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for last checked in | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.cloud_agent import list_agents

auth = BasicAuth(<username>, <password>, platform='qg1')
list_agents(auth, os='Windows')
>>>[CloudAgent(id=123456789, ...), ...]
```


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

```bulk_purge_agent``` purges multiple cloud agents from the subscription. Returns a ```str``` indicating success or an error message.

>**Head's Up!:** It is **HIGHLY** recommended to only use the ```asset_ids``` parameter for accuracy.

|Parameter | Possible Values | Description | Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```asset_ids``` | ```List[str]``` | List of asset IDs | ❌, but recommended! | 
| ```names``` | ```List[str]``` | List of asset names | ❌ | 
| ```created``` | ```str``` | Date string or datetime object formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```updated``` | ```str``` | Date string or datetime object formatted like ```YYYY-MM-DD[THH:MM:SSZ] | ❌ |
| ```created_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for created date | ❌ |
| ```updated_operator``` | ```Literal['GREATER', 'LESSER']``` | Operator for updated date | ❌ |
| ```tagName``` | ```list[str]``` | List of tag names | ❌ |
| ```agentUuid``` | ```list[str]``` | List of agent UUIDs | ❌ |


```py
from qualysdk.auth import BasicAuth
from qualysdk.cloud_agent import bulk_purge_agent

auth = BasicAuth(<username>, <password>, platform='qg1')
bulk_purge_agent(auth, asset_ids=['123456789', '987654321'])
>>>SUCCESS
```