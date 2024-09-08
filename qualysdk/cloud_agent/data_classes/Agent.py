"""
Contains the Agent data class for the Cloud Agent module.
"""

from typing import List, Union, Literal
from datetime import datetime
from dataclasses import dataclass, asdict, field
from ipaddress import ip_address

from ...base.base_list import BaseList
from ..data_classes.CloudAgentTag import CloudAgentTag


@dataclass
class CloudAgent:
    """
    Represents one cloud agent in a Qualys subscription.
    """

    id: int = field(default=None)
    name: str = field(default=None)
    created: datetime = field(default=None)
    modified: datetime = field(default=None)
    type: str = field(default=None)
    tags: BaseList[CloudAgentTag] = field(default=None)
    sourceInfo: list = field(default=None)
    qwebHostId: int = field(default=None)
    lastComplianceScan: datetime = field(default=None)
    lastSystemBoot: datetime = field(default=None)
    lastLoggedOnUser: str = field(default=None)
    dnsHostName: str = field(default=None)
    agentInfo: None = field(default=None)
    # agentInfo is parsed out into below fields:
    agentInfo_agentVersion: str = field(default=None)
    agentInfo_agentId: str = field(default=None)
    agentInfo_status: str = field(default=None)
    agentInfo_lastCheckedIn: datetime = field(default=None)
    agentInfo_connectedFrom: ip_address = field(default=None)
    agentInfo_location: str = field(default=None)
    agentInfo_locationGeoLatitude: float = field(default=None)
    agentInfo_locationGeoLongitude: float = field(default=None)
    agentInfo_chripStatus: str = field(default=None)
    agentInfo_platform: str = field(default=None)
    agentInfo_activatedModule: str = field(default=None)
    agentInfo_manifestVersion: str = field(default=None)
    agentInfo_agentConfiguration: None = field(default=None)
    # agentConfiguration is parsed out into below fields,
    # and is a sub-dictionary of agentInfo:
    agentInfo_agentConfiguration_id: int = field(default=None)
    agentInfo_agentConfiguration_name: str = field(default=None)
    # END agentConfiguration fields
    agentInfo_activationKey: None = field(default=None)
    # agentInfo_activationKey is a sub-dictionary of agentInfo
    # and is parsed out into below fields:
    agentInfo_activationKey_activationId: str = field(default=None)
    agentInfo_activationKey_title: str = field(default=None)
    # END agentInfo_activationKey fields
    # END agentInfo fields
    netbiosName: str = field(default=None)
    criticalityScore: int = field(default=None)
    lastVulnScan: datetime = field(default=None)
    vulnsUpdated: datetime = field(default=None)
    informationGatheredUpdated: datetime = field(default=None)
    domain: str = field(default=None)
    fqdn: str = field(default=None)
    os: str = field(default=None)
    networkGuid: str = field(default=None)
    address: ip_address = field(default=None)
    trackingMethod: Literal[
        "NONE", "IP", "DNSNAME", "NETBIOS", "INSTANCE_ID", "QAGENT"
    ] = field(default=None)
    manufacturer: str = field(default=None)
    model: str = field(default=None)
    totalMemory: int = field(default=None)
    timezone: str = field(default=None)
    biosDescription: str = field(default=None)
    openPort: BaseList[str] = field(default=None)
    software: BaseList[str] = field(default=None)
    vuln: BaseList[str] = field(default=None)
    processor: str = field(default=None)
    volume: BaseList[str] = field(default=None)
    account: BaseList[str] = field(default=None)
    networkInterface: BaseList[str] = field(default=None)
    isDockerHost: bool = field(default=None)
    dockerInfo: str = field(default=None)
    cloudProvider: str = field(default=None)

    def __post_init__(self):
        DATE_FIELDS = [
            "created",
            "modified",
            "lastComplianceScan",
            "lastSystemBoot",
            "agentInfo_lastCheckedIn",
            "lastVulnScan",
            "vulnsUpdated",
            "informationGatheredUpdated",
        ]
        INT_FIELDS = [
            "id",
            "qwebHostId",
            "agentInfo_agentConfiguration_id",
            "criticalityScore",
            "totalMemory",
        ]
        TO_NONE_FIELDS = [
            "agentInfo",
            "agentInfo_agentConfiguration",
            "agentInfo_activationKey",
        ]
        FLOAT_FIELDS = [
            "agentInfo_locationGeoLatitude",
            "agentInfo_locationGeoLongitude",
        ]
        IP_ADDRESS_FIELDS = ["agentInfo_connectedFrom"]

        for field in DATE_FIELDS:
            if getattr(self, field):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        for field in INT_FIELDS:
            if getattr(self, field):
                setattr(self, field, int(getattr(self, field)))

        for field in FLOAT_FIELDS:
            if getattr(self, field):
                setattr(self, field, float(getattr(self, field)))

        for field in IP_ADDRESS_FIELDS:
            if getattr(self, field):
                setattr(self, field, ip_address(getattr(self, field)))

        # Before setting none fields, let's build the BaseList objects
        if self.tags:
            tags = BaseList()
            data = self.tags.get("list")
            if data:
                data = data.get("TagSimple")
                if data and not isinstance(data, list):
                    data = [data]
                for tag in data:
                    tags.append(CloudAgentTag(**tag))

            if len(tags) > 0:
                setattr(self, "tags", tags)
            else:
                setattr(self, "tags", None)

        if self.openPort:
            open_ports = BaseList()
            data = self.openPort.get("list")
            if data:
                data = data.get("HostAssetOpenPort")
                if data and not isinstance(data, list):
                    data = [data]
                for port in data:
                    open_ports.append(
                        f"{port.get('port')}-{port.get('protocol')} ({port.get('serviceName')})"
                    )

            if len(open_ports) > 0:
                setattr(self, "openPort", open_ports)
            else:
                setattr(self, "openPort", None)

        if self.software:
            software = BaseList()
            data = self.software.get("list")
            if data:
                data = data.get("HostAssetSoftware")
                if data and not isinstance(data, list):
                    data = [data]
                for software_item in data:
                    software.append(f"{software_item.get('name')}")

            if len(software) > 0:
                setattr(self, "software", software)
            else:
                setattr(self, "software", None)

        if self.vuln:
            vulns = BaseList()
            data = self.vuln.get("list")
            if data:
                data = data.get("HostAssetVuln")
                if data and not isinstance(data, list):
                    data = [data]
                for vuln in data:
                    vulns.append(
                        f"{vuln.get('qid')} ({vuln.get('hostInstanveVulnId')}) First found: {vuln.get('firstFound')} Last found: {vuln.get('lastFound')}"
                    )

            if len(vulns) > 0:
                setattr(self, "vuln", vulns)
            else:
                setattr(self, "vuln", None)

        if self.processor:
            temp = []
            data = self.processor.get("list")
            if data:
                data = data.get("HostAssetProcessor")
                if data and not isinstance(data, list):
                    data = [data]
                for processor_item in data:
                    temp.append(f"{processor_item.get('name')}")

            if len(temp) > 0:
                setattr(self, "processor", temp[0])
            else:
                setattr(self, "processor", None)

        if self.volume:
            volumes = BaseList()
            data = self.volume.get("list")
            if data:
                data = data.get("HostAssetVolume")
                if data and not isinstance(data, list):
                    data = [data]
                for volume in data:
                    # Calculate the % free space on the volume. Account for 0 division!
                    try:
                        percent_free = (
                            int(volume.get("free")) / int(volume.get("size"))
                        ) * 100
                    except ZeroDivisionError:
                        percent_free = 0
                    volumes.append(f"{volume.get('name')} ({percent_free:.2f}% free)")

            if len(volumes) > 0:
                setattr(self, "volume", volumes)
            else:
                setattr(self, "volume", None)

        if self.account:
            accounts = BaseList()
            data = self.account.get("list")
            if data:
                data = data.get("HostAssetAccount")
                if data and not isinstance(data, list):
                    data = [data]
                for account in data:
                    accounts.append(account.get("username"))

            if len(accounts) > 0:
                setattr(self, "account", accounts)
            else:
                setattr(self, "account", None)

        if self.networkInterface:
            interfaces = BaseList()
            data = self.networkInterface.get("list")
            if data:
                data = data.get("HostAssetInterface")
                if data and not isinstance(data, list):
                    data = [data]
                for interface in data:
                    interfaces.append(
                        f"{interface.get('interfaceName')} ({interface.get('macAddress')})"
                    )

            if len(interfaces) > 0:
                setattr(self, "networkInterface", interfaces)
            else:
                setattr(self, "networkInterface", None)

        for field in TO_NONE_FIELDS:
            if getattr(self, field) == {}:
                setattr(self, field, None)

        if "isDockerHost" in asdict(self).keys():
            setattr(self, "isDockerHost", self.isDockerHost == "true")

        if self.dockerInfo:
            # dockerInfo is a dictionary with various keys and values.
            # Since we never know how many keys there are, we will
            # have to dynamically build the string.
            s = ""
            for key, value in self.dockerInfo.items():
                s += f"{key}: {value}"
                # if this is not the last key, add a comma and space
                if key != list(self.dockerInfo.keys())[-1]:
                    s += ", "

            setattr(self, "dockerInfo", s)

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    def __int__(self):
        return self.id

    def __str__(self) -> str:
        return self.name

    def created_after(self, date: datetime) -> bool:
        """
        Check if the agent was created after a certain date.

        Args:
            date (datetime): The date to check against.

        Returns:
            bool: True if the agent was created after the date, False otherwise.
        """
        return self.created > date

    def created_before(self, date: datetime) -> bool:
        """
        Check if the agent was created before a certain date.

        Args:
            date (datetime): The date to check against.

        Returns:
            bool: True if the agent was created before the date, False otherwise.
        """
        return self.created < date

    def modified_after(self, date: datetime) -> bool:
        """
        Check if the agent was modified after a certain date.

        Args:
            date (datetime): The date to check against.

        Returns:
            bool: True if the agent was modified after the date, False otherwise.
        """
        return self.modified > date

    def modified_before(self, date: datetime) -> bool:
        """
        Check if the agent was modified before a certain date.

        Args:
            date (datetime): The date to check against.

        Returns:
            bool: True if the agent was modified before the date, False otherwise.
        """
        return self.modified < date
