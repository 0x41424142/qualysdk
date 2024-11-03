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
| ```get_inventory``` | Get your inventory for a specific resource type on a specific cloud provider. |
| ```get_resource_details``` | Get details for a specific instance of a resource type. |
| ```get_evaluation``` | Get statistics for a specific control on a specific resource ID. |
| ```get_account_evaluation``` | Get statistics for a list of controls for a specific cloud account. |
| ```get_resources_evaluated_by_control``` | Get resources evaluated by a specific control. |
| ```get_remediation_activities``` | Get a list of remediation activities for a specific cloud provider. |



## List Connectors API

```get_connectors``` returns a list of AWS connectors in the subscription.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal["aws", "azure"]``` | The cloud provider to get connectors for | ✅ |
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

```get_connector_details``` returns details about a specific connector in AWS/Azure.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal["aws", "azure"]``` | The cloud provider to get connectors for | ✅ |
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
| ```filter``` | ```str``` | Filter the results. | ❌ |

#### ```filter``` Search Tokens

>**Head's Up!:** When using ```resource.type``` as the filter, you must use the API-expected name. See **```resourceType``` Values** table for expected names.

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

## Get Inventory API

```get_inventory``` returns your inventory for a specific resource type on a specific cloud provider.

This function takes advantage of multithreading to pull down data faster. You can specify the number of threads with the ```thread_count``` argument, which defaults to 5.

>**Head's Up!:** At maximum, this API endpoint returns 10,000 records. This is a hard limit imposed by Qualys. If you have more than 10K records under a single ```resourceType```, you will need to use the ```filter``` argument to narrow down the results and make repeated calls to get all the data. An easy way to do this is to use ```totalcloud.get_connectors()```, then use the connector's account ID (```subscriptionId``` for Azure) attribute in this API call's ```filter``` argument, storing the results in a ```BaseList```. For example: 

```py
from qualysdk import BaseList

# Pull ALL EC2s, not just the first 10K:
all_results = BaseList()
aws_connectors = get_connectors(auth, provider='aws')
aws_account_ids = [c.awsAccountId for c in aws_connectors]
if aws_account_ids:
    for account_id in aws_account_ids:
        data = get_inventory(auth, provider='aws', resourceType='ec2', filter=f"account.id:{account_id}")
        all_results.extend(data)
```


|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal["aws", "azure"]``` | The cloud provider to get inventory for | ✅ |
| ```resourceType``` | ```str``` | The resource type to get inventory for. See **resourceType Values**. | ✅ |
| ```page_count``` | ```Union[int>=1, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```thread_count``` | ```int >=1``` | Number of threads to use for pulling data | ❌ |
| ```sort``` | ```Literal['lastSyncedOn:asc', 'lastSyncedOn:desc']``` | Sort last synced date in ascending or descending order | ❌ |
| ```updated``` | ```str``` | Filter by updated date | ❌ |
| ```filter``` | ```str``` | Filter the results using TotalCloud QQL | ❌ |


```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_inventory

# Pull pull all EC2s with vulnerabilities
# using 8 threads:
vulnerable_ec2s = get_inventory(
    auth,
    provider='aws',
    resourceType='ec2',
    filter="vulnerability.typeDetected in (Confirmed, Potential) and NOT vulnerability.status:FIXED"
)
>>>[AWSEC2Instance(instanceId="i-1234567890abcdef0", ...), ...]
```

## Get Resource Details API

```get_resource_details``` returns details for a specific instance of a resource type, identified by the resource's UUID (can be accessed via the ```uuid``` attribute on an object).

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal["aws", "azure"]``` | The cloud provider to get resource details for | ✅ |
| ```resourceType``` | ```str``` | The resource type to get details for. See **resourceType Values** for acceptable values by cloud provider. | ✅ |
| ```resourceUuid``` | ```str``` | The resource UUID to get details for | ✅ |
| ```pageSize``` | ```int``` | Number of records to pull per page | ❌ |
| ```pageNo``` | ```int``` | Page number to start pulling from, or page to pull if ```page_count``` is set to 1 | ❌ |
| ```filter``` | ```str``` | Filter the results. See **resouceType Values** for acceptable search tokens | ❌ |
| ```sort``` | ```Literal['lastSyncedOn:asc', 'lastSyncedOn:desc']``` | Sort last synced date in ascending or descending order | ❌ |
| ```updated``` | ```str``` | Filter by updated date | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_resource_details, get_inventory

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get some EC2s:
ec2s = totalcloud.get_inventory(
    auth, 
    provider="aws", 
    resourceType="ec2", 
    page_count=1
)
# Get details for an EC2 instance:
get_resource_details(
    auth,
    provider='aws',
    resourceType='ec2',
    resourceUuid=ec2s[0].uuid
)
>>>AWSEC2Instance(instanceId="i-1234567890abcdef0", ...)
```


## Get Evaluation Results for a Control ID on a Single Resource


```get_evaluation``` returns datetime statistics for a specific control on a specific resource ID. You can see when the control was first and last checked on the resource, as well as if the control has been fixed, re-opened, or is still open.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal["aws", "azure"]``` | The cloud provider to get control statistics for | ✅ |
| ```controlId``` | ```Union[str, int]``` | The control ID to get statistics for | ✅ |
| ```connectorId``` | ```str``` | The connector ID to get statistics for | ✅ |
| ```resourceId``` | ```str``` | The resource ID to get statistics for | ✅ |


```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_evaluation

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get statistics for control 123 on EC2 instance
# i-1234567890abcdef0:
get_evaluation(
    auth,
    provider='aws',
    controlId=123,
    connectorId='12345678-1234-1234-1234-123456789012', #ec2.connectorUuid
    resourceId='i-1234567890abcdef0' #ec2.resourceId
)
>>>Evaluation(
    firstEvaluated=datetime.datetime(2024, 5, 10),
    lastEvaluated=datetime.datetime(2024, 5, 20),
    dateReopened=None,
    dateFixed=datetime.datetime(2024, 5, 15),
)
```

## Get Control Evaluation List for a Cloud Account

```get_account_evaluation``` returns statistics for a list of controls for a specific cloud account.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal['aws', 'azure']``` | Cloud Provider | ✅ |
| ```accountId``` | ```str``` | The cloud account/subscription ID to get statistics for | ✅ |
| ```filter``` | ```str``` | Filter results by Qualys Totalcloud ["Posture" QQL](https://docs.qualys.com/en/cloudview/latest/search_tips/search_ui_monitor.htm) | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_account_evaluation, get_connectors

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get some accounts:
aws_connectors = get_connectors(
    auth, 
    provider='aws', 
    page_count=1
)
# Get evaluations for all controls for the account:
account_evals = get_account_evaluation(
    auth,
    provider='aws',
    accountId=aws_connectors[0].awsAccountId
)
# Check out the first evaluation:
account_evals[0]
>>>AccountLevelControl(
    controlName='Ensure that custom IAM password policy requires minimum length of 14 or greater', 
    controlId=11, 
    policyNames=['CIS Amazon Web Services Foundations Benchmark'], 
    criticality='HIGH', 
    service='IAM', 
    result='PASS', 
    passedResources=10, 
    failedResources=0, 
    passWithExceptionResources=0
)
```

## Get a List of Resources Evaluated by a Control by Account

```get_resources_evaluated_by_control``` returns a list of resources evaluated by a specific control (identified by control ID) for a specific cloud account.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal['aws', 'azure']``` | Cloud Provider | ✅ |
| ```accountId``` | ```Union[str, int]``` | The cloud account/subscription ID to get statistics for | ✅ |
| ```controlId``` | ```Union[str, int]``` | The control ID to get statistics for | ✅ |
| ```filter``` | ```str``` | Filter results by Qualys Totalcloud ["Posture" QQL](https://docs.qualys.com/en/cloudview/latest/search_tips/search_ui_monitor.htm) | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_resources_evaluated_by_control, get_connectors, get_control_metadata

# Get some accounts:
aws_connectors = get_connectors(
    auth, 
    provider='aws', 
    page_count=1
)

# Get some controls:
controls = get_control_metadata(auth, filter='provider:AWS')

# Get resources evaluated by control 123 for the account:
resources_evaluated = get_resources_evaluated_by_control(
    auth,
    provider='aws',
    accountId=aws_connectors[0].awsAccountId,
    controlId=123
)
# Check out the first resource evaluated:
resources_evaluated[0]
>>>AccountLevelEvaluation(
    resourceId='123456789123', 
    region=None, 
    accountId='246802456', 
    evaluatedOn=datetime.datetime(2024, 1, 1, 22, 54, 12, tzinfo=datetime.timezone.utc), 
    evidences=[{'settingName': 'cn-north-1', 'actualValue': 'Access Analyzer disabled'}, ...], 
    resourceType='IAM_ACCESS_ANALYZER', 
    connectorId='aaaaaaaa-bbbb-cccc-dddd-1234567890', 
    result='FAIL', 
    evaluationDates=Evaluation(
        firstEvaluated=datetime.datetime(2023, 1, 16, 16, 39, 58, tzinfo=datetime.timezone.utc), 
        lastEvaluated=datetime.datetime(2024, 1, 1, 22, 54, 12, tzinfo=datetime.timezone.utc), 
        dateReopen=None, 
        dateFixed=None
    )
)
```

## Get Remediation Activities API

```get_remediation_activities``` returns a list of remediation activities for a specific cloud provider.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```provider``` | ```Literal['aws', 'azure']``` | Cloud Provider | ✅ |
| ```page_count``` | ```Union[int>=1, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```filter``` | ```str``` | Filter results by Qualys Totalcloud [QQL](https://docs.qualys.com/en/cloudview/latest/search_tips/search_remediation_activity.htm?rhhlterm=search%20remediation%20activity%20activities&rhsearch=Search%20for%20Remediation%20Activity) | ❌ |
| ```pageNo``` | ```int``` | Page number to start pulling from, or page to pull if ```page_count``` is set to 1 | ❌ |
| ```pageSize``` | ```int``` | Number of records to pull per page | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.totalcloud import get_remediation_activities

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get all remediation activities for AWS:
get_remediation_activities(auth, provider='aws')
>>>[RemediationActivity(
    resourceId='123456789123', 
    region=None, 
    accountId='246802456', 
    remediationAction='Disable Access Analyzer',
    connectorName='myConnector',
    ...), ...
]
```


## ```resourceType``` Values

```resourceType``` is case-insensitive. Values are translated to their expected API names. You can also just use the expected names directly, for example when feeding an API call based on data from a prior call using a dataclass's ```.resourceType``` attribute.

### AWS ```resourceType``` Values

| Provider | Resource Type/Final API-Expected Name | Acceptable ```resourceType``` Values |
|--|--|--|
| AWS | RDS | ```"RDS"``` |
| AWS | NETWORK_ACL | ```"NETWORK ACL"```, ```"ACL"``` |
| AWS | BUCKET | ```"BUCKET"```, ```"S3 BUCKET"```, ```"S3"``` |
| AWS | IAM_USER | ```"IAM USER"```, ```"IAM"```, ```"IAMUSER"``` |
| AWS | VPC | ```"VPC"``` |
| AWS | VPC_SECURITY_GROUP | ```"VPC SECURITY GROUP"```, ```"SECURITY GROUP"```, ```"SG"``` |
| AWS | LAMBDA | ```"LAMBDA"```, ```"LAMBDA FUNCTION"``` |
| AWS | SUBNET | ```"SUBNET"``` |
| AWS | INTERNET_GATEWAY | ```"INTERNET GATEWAY"```, ```"IG"```, ```"IGW"```, ```"GATEWAY"``` |
| AWS | LOAD_BALANCER | ```"LOAD BALANCER"```, ```"ELB"```, ```"LB"``` |
| AWS | EC2_INSTANCE | ```"EC2 INSTANCE"```, ```"EC2"```, ```"INSTANCE"``` |
| AWS | ROUTE_TABLE | ```"ROUTE TABLE"```, ```"ROUTE"```, ```"ROUTES"``` |
| AWS | EBS | ```"EBS"```, ```"VOLUME"```, ```"VOLUMES"```, ```"EBS VOLUME"```, ```"EBS VOLUMES"``` |
| AWS | AUTO_SCALING_GROUP | ```"AUTO SCALING GROUP"```, ```"ASG"```, ```"AUTO SCALING"``` |
| AWS | EKS_CLUSTER | ```"EKS CLUSTER"```, ```"EKS"``` |
| AWS | EKS_NODEGROUP | ```"EKS NODE GROUP"```, ```"EKSNG"```. ```"NODE GROUP"``` |
| AWS | EKS_FARGATE_PROFILE | ```"EKS FARGATE PROFILE"```, ```"FARGATE PROFILE"```, ```"EKS FARGATE"```, ```"FARGATE"``` |
| AWS | VPC_ENDPOINT | ```"VPC ENDPOINT"```, ```"ENDPOINT"``` |
| AWS | VPC_ENDPOINT_SERVICE | ```"VPC ENDPOINT SERVICE"```, ```"ENDPOINT SERVICE"``` |
| AWS | IAM_GROUP | ```"IAM GROUP"```, ```"IAMGROUP"``` |
| AWS | IAM_POLICY | ```"IAM POLICY"```, ```"IAMPOLICY"``` |
| AWS | IAM_ROLE | ```"IAM ROLE"```, ```"IAMROLE"``` |
| AWS | SAGEMAKER_NOTEBOOK | ```"SAGEMAKER NOTEBOOK"```, ```"NOTEBOOK"```, ```"SAGEMAKER"``` |
| AWS | CLOUDFRONT_DISTRIBUTION | ```"CLOUDFRONT DISTRIBUTION"```, ```"CLOUDFRONT"```|


### Azure ```resourceType``` Values


| Provider | Resource Type/Final API-Expected Name | Acceptable ```resourceType``` Values |
|--|--|--|
| AZURE | SQL_SERVER | ```"SQL SERVER"```, ```"MSSQL"``` |
| AZURE | FUNCTION_APP | ```"FUNCTION APP"```, ```"FUNCTION"``` |
| AZURE | SQL_SERVER_DATABASE | ```"SQL SERVER DATABASE"```, ```"MSSQL DATABASE"```, ```"MSSQLDB"```, ```"MSSQL DB"```|
| AZURE | RESOURCE_GROUP | ```"RESOURCE GROUP"```, ```"RG"``` |
| AZURE | VIRTUAL_NETWORK | ```"VIRTUAL NETWORK"```, ```"VNET"``` |
| AZURE | VIRTUAL_MACHINE | ```"VIRTUAL MACHINE"```, ```"VM"``` |
| AZURE | NETWORK_SECURITY_GROUP | ```"NETWORK SECURITY GROUP"```, ```"NSG"```, ```"SECURITY GROUP"``` |
| AZURE | WEB_APP | ```"WEB APP"```, ```"WEBAPP"``` |
| AZURE | NETWORK_INTERFACES | ```"NETWORK INTERFACES"```, ```"NIC"``` |
| AZURE | POSTGRE_SINGLE_SERVER | ```"POSTGRES"```, ```"POSTGRE"```, ```"POSTGRESQL"``` |
| AZURE | LOAD_BALANCER | ```"LOAD BALANCER"```, ```"LB"``` |
| AZURE | FIREWALL | ```"FIREWALL"```, ```"FW"``` |
| AZURE | MYSQL | ```"MYSQL"```, ```"MYSQL_DB"```, ```"MYSQLDB"``` |
| AZURE | STORAGE_ACCOUNT | ```"STORAGE ACCOUNT"```, ```"STORAGE"``` |
| AZURE | APPLICATION_GATEWAYS | ```"APPLICATION GATEWAYS"```, ```"AG"``` |
| AZURE | SECRETS | ```"SECRETS"```, ```"SECRET"``` |
| AZURE | MARIADB | ```"MARIADB"```, ```"MARIA_DB"```, ```"MARIA"``` |
| AZURE | COSMODB | ```"COSMOS DB"```, ```"COSMOSDB"```, ```"COSMODB"``` |
| AZURE | NAT_GATEWAYS | ```"NAT GATEWAYS"```, ```"NAT"``` |
