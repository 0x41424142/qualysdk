# Global AssetView APIs
Global AssetView APIs return data on hosts within your Qualys subscription. 
>**Pro Tip**: To see all available GAV QQL filters, look [here!](https://docs.qualys.com/en/gav/2.18.0.0/search/how_to_search.htm)

After running:

```py
from qualysdk.gav import *
```
You can any of the 4 GAV endpoints:

## GAV Endpoints
|API Call| Description |
|--|--|
| ```count_assets``` | Count assets based on the ```filter``` kwarg, which is written in Qualys QQL.|
```get_asset```|Get a specific host based on the ```assetId``` kwarg.|
```get_all_assets```| Pull the entire host inventory (or a few pages of it with ```page_count```), in file sizes of ```pageSize```. Does **NOT** support ```filter```.|
|```query_assets```| Scaled down version of```get_all_assets``` - pulls entire host inventory that matches the given ```filter``` kwarg.

Or use the uber class:

```py
from qualysdk import TokenAuth, GAVUber

#Hey look! context managers!
with TokenAuth(<username>, <password>, platform='qg1') as auth:
    with GAVUber(auth) as uber:
        full_inventory_count = uber.get("count_assets")
        ...
```

## GAV QQL Tokens

**For a list of valid QQL search keywords, [click here.](https://docs.qualys.com/en/gav/latest/search_tips/search_ui.htm)**

## Count Assets API

The ```count_assets``` API is used to count the number of assets that match a given filter. The filter is written in GAV QQL.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
| ```filter```| ```str``` | The QQL filter to search for assets. | ❌ |
|```lastModifiedDate```| ```str``` | The last modified date of the asset. | ❌ |

```py
from qualysdk import TokenAuth
from qualysdk.gav import count_assets

with TokenAuth(<username>, <password>, platform='qg1') as auth:
    count = count_assets(auth, filter="operatingSystem.category1:`Windows`")
>>>{'count': 10000, 'responseCode': 'SUCCESS', 'responseMessage': 'Valid API Access'}
```

## Get Asset API

The ```get_asset``` API is used to get a specific asset based on its asset ID (accessible from the ```Host.assetId``` attribute).

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
|```assetId```| ```str``` | The asset ID of the host you want to get. | ✅ |
|```lastModifiedDate```| ```str``` | The last modified date of the asset. | ❌ |

```py
from qualysdk import TokenAuth
from qualysdk.gav import get_asset

with TokenAuth(<username>, <password>, platform='qg1') as auth:
    asset = get_asset(auth, assetId="123456")
>>>AssetID(123456)
```

## Get All Assets API

```get_all_assets``` is used to pull the entire GAV inventory. This is a very heavy operation, and will take some time depending on the size of your environment. 

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
|```page_count```| ```Union[int, 'all'] = 'all'``` | The number of pages to pull. | ❌ |
|```pageSize```| ```int``` | The number of assets to pull per page. Max value is 300.| ❌ |
|```excludeFields```|  ```Literal["activity", "lastLocation", "address", "lastLoggedOnUser", "agent", "netbiosName", "agentId", "networkInterface", "assetName", "openPort", "biosAssetTag", "operatingSystem", "biosDescription", "processor", "biosSerialNumber", "provider", "cloudProvider", "sensor", "container", "service", "cpuCount", "software", "dnsName", "tag", "hardware", "timeZone", "hostId", "totalMemory", "inventory", "userAccount", "isContainerHost", "volume", "lastBoot"]``` | Extra fields to exclude from the response. | ❌ |
| ```includeFields```| ```Literal["activity", "lastLocation", "address", "lastLoggedOnUser", "agent", "netbiosName", "agentId", "networkInterface", "assetName", "openPort", "biosAssetTag", "operatingSystem", "biosDescription", "processor", "biosSerialNumber", "provider", "cloudProvider", "sensor", "container", "service", "cpuCount", "software", "dnsName", "tag", "hardware", "timeZone", "hostId", "totalMemory", "inventory", "userAccount", "isContainerHost", "volume", "lastBoot"]``` | Extra fields to include in the response. | ❌ |
|```lastModifiedDate```| ```str``` | The last modified date of the asset. | ❌ |

```py
from qualysdk import TokenAuth
from qualysdk.gav import get_all_assets

# Get the first page of 100 assets, with
# cloudProvider, lastLoggedOnUser, and volume data excluded.
with TokenAuth(<username>, <password>, platform='qg1') as auth:
    all_assets = get_all_assets(
        auth, 
        page_count=1, 
        pageSize=100,
        excludeFields="cloudProvider,lastLoggedOnUser,volume",
    )
>>>[AssetID(123456), AssetID(123457), ...]
```

## Query Assets API

```query_assets``` is a scaled down version of ```get_all_assets```, and is used to pull the entire GAV inventory that matches a given QQL filter.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
|```filter```| ```str``` | The QQL filter to search for assets. | ✅ |
|```page_count```| ```Union[int, 'all'] = 'all'``` | The number of pages to pull. | ❌ |
|```pageSize```| ```int``` | The number of assets to pull per page. Max value is 300.| ❌ |
|```excludeFields```|  ```Literal["activity", "lastLocation", "address", "lastLoggedOnUser", "agent", "netbiosName", "agentId", "networkInterface", "assetName", "openPort", "biosAssetTag", "operatingSystem", "biosDescription", "processor", "biosSerialNumber", "provider", "cloudProvider", "sensor", "container", "service", "cpuCount", "software", "dnsName", "tag", "hardware", "timeZone", "hostId", "totalMemory", "inventory", "userAccount", "isContainerHost", "volume", "lastBoot"]``` | Extra fields to exclude from the response. | ❌ |
| ```includeFields```| ```Literal["activity", "lastLocation", "address", "lastLoggedOnUser", "agent", "netbiosName", "agentId", "networkInterface", "assetName", "openPort", "biosAssetTag", "operatingSystem", "biosDescription", "processor", "biosSerialNumber", "provider", "cloudProvider", "sensor", "container", "service", "cpuCount", "software", "dnsName", "tag", "hardware", "timeZone", "hostId", "totalMemory", "inventory", "userAccount", "isContainerHost", "volume", "lastBoot"]``` | Extra fields to include in the response. | ❌ |
|```lastModifiedDate```| ```str``` | The last modified date of the asset. | ❌ |

```py
from qualysdk import TokenAuth
from qualysdk.gav import query_assets

# Pull the first 100 Windows hosts:
with TokenAuth(<username>, <password>, platform='qg1') as auth:
    windows_assets = query_assets(auth, filter="operatingSystem.category1:`Windows`", page_count=1, pageSize=100)
>>>[AssetID(123456), AssetID(123457), ...]
```

## The GAV Host Dataclass
>**Heads Up!**: The ```Host``` class does not apply to ```count_assets()```

>**Head's Up!**: Not all ```Host``` attributes are populated by default. You can specify which fields to include/exclude in the response by using the ```includeFields``` and ```excludeFields``` parameters. Note that some fields will not be returned if your subscription does not include the Cybersecurity Asset Management upgrade.

When results are received from a GAV API, each host record is stored in a ```Host``` object, with its data points as attributes. Below is a list of all possible attributes:

```txt
'activity'
'activity_lastScannedDate'
'activity_source'
'address'
'agent'
'agentId'
'agent_configurationProfile'
'agent_connectedFrom'
'agent_errorStatus'
'agent_key'
'agent_lastActivity'
'agent_lastCheckedIn'
'agent_lastInventory'
'agent_status'
'agent_udcManifestAssigned'
'agent_version'
'asn'
'assetId'
'assetName'
'assetType'
'assetUUID'
'assignedLocation'
'biosAssetTag'
'biosDescription'
'biosSerialNumber'
'businessAppListData'
'businessInformation'
'cloudProvider'
'cloudProvider_accountId'
'cloudProvider_availabilityZone'
'cloudProvider_hasAgent'
'cloudProvider_hostname'
'cloudProvider_imageId'
'cloudProvider_imageOffer'
'cloudProvider_imagePublisher'
'cloudProvider_imageVersion'
'cloudProvider_instanceId'
'cloudProvider_instanceState'
'cloudProvider_instanceType'
'cloudProvider_launchdate'
'cloudProvider_location'
'cloudProvider_macAddress'
'cloudProvider_name'
'cloudProvider_platform'
'cloudProvider_privateDNS'
'cloudProvider_privateIpAddress'
'cloudProvider_publicDNS'
'cloudProvider_publicIpAddress'
'cloudProvider_qualysScanner'
'cloudProvider_region'
'cloudProvider_resourceGroupName'
'cloudProvider_size'
'cloudProvider_spotInstance'
'cloudProvider_state'
'cloudProvider_subnet'
'cloudProvider_subnetId'
'cloudProvider_subscriptionId'
'cloudProvider_virtualNetwork'
'cloudProvider_vmId'
'cloudProvider_vpcId'
'container'
'container_hasSensor'
'container_noOfContainers'
'container_noOfImages'
'container_product'
'container_version'
'cpuCount'
'createdDate'
'criticality'
'customAttributes'
'dnsName'
'domain'
'domainRole'
'easmTags'
'hardware'
'hardwareVendor'
'hardware_category'
'hardware_category1'
'hardware_category2'
'hardware_fullName'
'hardware_lifecycle'
'hardware_lifecycle_eosDate'
'hardware_lifecycle_gaDate'
'hardware_lifecycle_introDate'
'hardware_lifecycle_lifeCycleConfidence'
'hardware_lifecycle_obsoleteDate'
'hardware_lifecycle_stage'
'hardware_manufacturer'
'hardware_model'
'hardware_productFamily'
'hardware_productName'
'hardware_productUrl'
'hostId'
'hostingCategory1'
'hwUUID'
'inventory'
'inventory_created'
'inventory_lastUpdated'
'inventory_source'
'isContainerHost'
'isp'
'lastBoot'
'lastLocation'
'lastLoggedOnUser'
'lastModifiedDate'
'missingSoftware'
'netbiosName'
'networkInterfaceListData'
'openPortListData'
'operatingSystem'
'operatingSystem_architecture'
'operatingSystem_category'
'operatingSystem_category1'
'operatingSystem_category2'
'operatingSystem_cpe'
'operatingSystem_cpeId'
'operatingSystem_cpeType'
'operatingSystem_edition'
'operatingSystem_fullName'
'operatingSystem_installDate'
'operatingSystem_lifecycle'
'operatingSystem_lifecycle_detectionScore'
'operatingSystem_lifecycle_eolDate'
'operatingSystem_lifecycle_eolSupportStage'
'operatingSystem_lifecycle_eosDate'
'operatingSystem_lifecycle_eosSupportStage'
'operatingSystem_lifecycle_gaDate'
'operatingSystem_lifecycle_lifeCycleConfidence'
'operatingSystem_lifecycle_stage'
'operatingSystem_marketVersion'
'operatingSystem_osName'
'operatingSystem_productFamily'
'operatingSystem_productName'
'operatingSystem_productUrl'
'operatingSystem_publisher'
'operatingSystem_release'
'operatingSystem_update'
'operatingSystem_version'
'organizationName'
'passiveSensor'
'processor'
'provider'
'riskScore'
'sensor'
'sensorLastUpdatedDate'
'sensor_activatedForModules'
'sensor_firstEasmScanDate'
'sensor_lastComplianceScan'
'sensor_lastEasmScanDate'
'sensor_lastFullScan'
'sensor_lastPcScanDateAgent'
'sensor_lastPcScanDateScanner'
'sensor_lastVMScan'
'sensor_lastVmScanDateAgent'
'sensor_lastVmScanDateScanner'
'sensor_pendingActivationForModules'
'serviceList'
'softwareComponent'
'softwareListData'
'subdomain'
'tagList'
'timeZone'
'totalMemory'
'userAccountListData'
'volumeListData'
'whois'
```