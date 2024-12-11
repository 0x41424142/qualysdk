"""
Contains the functions to upload supported GAV API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


# For the softwareListData column, we need to parse build a string containing
# certain fields from the softwareListData object:
def parse_software_list_data(software_list_data):
    bl = BaseList()
    if software_list_data:
        for sw in software_list_data:
            if sw.get("productName") not in [None, "Unknown"]:
                bl.append(
                    f"{sw.get('productName')} ({sw.get('category')}) ({sw.get('version')})"
                )
            else:
                bl.append(
                    f"{sw.get('productName')} ({sw.get('category')}) ({sw.get('version')}) ({sw.get('ignoredReason')})"
                )
    return bl


def upload_gav_hosts(
    hosts: BaseList,
    cnxn: Connection,
    table_name: str = "gav_hosts",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```gav.query_assets``` or
    ```gav.get_all_assets``` to a SQL database.

    Args:
        hosts (BaseList): A BaseList of Host objects.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "assetId": types.Integer(),
        "assetUUID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hostId": types.Integer(),
        "lastModifiedDate": types.DateTime(),
        "agentId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdDate": types.DateTime(),
        "sensorLastUpdatedDate": types.DateTime(),
        "assetType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "address": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dnsName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "assetName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "netbiosName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "timeZone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "biosDescription": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "lastBoot": types.DateTime(),
        "totalMemory": types.Integer(),
        "cpuCount": types.Integer(),
        "lastLoggedOnUser": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "domainRole": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hwUUID": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "biosSerialNumber": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "biosAssetTag": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isContainerHost": types.Boolean(),
        "operatingSystem_osName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_fullName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_category": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_category1": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_category2": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_productName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_publisher": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_edition": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_marketVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_update": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_architecture": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_lifecycle_gaDate": types.DateTime(),
        "operatingSystem_lifecycle_eolDate": types.DateTime(),
        "operatingSystem_lifecycle_eosDate": types.DateTime(),
        "operatingSystem_lifecycle_stage": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_lifecycle_lifeCycleConfidence": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_lifecycle_eolSupportStage": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_lifecycle_eosSupportStage": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_lifecycle_detectionScore": types.Integer(),
        "operatingSystem_productUrl": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_productFamily": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_release": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_cpeId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_cpe": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_cpeType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem_installDate": types.DateTime(),
        "hardwareVendor": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_fullName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_category": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_category1": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_category2": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_manufacturer": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_productName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_model": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_lifecycle": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_productUrl": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_productFamily": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_introDate": types.DateTime(),
        "hardware_gaDate": types.DateTime(),
        "hardware_eosDate": types.DateTime(),
        "hardware_obsoleteDate": types.DateTime(),
        "hardware_stage": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_lifeCycleConfidence": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userAccountListData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "openPortListData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "volumeListData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "networkInterfaceListData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "softwareListData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "softwareComponent": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_accountId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_availabiltyZone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_hostname": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_instanceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_imageId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_instanceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvder_instanceState": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_qualysScanner": types.Boolean(),
        "cloudProvider_launchdate": types.DateTime(),
        "cloudProvider_privateDNS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_privateIpAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_publicDNS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_publicIpAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_hasAgent": types.Boolean(),
        "cloudProvider_region": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_spotInstance": types.Boolean(),
        "cloudProvider_subnetId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_vpcId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_imageOffer": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_imagePublisher": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_imageVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_location": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_macAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_platform": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_resourceGroupName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_size": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_state": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_subnet": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_subscriptionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_virtualNetwork": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudProvider_vmId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agent_version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agent_configurationProfile": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agent_connectedFrom": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agent_lastActivity": types.DateTime(),
        "agent_lastCheckedIn": types.DateTime(),
        "agent_lastInventory": types.DateTime(),
        "agent_udcManifestAssigned": types.Boolean(),
        "agent_errorStatus": types.Boolean(),
        "agent_key": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agent_status": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sensor_activatedForModules": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "sensor_pendingActivationForModules": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "sensor_lastVMScan": types.DateTime(),
        "sensor_lastComplianceScan": types.DateTime(),
        "sensor_lastFullScan": types.DateTime(),
        "sensor_lastVmScanDateScanner": types.DateTime(),
        "sensor_lastVmScanDateAgent": types.DateTime(),
        "sensor_lastPcScanDateScanner": types.DateTime(),
        "sensor_lastPcScanDateAgent": types.DateTime(),
        "sensor_firstEasmScanDate": types.DateTime(),
        "sensor_lastEasmScanDate": types.DateTime(),
        "container_product": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "container_version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "container_noOfContainers": types.Integer(),
        "container_noOfImages": types.Integer(),
        "container_hasSensor": types.Boolean(),
        "inventory_source": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "inventory_created": types.DateTime(),
        "inventory_lastUpdated": types.DateTime(),
        "activity_lastScannedDate": types.DateTime(),
        "tagList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "serviceList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "lastLocation": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "criticality": types.Integer(),
        "businessInformation": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "assignedLocation": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "businessAppListData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "riskScore": types.Integer(),
        "passiveSensor": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # ???
        "domain": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "subdomain": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "missingSoftware": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "whois": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "organizationName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isp": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "asn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "easmTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "hostingCategory1": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customAttributes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList[str]
        "processor": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the softwareListData column:
    for host in hosts:
        host.softwareListData = parse_software_list_data(host.softwareListData)

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(host) for host in hosts])

    # Drop cols that are parsed out into other fields:
    df.drop(
        columns=[
            "operatingSystem",
            "hardware",
            "provider",
            "agent",
            "sensor",
            "container",
            "inventory",
            "activity",
            "operatingSystem_lifecycle",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
