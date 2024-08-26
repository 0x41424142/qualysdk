"""
gav.py - Contains the functions to upload supported GAV API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_gav_hosts(
    hosts: BaseList, cnxn: Connection, override_import_dt: datetime = None
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
        "assetUUID": types.String(),
        "hostId": types.Integer(),
        "lastModifiedDate": types.DateTime(),
        "agentId": types.String(),
        "createdDate": types.DateTime(),
        "sensorLastUpdatedDate": types.DateTime(),
        "assetType": types.String(),
        "address": types.String(),
        "dnsName": types.String(),
        "assetName": types.String(),
        "netbiosName": types.String(),
        "timeZone": types.String(),
        "biosDescription": types.String(),
        "lastBoot": types.DateTime(),
        "totalMemory": types.Integer(),
        "cpuCount": types.Integer(),
        "lastLoggedOnUser": types.String(),
        "domainRole": types.String(),
        "hwUUID": types.String(),
        "biosSerialNumber": types.String(),
        "biosAssetTag": types.String(),
        "isContainerHost": types.Boolean(),
        "operatingSystem_osName": types.String(),
        "operatingSystem_fullName": types.String(),
        "operatingSystem_category": types.String(),
        "operatingSystem_category1": types.String(),
        "operatingSystem_category2": types.String(),
        "operatingSystem_productName": types.String(),
        "operatingSystem_publisher": types.String(),
        "operatingSystem_edition": types.String(),
        "operatingSystem_marketVersion": types.String(),
        "operatingSystem_version": types.String(),
        "operatingSystem_update": types.String(),
        "operatingSystem_architecture": types.String(),
        "operatingSystem_lifecycle": types.String(),
        "operatingSystem_productUrl": types.String(),
        "operatingSystem_productFamily": types.String(),
        "operatingSystem_release": types.String(),
        "operatingSystem_cpeId": types.String(),
        "operatingSystem_cpe": types.String(),
        "operatingSystem_cpeType": types.String(),
        "operatingSystem_installDate": types.DateTime(),
        "hardwareVendor": types.String(),
        "hardware_fullName": types.String(),
        "hardware_category": types.String(),
        "hardware_category1": types.String(),
        "hardware_category2": types.String(),
        "hardware_manufacturer": types.String(),
        "hardware_productName": types.String(),
        "hardware_model": types.String(),
        "hardware_lifecycle": types.String(),
        "hardware_productUrl": types.String(),
        "hardware_productFamily": types.String(),
        "userAccountListData": types.String(),  # BaseList[str]
        "openPortListData": types.String(),  # BaseList[str]
        "volumeListData": types.String(),  # BaseList[str]
        "networkInterfaceListData": types.String(),  # BaseList[str]
        "softwareListData": types.String(),  # BaseList[str]
        "softwareComponent": types.String(),
        "cloudProvider": types.String(),
        "cloudProvider_accountId": types.String(),
        "cloudProvider_availabiltyZone": types.String(),
        "cloudProvider_hostname": types.String(),
        "cloudProvider_instanceId": types.String(),
        "cloudProvider_imageId": types.String(),
        "cloudProvider_instanceType": types.String(),
        "cloudProvder_instanceState": types.String(),
        "cloudProvider_qualysScanner": types.Boolean(),
        "cloudProvider_launchdate": types.DateTime(),
        "cloudProvider_privateDNS": types.String(),
        "cloudProvider_privateIpAddress": types.String(),
        "cloudProvider_publicDNS": types.String(),
        "cloudProvider_publicIpAddress": types.String(),
        "cloudProvider_hasAgent": types.Boolean(),
        "cloudProvider_region": types.String(),
        "cloudProvider_spotInstance": types.Boolean(),
        "cloudProvider_subnetId": types.String(),
        "cloudProvider_vpcId": types.String(),
        "cloudProvider_imageOffer": types.String(),
        "cloudProvider_imagePublisher": types.String(),
        "cloudProvider_imagePublisher": types.String(),
        "cloudProvider_imageVersion": types.String(),
        "cloudProvider_location": types.String(),
        "cloudProvider_macAddress": types.String(),
        "cloudProvider_name": types.String(),
        "cloudProvider_platform": types.String(),
        "cloudProvider_resourceGroupName": types.String(),
        "cloudProvider_size": types.String(),
        "cloudProvider_state": types.String(),
        "cloudProvider_subnet": types.String(),
        "cloudProvider_subscriptionId": types.String(),
        "cloudProvider_virtualNetwork": types.String(),
        "cloudProvider_vmId": types.String(),
        "agent_version": types.String(),
        "agent_configurationProfile": types.String(),
        "agent_connectedFrom": types.String(),
        "agent_lastActivity": types.DateTime(),
        "agent_lastCheckedIn": types.DateTime(),
        "agent_lastInventory": types.DateTime(),
        "agent_udcManifestAssigned": types.Boolean(),
        "agent_errorStatus": types.Boolean(),
        "agent_key": types.String(),
        "agent_status": types.String(),
        "sensor_activatedForModules": types.String(),  # BaseList[str]
        "sensor_pendingActivationForModules": types.String(),  # BaseList[str]
        "sensor_lastVMScan": types.DateTime(),
        "sensor_lastComplianceScan": types.DateTime(),
        "sensor_lastFullScan": types.DateTime(),
        "sensor_lastVmScanDateScanner": types.DateTime(),
        "sensor_lastVmScanDateAgent": types.DateTime(),
        "sensor_lastPcScanDateScanner": types.DateTime(),
        "sensor_lastPcScanDateAgent": types.DateTime(),
        "sensor_firstEasmScanDate": types.DateTime(),
        "sensor_lastEasmScanDate": types.DateTime(),
        "container_product": types.String(),
        "container_version": types.String(),
        "container_noOfContainers": types.Integer(),
        "container_noOfImages": types.Integer(),
        "container_hasSensor": types.Boolean(),
        "inventory_source": types.String(),
        "inventory_created": types.DateTime(),
        "inventory_lastUpdated": types.DateTime(),
        "activity_lastScannedDate": types.DateTime(),
        "tagList": types.String(),  # BaseList[str]
        "serviceList": types.String(),  # BaseList[str]
        "lastLocation": types.String(),
        "criticality": types.Integer(),
        "businessInformation": types.String(),
        "assignedLocation": types.String(),
        "businessAppListData": types.String(),  # BaseList[str]
        "riskScore": types.Integer(),
        "passiveSensor": types.String(),  # ???
        "domain": types.String(),
        "subdomain": types.String(),
        "missingSoftware": types.String(),  # BaseList[str]
        "whois": types.String(),
        "organizationName": types.String(),
        "isp": types.String(),
        "asn": types.String(),
        "easmTags": types.String(),  # BaseList[str]
        "hostingCategory1": types.String(),
        "customAttributes": types.String(),  # BaseList[str]
        "processor": types.String(),
    }

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
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, "gav_hosts", cnxn, COLS, override_import_dt)
