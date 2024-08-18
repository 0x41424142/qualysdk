"""
hosts.py - contains the dataclass for a Qualys GAV host record.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Union

from ..base.base_list import BaseList


def handle_dict_or_list(data: Union[dict, list[dict]]) -> list[dict]:
    """
    Checks if an attribute contains a list of values or a single value,
    putting the single value into a list if necessary.

    Args:
        data (Union[dict, list[dict]]): The data to check.

    Returns:
        list[dict]: A list of dictionaries.
    """

    if isinstance(data, dict):
        data = [data]

    return data


@dataclass
class Host:
    """
    Host - represents a Qualys GAV host record.

    due to the fact that some APIs have excludeFields and IncludeFields parameters,
    virtually all fields are optional other than assetId.
    """

    assetId: int = None
    assetUUID: Optional[str] = None
    hostId: Optional[int] = None
    lastModifiedDate: Optional[str] = None
    agentId: Optional[str] = None
    createdDate: Optional[str] = None
    sensorLastUpdatedDate: Optional[str] = None
    assetType: Optional[str] = None
    address: Optional[str] = None
    dnsName: Optional[str] = None
    assetName: Optional[str] = None
    netbiosName: Optional[str] = None
    timeZone: Optional[str] = None
    biosDescription: Optional[str] = None
    lastBoot: Optional[str] = None
    totalMemory: Optional[int] = None
    cpuCount: Optional[int] = None
    lastLoggedOnUser: Optional[str] = None
    domainRole: Optional[str] = None
    hwUUID: Optional[str] = None
    biosSerialNumber: Optional[str] = None
    biosAssetTag: Optional[str] = None
    isContainerHost: Optional[bool] = None
    operatingSystem: Optional[str] = None
    operatingSystem_osName: Optional[str] = None
    operatingSystem_fullName: Optional[str] = None
    operatingSystem_category: Optional[str] = None
    operatingSystem_category1: Optional[str] = None
    operatingSystem_category2: Optional[str] = None
    operatingSystem_productName: Optional[str] = None
    operatingSystem_publisher: Optional[str] = None
    operatingSystem_edition: Optional[str] = None
    operatingSystem_marketVersion: Optional[str] = None
    operatingSystem_version: Optional[str] = None
    operatingSystem_update: Optional[str] = None
    operatingSystem_architecture: Optional[str] = None
    operatingSystem_lifecycle: Optional[str] = None
    operatingSystem_productUrl: Optional[str] = None
    operatingSystem_productFamily: Optional[str] = None
    operatingSystem_release: Optional[str] = None
    operatingSystem_cpeId: Optional[str] = None
    operatingSystem_cpe: Optional[str] = None
    operatingSystem_cpeType: Optional[str] = None
    operatingSystem_installDate: Optional[datetime] = None
    hardwareVendor: Optional[str] = None
    hardware: Optional[dict] = None
    hardware_fullName: Optional[str] = None
    hardware_category: Optional[str] = None
    hardware_category1: Optional[str] = None
    hardware_category2: Optional[str] = None
    hardware_manufacturer: Optional[str] = None
    hardware_productName: Optional[str] = None
    hardware_model: Optional[str] = None
    hardware_lifecycle: Optional[str] = None
    hardware_productUrl: Optional[str] = None
    hardware_productFamily: Optional[str] = None
    userAccountListData: Optional[Union[list[dict], BaseList[str]]] = None
    openPortListData: Optional[Union[list[dict], BaseList[str]]] = None
    volumeListData: Optional[Union[list[dict], BaseList[str]]] = None
    networkInterfaceListData: Optional[dict] = None
    softwareListData: Optional[Union[list[dict], BaseList[str]]] = None
    softwareComponent: Optional[str] = None
    provider: Optional[str] = None
    cloudProvider: Optional[dict] = None
    # AWS:
    cloudProvider_accountId: Optional[str] = None
    cloudProvider_availabilityZone: Optional[str] = None
    cloudProvider_hostname: Optional[str] = None
    cloudProvider_imageId: Optional[str] = None
    cloudProvider_instanceId: Optional[str] = None
    cloudProvider_instanceState: Optional[str] = None
    cloudProvider_instanceType: Optional[str] = None
    cloudProvider_qualysScanner: Optional[bool] = None
    cloudProvider_launchdate: Optional[Union[str, datetime]] = None
    cloudProvider_privateDNS: Optional[str] = None
    cloudProvider_privateIpAddress: Optional[str] = None
    cloudProvider_publicDNS: Optional[str] = None
    cloudProvider_publicIpAddress: Optional[str] = None
    cloudProvider_hasAgent: Optional[bool] = None
    cloudProvider_region: Optional[str] = None
    cloudProvider_spotInstance: Optional[bool] = None
    cloudProvider_subnetId: Optional[str] = None
    cloudProvider_vpcId: Optional[str] = None
    # Azure:
    cloudProvider_imageOffer: Optional[str] = None
    cloudProvider_imagePublisher: Optional[str] = None
    cloudProvider_imageVersion: Optional[str] = None
    cloudProvider_location: Optional[str] = None
    cloudProvider_macAddress: Optional[str] = None
    cloudProvider_name: Optional[str] = None
    cloudProvider_platform: Optional[str] = None
    cloudProvider_resourceGroupName: Optional[str] = None
    cloudProvider_size: Optional[str] = None
    cloudProvider_state: Optional[str] = None
    cloudProvider_subnet: Optional[str] = None
    cloudProvider_subscriptionId: Optional[str] = None
    cloudProvider_virtualNetwork: Optional[str] = None
    cloudProvider_vmId: Optional[str] = None
    # NO SUPPORT FOR OTHER CLOUD PROVIDERS YET!
    agent: Optional[dict] = None
    agent_version: Optional[str] = None
    agent_configurationProfile: Optional[str] = None
    agent_connectedFrom: Optional[str] = None
    agent_lastActivity: Optional[Union[str, datetime]] = None
    agent_lastCheckedIn: Optional[Union[str, datetime]] = None
    agent_lastInventory: Optional[Union[str, datetime]] = None
    agent_udcManifestAssigned: Optional[bool] = None
    agent_errorStatus: Optional[bool] = None
    agent_key: Optional[str] = None
    agent_status: Optional[str] = None
    sensor: Optional[dict] = None
    sensor_activatedForModules: Optional[Union[list[str], BaseList[str]]] = None
    sensor_pendingActivationForModules: Optional[Union[list[str], BaseList[str]]] = None
    sensor_lastVMScan: Optional[Union[str, datetime]] = None
    sensor_lastComplianceScan: Optional[Union[str, datetime]] = None
    sensor_lastFullScan: Optional[Union[str, datetime]] = None
    sensor_lastVmScanDateScanner: Optional[Union[str, datetime]] = None
    sensor_lastVmScanDateAgent: Optional[Union[str, datetime]] = None
    sensor_lastPcScanDateScanner: Optional[Union[str, datetime]] = None
    sensor_lastPcScanDateAgent: Optional[Union[str, datetime]] = None
    sensor_firstEasmScanDate: Optional[Union[str, datetime]] = None
    sensor_lastEasmScanDate: Optional[Union[str, datetime]] = None
    container: Optional[dict] = None
    container_product: Optional[str] = None
    container_version: Optional[str] = None
    container_noOfContainers: Optional[int] = None
    container_noOfImages: Optional[int] = None
    container_hasSensor: Optional[bool] = None
    inventory: Optional[dict] = None
    inventory_source: Optional[str] = None
    inventory_created: Optional[Union[str, datetime]] = None
    inventory_lastUpdated: Optional[Union[str, datetime]] = None
    activity: Optional[dict] = None
    activity_source: Optional[str] = None
    activity_lastScannedDate: Optional[Union[str, datetime]] = None
    tagList: Optional[Union[str, List[str], BaseList[str]]] = None
    serviceList: Optional[Union[str, List[str], BaseList[str]]] = None
    lastLocation: Optional[Union[dict, str]] = None
    criticality: Optional[int] = None
    businessInformation: Optional[dict] = None
    assignedLocation: Optional[dict] = None
    businessAppListData: Optional[Union[list[dict], BaseList[str]]] = None
    riskScore: Optional[int] = None
    passiveSensor: Optional[dict] = None
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    missingSoftware: Optional[Union[list[dict], BaseList[str]]] = None
    whois: Optional[dict] = None
    organizationName: Optional[str] = None
    isp: Optional[str] = None
    asn: Optional[str] = None
    easmTags: Optional[Union[str, List[str], BaseList[str]]] = None
    hostingCategory1: Optional[str] = None
    customAttributes: Optional[dict] = None
    processor: Optional[Union[dict, str]] = None

    def __post_init__(self):
        DT_FIELDS = [
            "lastModifiedDate",
            "createdDate",
            "sensorLastUpdatedDate",
            "lastBoot",
        ]

        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if self.businessAppListData:
            # EXPERIMENTAL! I DO NOT HAVE ANY BUSINESS APPS!
            try:
                data = handle_dict_or_list(self.businessAppListData["businessApp"])
                bl = BaseList()
                bl.extend([app.get("name") for app in data])
                setattr(self, "businessAppListData", bl)
            except KeyError:
                # Best guesses here...
                data = handle_dict_or_list(self.businessAppListData["app"])
                bl = BaseList()
                bl.extend([app.get("name") for app in data])
                setattr(self, "businessAppListData", bl)

        if self.operatingSystem:
            for field in [
                "osName",
                "fullName",
                "category",
                "category1",
                "category2",
                "productName",
                "publisher",
                "edition",
                "marketVersion",
                "version",
                "update",
                "architecture",
                "lifecycle",
                "productUrl",
                "productFamily",
                "release",
                "cpeId",
                "cpe",
                "cpeType",
            ]:
                if self.operatingSystem.get(field):
                    setattr(
                        self, f"operatingSystem_{field}", self.operatingSystem[field]
                    )
            # we will deal with installDate separately:
            if self.operatingSystem.get("installDate"):
                # Convert installDate to datetime object
                setattr(
                    self,
                    "operatingSystem_installDate",
                    datetime.fromisoformat(self.operatingSystem["installDate"]),
                )

            # Set the operatingSystem field to None
            setattr(self, "operatingSystem", None)

        if self.hardware:
            for field in [
                "fullName",
                "category",
                "category1",
                "category2",
                "manufacturer",
                "productName",
                "model",
                "lifecycle",
                "productUrl",
                "productFamily",
            ]:
                if self.hardware.get(field):
                    setattr(self, f"hardware_{field}", self.hardware[field])
            # Set the hardware field to None
            setattr(self, "hardware", None)

        if self.userAccountListData:
            # Check for a dict or a list of dicts:
            data = handle_dict_or_list(self.userAccountListData["userAccount"])
            bl = BaseList()
            for user in data:
                bl.append(user.get("name"))
            setattr(self, "userAccountListData", bl)

        if self.openPortListData:
            # Check for a dict or a list of dicts:
            data = self.openPortListData["openPort"]
            bl = BaseList()
            for port in data:
                bl.append(
                    f"{port.get('port')}-{port.get('protocol')} ({port.get('detectedService')})"
                )
            setattr(self, "openPortListData", bl)

        if self.volumeListData:
            # Check for a dict or a list of dicts:
            data = handle_dict_or_list(self.volumeListData["volume"])
            bl = BaseList()
            for vol in data:
                try:
                    percent_filled = (
                        (vol.get("size") - vol.get("free")) / vol.get("size") * 100
                    )
                except ZeroDivisionError:
                    percent_filled = 0.0
                bl.append(f"{vol.get('name')}: {percent_filled:.2f}% filled")
            setattr(self, "volumeListData", bl)

        if self.networkInterfaceListData:
            # Check for a dict or a list of dicts:
            data = handle_dict_or_list(
                self.networkInterfaceListData["networkInterface"]
            )
            bl = BaseList()
            for iface in data:
                bl.append(
                    f"{iface.get('interfaceName').replace('      ', ' ')} - {iface.get('manufacturer')}"
                )  # Replace multi-spaces with single spaces for easier reading
            setattr(self, "networkInterfaceListData", bl)

        if self.softwareListData:
            data = handle_dict_or_list(self.softwareListData["software"])
            bl = BaseList()
            for sw in data:
                bl.append(
                    f"{sw.get('fullName')} ({sw.get('category')}) ({sw.get('ignoredReason')})"
                )
            setattr(self, "softwareListData", bl)

        if self.softwareComponent:
            if not isinstance(self.softwareComponent, str):
                raise Exception("SoftwareComponent must be a string.")

        if self.cloudProvider:
            # A bit different. This is a dictionary with all cloud providers.
            # The valid one will have a dictionary underneath of it.
            # First, find the one that is not a NoneType:
            for provider, data in self.cloudProvider.items():
                if data:
                    cloudProvider = provider
                    subkeys = list(data.keys())
                    break

            for subkey in subkeys:
                if subkey != "tags":
                    for attr in [
                        "accountId",
                        "availabilityZone",
                        "hasAgent",
                        "hostname",
                        "imageId",
                        "instanceId",
                        "instanceState",
                        "instanceType",
                        "qualyScanner",
                        "kernelId",
                        "privateDNS",
                        "privateIpAddress",
                        "publicDNS",
                        "publicIpAddress",
                        "spotInstance",
                        "subnetId",
                        "vpcId",
                        "imageOffer",
                        "imagePublisher",
                        "imageVersion",
                        "location",
                        "macAddress",
                        "name",
                        "platform",
                        "resourceGroupName",
                        "size",
                        "state",
                        "subnet",
                        "subscriptionId",
                        "virtualNetwork",
                        "vmId",
                    ]:
                        if self.cloudProvider[cloudProvider].get(subkey).get(attr):
                            setattr(
                                self,
                                f"cloudProvider_{attr}",
                                self.cloudProvider[cloudProvider][subkey].get(attr),
                            )

                    # Convert launchdate to datetime object
                    if self.cloudProvider[cloudProvider].get(subkey).get(
                        "launchDate"
                    ) and not isinstance(
                        self.cloudProvider[cloudProvider][subkey]["launchDate"],
                        datetime,
                    ):
                        setattr(
                            self,
                            "cloudProvider_launchDate",
                            datetime.fromisoformat(
                                self.cloudProvider[cloudProvider][subkey]["launchDate"]
                            ),
                        )

                    # Parse out region:
                    if self.cloudProvider[cloudProvider].get(subkey).get(
                        "region"
                    ) and not isinstance(
                        self.cloudProvider[cloudProvider][subkey]["region"], str
                    ):
                        setattr(
                            self,
                            "cloudProvider_region",
                            self.cloudProvider[cloudProvider][subkey]
                            .get("region")
                            .get("code"),
                        )

                elif subkey == "tags":
                    data = handle_dict_or_list(
                        self.cloudProvider[cloudProvider][subkey]
                    )
                    bl = BaseList()
                    if data:
                        for tag in data:
                            s = (
                                f"{tag.get('key')}:{tag.get('value')}"
                                if tag.get("key")
                                else f"{tag.get('name')}:{tag.get('value')}"
                            )
                        setattr(self, "cloudProvider_tags", bl)

                else:
                    print(f"Unknown subkey: {subkey}")

                # Set the cloudProvider field to the valid provider
            setattr(self, "cloudProvider", cloudProvider)

        if self.agent:
            for field in [
                "version",
                "configurationProfile",
                "connectedFrom",
                "udcManifestAssigned",
                "errorStatus",
            ]:
                if self.agent.get(field):
                    setattr(self, f"agent_{field}", self.agent[field])
            if self.agent.get("activations"):
                setattr(self, "agent_key", self.agent.get("activations")[0].get("key"))
                setattr(
                    self, "agent_status", self.agent.get("activations")[0].get("status")
                )
            for dt_field in ["lastActivity", "lastCheckedIn", "lastInventory"]:
                if self.agent.get(dt_field) and not isinstance(
                    self.agent.get(dt_field), datetime
                ):
                    if self.agent.get(dt_field) != -1:
                        setattr(
                            self,
                            f"agent_{dt_field}",
                            datetime.fromtimestamp(self.agent[dt_field] / 1000),
                        )
                    else:
                        setattr(self, f"agent_{dt_field}", None)

            # Set the agent field to None
            setattr(self, "agent", None)

        if self.sensor:
            for field in ["activatedForModules", "pendingActivationForModules"]:
                bl = BaseList()
                if self.sensor.get(field):
                    bl.extend(self.sensor[field])
                    setattr(self, f"sensor_{field}", bl)
            for dt_field in [
                "lastVMScan",
                "lastComplianceScan",
                "lastFullScan",
                "lastVmScanDateScanner",
                "lastVmScanDateAgent",
                "lastPcScanDateScanner",
                "lastPcScanDateAgent",
                "firstEasmScanDate",
                "lastEasmScanDate",
            ]:
                if self.sensor.get(dt_field) and not isinstance(
                    self.sensor.get(dt_field), datetime
                ):
                    setattr(
                        self,
                        f"sensor_{dt_field}",
                        datetime.fromtimestamp(self.sensor[dt_field] / 1000),
                    )

            # Set the sensor field to None
            setattr(self, "sensor", None)

        if self.container:
            for field in ["product", "version", "noOfContainers", "noOfImages"]:
                if self.container.get(field):
                    setattr(self, f"container_{field}", self.container[field])

            if self.container.get("hasSensor"):
                setattr(self, "container_hasSensor", bool(self.container["hasSensor"]))
            else:
                setattr(self, "container_hasSensor", False)

            # Set the container field to None
            setattr(self, "container", None)

        if self.inventory:
            setattr(self, "inventory_source", self.inventory.get("source"))
            setattr(
                self,
                "inventory_created",
                datetime.fromtimestamp(self.inventory.get("created") / 1000),
            )
            setattr(
                self,
                "inventory_lastUpdated",
                datetime.fromtimestamp(self.inventory.get("lastUpdated") / 1000),
            )

            # Set the inventory field to None
            setattr(self, "inventory", None)

        if self.activity:
            setattr(self, "activity_source", self.activity.get("source"))
            setattr(
                self,
                "activity_lastScannedDate",
                datetime.fromtimestamp(self.activity.get("lastScannedDate") / 1000),
            )

            # Set the activity field to None
            setattr(self, "activity", None)

        if self.tagList:
            data = handle_dict_or_list(self.tagList["tag"])
            bl = BaseList()
            bl.extend([tag.get("tagName") for tag in data])
            setattr(self, "tagList", bl)

        if self.serviceList:
            data = handle_dict_or_list(self.serviceList["service"])
            bl = BaseList()
            for service in data:
                bl.append(f"{service.get('name')} ({service.get('status')})")
            setattr(self, "serviceList", bl)

        if self.lastLocation and not isinstance(self.lastLocation, str):
            setattr(self, "lastLocation", self.lastLocation.get("name"))

        if self.criticality:
            score = self.criticality.get("score")
            if not score:
                score = 0
            setattr(self, "criticality", score)

        if self.missingSoftware:
            data = handle_dict_or_list(self.missingSoftware)
            bl = BaseList()
            if data:
                for sw in data:
                    full_category = f"{sw.get('category1')} / {sw.get('category2')}"
                    bl.append(f"{sw.get('name')} ({full_category})")

                setattr(self, "missingSoftware", bl)
            else:
                setattr(self, "missingSoftware", None)

        if self.easmTags:
            # EXPERIMENTAL! I DO NOT HAVE ACCESS TO EASM!
            data = handle_dict_or_list(self.tagList["tag"])
            bl = BaseList()
            bl.extend([tag.get("tagName") for tag in data])
            setattr(self, "tagList", bl)

        if self.customAttributes:
            print(self.customAttributes)

        if self.processor and not isinstance(self.processor, str):
            setattr(self, "processor", self.processor.get("description"))

    def is_cloud_host(self) -> bool:
        """
        Returns True if the host is a cloud host, False otherwise.
        """
        return self.cloudProvider is not None

    def is_container_host(self) -> bool:
        """
        Returns True if the host is a container host, False otherwise.
        """
        return self.container is not None

    def has_agent(self) -> bool:
        """
        Returns True if the host has an agent, False otherwise.
        """
        return self.agentId is not None

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the host object.
        """
        return asdict(self)

    def keys(self) -> list:
        """
        Returns a list of keys for the host object.
        """
        return [key for key in self.to_dict().keys()]

    def values(self) -> list:
        """
        Returns a list of values for the host object.
        """
        return [value for value in self.to_dict().values()]

    def items(self) -> list:
        """
        Returns a list of tuples for the host object.
        """
        return [(key, value) for key, value in self.to_dict().items()]

    def valid_values(self) -> list:
        """
        Return a list of keys that have values.
        """
        return [key for key, value in self.to_dict().items() if value]

    def __dict__(self) -> dict:
        return asdict(self)

    def __iter__(self):
        """
        Allows for iteration over the host object.
        """
        for key, value in self.to_dict().items():
            yield key, value

    def __str__(self) -> str:
        """
        String representation of the host object.
        """
        return self.assetName

    def __int__(self) -> int:
        """
        Integer representation of the host object.
        """
        return self.assetId

    def __repr__(self) -> str:
        """
        Breaking the unwritten rule of having repr be something
        that can create the object for terminal space's sake.
        """
        return f"AssetID({self.assetId})"
