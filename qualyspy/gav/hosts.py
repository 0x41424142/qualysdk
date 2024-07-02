"""
hosts.py - contains the dataclass for a Qualys GAV host record.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
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
    hardwareVendor: Optional[str] = None
    hardware: Optional[dict] = None
    userAccountListData: Optional[dict] = None
    openPortListData: Optional[dict] = None
    volumeListData: Optional[dict] = None
    networkInterfaceListData: Optional[dict] = None
    softwareListData: Optional[dict] = None
    softwareComponent: Optional[str] = None
    provider: Optional[str] = None
    cloudProvider: Optional[str] = None
    agent: Optional[dict] = None
    sensor: Optional[dict] = None
    container: Optional[dict] = None
    inventory: Optional[dict] = None
    activity: Optional[dict] = None
    tagList: Optional[List[str]] = None
    serviceList: Optional[List[str]] = None
    lastLocation: Optional[dict] = None
    criticality: Optional[int] = None
    businessInformation: Optional[dict] = None
    assignedLocation: Optional[dict] = None
    businessAppListData: Optional[dict] = None
    riskScore: Optional[int] = None
    passiveSensor: Optional[dict] = None
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    missingSoftware: Optional[list] = None
    whois: Optional[dict] = None
    organizationName: Optional[str] = None
    isp: Optional[str] = None
    asn: Optional[str] = None
    easmTags: Optional[List[str]] = None
    hostingCategory1: Optional[str] = None
    customAttributes: Optional[dict] = None
    processor: Optional[dict] = None

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
        return self.__dict__

    def keys(self) -> list:
        """
        Returns a list of keys for the host object.
        """
        return [key for key in self.__dict__.keys()]

    def values(self) -> list:
        """
        Returns a list of values for the host object.
        """
        return [value for value in self.__dict__.values()]

    def valid_values(self) -> list:
        """
        Return a list of keys that have values.
        """
        return [key for key, value in self.__dict__.items() if value is not None]

    def __iter__(self):
        """
        Allows for iteration over the host object.
        """
        for key, value in self.__dict__.items():
            yield key, value

    def __str__(self) -> str:
        """
        String representation of the host object.
        """
        return f"AssetID({self.assetId}))"

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
