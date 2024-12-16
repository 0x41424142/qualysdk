"""
scanner_appliance.py - Contains the ScannerAppliance data class.
"""

from dataclasses import dataclass, field, asdict
from uuid import UUID as uuid
from typing import Literal
from datetime import datetime
from ipaddress import IPv4Address

from .asset_group import AssetGroup
from .tag import Tag
from ...base.base_list import BaseList
from ...base.base_class import BaseClass


def build_dataclass_baselist(
    data: list[dict], class_type: Literal["ag", "tag"]
) -> BaseList:
    """
    Helps to normalize and build a BaseList of dataclasses from a list of dictionaries
    for the various fields in the ScannerAppliance dataclass.

    Parameters:
        data (list[dict]): The list of dictionaries to convert to a BaseList of dataclasses.
        class_type (Literal["ag", "tag"]): The type of dataclass to build. Either "ag" for AssetGroup or "tag" for Tag.

    Returns:
        BaseList[Union[AssetGroup, Tag]]: A BaseList of dataclasses.
    """

    key_mapping = {
        "ag": "ASSET_GROUP",
        "tag": "ASSET_TAG",
    }

    result = BaseList()

    # Qualys can return an immediate dict instead of a list of dicts
    # if the data is only one item. Convert it to a list of one dict
    # for normalization.

    if isinstance(data[key_mapping[class_type]], dict):
        data[key_mapping[class_type]] = [data[key_mapping[class_type]]]

    for item in data[key_mapping[class_type]]:
        match class_type:
            case "ag":
                # Convert the NAME key to TITLE
                item["TITLE"] = item.pop("NAME")
                # And build the AssetGroup object
                item = AssetGroup(**item)
            case "tag":
                # Convert the UUID key to ID
                item["TAG_ID"] = uuid(item.pop("UUID"))
                # And build the Tag object
                item = Tag(**item)
            # Other cases coming soon
        result.append(item)

    return result


@dataclass
class SecurityGroup(BaseClass):
    """
    Dataclass to store a scanner appliance's cloud security group information.
    """

    SECURITY_GROUP_IDS: str = field(
        metadata={"description": "The security group ID."},
        default=None,
    )

    SECURITY_GROUP_NAMES: str = field(
        metadata={"description": "The security group name."},
        default=None,
    )


@dataclass
class ScannerCloudInfo(BaseClass):
    """
    Dataclass to store a scanner appliance's cloud provider
    and instance information.
    """

    PLATFORM_PROVIDER: str = field(
        metadata={"description": "The cloud platform provider."},
        default=None,
    )

    EC2_INFO: dict = field(
        metadata={"description": "EC2 information. Gets deleted out."},
        default=None,
    )

    INSTANCE_ID: str = field(
        metadata={"description": "The cloud instance ID."},
        default=None,
    )

    INSTANCE_TYPE: str = field(
        metadata={"description": "The cloud instance type."},
        default=None,
    )

    AMI_ID: str = field(
        metadata={"description": "The cloud AMI ID."},
        default=None,
    )

    ACCOUNT_ID: int = field(
        metadata={"description": "The cloud account ID."},
        default=None,
    )

    INSTANCE_REGION: str = field(
        metadata={"description": "The cloud instance region."},
        default=None,
    )

    INSTANCE_AVAILABILITY_ZONE: str = field(
        metadata={"description": "The cloud instance availability zone."},
        default=None,
    )

    INSTANCE_ZONE_TYPE: str = field(
        metadata={"description": "The cloud instance zone type."},
        default=None,
    )

    INSTANCE_VPC_ID: str = field(
        metadata={"description": "The cloud instance VPC ID."},
        default=None,
    )

    INSTANCE_SUBNET_ID: str = field(
        metadata={"description": "The cloud instance subnet ID."},
        default=None,
    )

    INSTANCE_ADDRESS_PRIVATE: IPv4Address = field(
        metadata={"description": "The cloud instance private address."},
        default=None,
    )

    INSTANCE_ADDRESS_PUBLIC: IPv4Address = field(
        metadata={"description": "The cloud instance public address."},
        default=None,
    )

    HOSTNAME_PRIVATE: str = field(
        metadata={"description": "The cloud instance private hostname."},
        default=None,
    )

    SECURITY_GROUPS: BaseList[SecurityGroup] = field(
        metadata={"description": "The cloud instance security groups."},
        default=None,
    )

    API_PROXY_SETTINGS: Literal["Disabled", "Enabled"] = field(
        metadata={"description": "The cloud instance API proxy settings."},
        default=None,
    )

    def __post_init__(self):
        """
        Post init function to convert certain fields to int/float.
        """
        INT_FIELDS = ["ACCOUNT_ID"]
        IPV4_FIELDS = ["INSTANCE_ADDRESS_PRIVATE", "INSTANCE_ADDRESS_PUBLIC"]

        if self.EC2_INFO:
            # Set the parsed out attributes
            self.INSTANCE_ID = self.EC2_INFO.get("INSTANCE_ID")
            self.INSTANCE_TYPE = self.EC2_INFO.get("INSTANCE_TYPE")
            self.AMI_ID = self.EC2_INFO.get("AMI_ID")
            self.ACCOUNT_ID = self.EC2_INFO.get("ACCOUNT_ID")
            self.INSTANCE_REGION = self.EC2_INFO.get("INSTANCE_REGION")
            self.INSTANVE_AVAILABILITY_ZONE = self.EC2_INFO.get(
                "INSTANVE_AVAILABILITY_ZONE"
            )
            self.INSTANCE_ZONE_TYPE = self.EC2_INFO.get("INSTANCE_ZONE_TYPE")
            self.INSTANCE_VPC_ID = self.EC2_INFO.get("INSTANCE_VPC_ID")
            self.INSTANCE_SUBNET_ID = self.EC2_INFO.get("INSTANCE_SUBNET_ID")
            self.INSTANCE_ADDRESS_PRIVATE = self.EC2_INFO.get(
                "INSTANCE_ADDRESS_PRIVATE"
            )
            self.INSTANCE_ADDRESS_PUBLIC = self.EC2_INFO.get("INSTANCE_ADDRESS_PUBLIC")
            self.HOSTNAME_PRIVATE = self.EC2_INFO.get("HOSTNAME_PRIVATE")
            if self.EC2_INFO.get("SECURITY_GROUPS"):
                self.SECURITY_GROUPS = SecurityGroup.from_dict(
                    self.EC2_INFO.get("SECURITY_GROUPS")
                )
            self.API_PROXY_SETTINGS = self.EC2_INFO.get("API_PROXY_SETTINGS")["SETTING"]

        for int_field in INT_FIELDS:
            if getattr(self, int_field):
                setattr(self, int_field, int(getattr(self, int_field)))

        for ip_field in IPV4_FIELDS:
            if getattr(self, ip_field):
                setattr(self, ip_field, IPv4Address(getattr(self, ip_field)))

        del self.EC2_INFO

    def __getitem__(self, key):
        return asdict(self)[key]

    def __setitem__(self, key, value):
        asdict(self)[key] = value
        return asdict(self)

    def __str__(self):
        return self.INSTANCE_ID

    def __repr__(self) -> str:
        # Only return non-empty values
        return (
            "ScannerCloudInfo("
            + ", ".join(f"{k}={v}" for k, v in self.valid_values().items())
            + ")"
        )

    def valid_values(self):
        return {k: v for k, v in asdict(self).items() if v}


@dataclass
class ProxySettings(BaseClass):
    """
    Proxy settings for a scanner appliance.
    """

    SETTING: str = field(
        metadata={"description": "The setting."},
        default=None,
    )

    PROXY: dict = field(
        metadata={"description": "The proxy settings."},
        default=None,
    )

    def __str__(self) -> str:
        return self.SETTING


@dataclass
class InterfaceSettings(BaseClass):
    """
    Dataclass to store a scanner appliance's interface settings.
    """

    INTERFACE: str = field(
        metadata={"description": "The interface."},
        default=None,
    )

    IP_ADDRESS: IPv4Address = field(
        metadata={"description": "The IP address."},
        default=None,
    )

    NETMASK: str = field(
        metadata={"description": "The netmask."},
        default=None,
    )

    GATEWAY: IPv4Address = field(
        metadata={"description": "The gateway."},
        default=None,
    )

    LEASE: str = field(
        metadata={"description": "The lease."},
        default=None,
    )

    SPEED: int = field(
        metadata={"description": "The speed."},
        default=None,
    )

    DUPLEX: str = field(
        metadata={"description": "The duplex."},
        default=None,
    )

    DNS: dict = field(
        metadata={"description": "The DNS settings."},
        default=None,
    )

    DNS_PRIMARY: IPv4Address = field(
        metadata={"description": "The primary DNS."},
        default=None,
    )

    DNS_SECONDARY: IPv4Address = field(
        metadata={"description": "The secondary DNS."},
        default=None,
    )

    SETTING: str = field(
        metadata={"description": "The setting."},
        default=None,
    )

    DOMAIN: str = field(
        metadata={"description": "The domain."},
        default=None,
    )

    def __post_init__(self):
        """
        Post init function to convert certain fields to int/float.
        """
        INT_FIELDS = ["SPEED"]
        IPV4_FIELDS = ["IP_ADDRESS", "GATEWAY"]

        for int_field in INT_FIELDS:
            if getattr(self, int_field):
                setattr(self, int_field, int(getattr(self, int_field)))

        for ip_field in IPV4_FIELDS:
            if getattr(self, ip_field):
                setattr(self, ip_field, IPv4Address(getattr(self, ip_field)))

        if self.DNS:
            self.DNS_PRIMARY = self.DNS.get("PRIMARY")
            self.DNS_SECONDARY = self.DNS.get("SECONDARY")
            self.DOMAIN = self.DNS.get("DOMAIN")
            del self.DNS

    def __str__(self):
        # Comma-separated string of non-empty values in k:v format
        return ", ".join(f"{k}:{v}" for k, v in self.valid_values().items() if v)

    def __repr__(self) -> str:
        # Only return non-empty values
        return (
            "InterfaceSettings("
            + ", ".join(f"{k}={v}" for k, v in self.valid_values().items())
            + ")"
        )

    def valid_values(self):
        return {k: v for k, v in asdict(self).items() if v}

    def __getitem__(self, key):
        return asdict(self)[key]

    def __setitem__(self, key, value):
        asdict(self)[key] = value
        return asdict(self)


@dataclass(order=True)
class ScannerAppliance(BaseClass):
    """
    Scanner Appliances in VMDR.
    """

    ID: int = field(
        metadata={"description": "Scanner Appliance ID."},
    )

    NAME: str = field(
        metadata={"description": "Scanner Appliance friendly name."},
        default=None,
    )

    SOFTWARE_VERSION: float = field(
        metadata={"description": "Software version of the scanner appliance."},
        default=None,
    )

    RUNNING_SCAN_COUNT: int = field(
        metadata={
            "description": "Number of scans currently running on the scanner appliance."
        },
        default=0,
    )

    STATUS: str = field(
        metadata={"description": "Status of the scanner appliance."},
        default=None,
    )

    UUID: uuid = field(
        metadata={"description": "UUID of the scanner appliance."},
        default=None,
    )

    RUNNING_SLICES_COUNT: int = field(
        metadata={
            "description": "Number of slices currently running on the scanner appliance."
        },
        default=0,
    )

    MODEL_NUMBER: str = field(
        metadata={"description": "Model number of the scanner appliance."},
        default=None,
    )

    TYPE: str = field(
        metadata={"description": "Type of scanner appliance."},
        default=None,
    )

    SERIAL_NUMBER: str = field(
        metadata={"description": "Serial number of the scanner appliance."},
        default=None,
    )

    ACTIVATION_CODE: int = field(
        metadata={"description": "Activation code of the scanner appliance."},
        default=None,
    )

    INTERFACE_SETTINGS: InterfaceSettings = field(
        metadata={"description": "Interface settings of the scanner appliance."},
        default=None,
    )

    PROXY_SETTINGS: ProxySettings = field(
        metadata={"description": "Proxy settings of the scanner appliance."},
        default=None,
    )

    IS_CLOUD_DEPLOYED: bool = field(
        metadata={"description": "Whether the scanner appliance is cloud deployed."},
        default=False,
    )

    CLOUD_INFO: ScannerCloudInfo = field(
        metadata={"description": "Cloud information of the scanner appliance."},
        default=None,
    )

    VLANS: dict = field(
        metadata={"description": "VLANs of the scanner appliance."},
        default=None,
    )

    STATIC_ROUTES: dict = field(
        metadata={"description": "Static routes of the scanner appliance."},
        default=None,
    )

    ML_LATEST: str = field(
        metadata={
            "description": "Latest machine learning model of the scanner appliance."
        },
        default=None,
    )

    ML_VERSION: dict = field(
        metadata={"description": "Machine learning version of the scanner appliance."},
        default=None,
    )

    VULNSIGS_LATEST: str = field(
        metadata={
            "description": "Latest vulnerability signature of the scanner appliance."
        },
        default=None,
    )

    VULNSIGS_VERSION: dict = field(
        metadata={
            "description": "Vulnerability signature version of the scanner appliance."
        },
        default=None,
    )

    ASSET_GROUP_COUNT: int = field(
        metadata={
            "description": "Number of asset groups associated with the scanner appliance."
        },
        default=0,
    )

    ASSET_GROUP_LIST: BaseList[AssetGroup] = field(
        metadata={
            "description": "List of asset groups associated with the scanner appliance."
        },
        default=None,
    )

    ASSET_TAGS_LIST: BaseList[Tag] = field(
        metadata={
            "description": "List of asset tags associated with the scanner appliance."
        },
        default=None,
    )

    LAST_UPDATED_DATE: datetime = field(
        metadata={"description": "Date the scanner appliance was last updated."},
        default=None,
    )

    POLLING_INTERVAL: int = field(
        metadata={"description": "Polling interval of the scanner appliance."},
        default=None,
    )

    USER_LOGIN: str = field(
        metadata={"description": "Owner account of the scanner appliance."},
        default=None,
    )

    HEARTBEATS_MISSED: int = field(
        metadata={
            "description": "Number of heartbeats missed by the scanner appliance."
        },
        default=None,
    )

    SS_CONNECTION: str = field(
        metadata={
            "description": "Status of the scanner appliance's connection to the Security Server."
        },
        default=None,
    )

    SS_LAST_CONNECTED: datetime = field(
        metadata={
            "description": "Date the scanner appliance last connected to the Security Server."
        },
        default=None,
    )

    USER_LIST: dict = field(
        metadata={
            "description": "List of users associated with the scanner appliance."
        },
        default=None,
    )

    UPDATED: bool = field(
        metadata={"description": "Whether the scanner appliance was updated."},
        default=None,
    )

    COMMENTS: str = field(
        metadata={"description": "Comments on the scanner appliance."},
        default=None,
    )

    MAX_CAPACITY_UNITS: int = field(
        metadata={"description": "Maximum capacity units of the scanner appliance."},
        default=None,
    )

    # BELOW ATTRIBUTES ARE PULLED UP A LEVEL FROM AN ABOVE ATTRIBUTE DICITONARY

    def __post_init__(self):
        """
        Post init function to convert certain fields to int/float.
        """
        INT_FIELDS = [
            "ID",
            "RUNNING_SCAN_COUNT",
            "RUNNING_SLICES_COUNT",
            "ACTIVATION_CODE",
            "ASSET_GROUP_COUNT",
            "POLLING_INTERVAL",
            "HEARTBEATS_MISSED",
            "MAX_CAPACITY_UNITS",
        ]
        DT_FIELDS = ["LAST_UPDATED_DATE", "SS_LAST_CONNECTED"]
        FLOAT_FIELDS = ["SOFTWARE_VERSION"]
        CUSTOM_DATACLASSES = [("ASSET_GROUP_LIST", "ag"), ("ASSET_TAGS_LIST", "tag")]

        for int_field in INT_FIELDS:
            if getattr(self, int_field):
                # Special case for polling interval. Split by space and take the first value.
                if int_field == "POLLING_INTERVAL":
                    setattr(self, int_field, int(getattr(self, int_field).split()[0]))
                else:
                    setattr(self, int_field, int(getattr(self, int_field)))

        for float_field in FLOAT_FIELDS:
            if getattr(self, float_field):
                setattr(self, float_field, float(getattr(self, float_field)))

        for dt_field in DT_FIELDS:
            if getattr(self, dt_field):
                setattr(
                    self,
                    dt_field,
                    datetime.strptime(getattr(self, dt_field), "%Y-%m-%dT%H:%M:%S%z"),
                )

        for custom_field in CUSTOM_DATACLASSES:
            if getattr(self, custom_field[0]):
                setattr(
                    self,
                    custom_field[0],
                    build_dataclass_baselist(
                        getattr(self, custom_field[0]), custom_field[1]
                    ),
                )

        if self.CLOUD_INFO:
            setattr(self, "CLOUD_INFO", ScannerCloudInfo.from_dict(self.CLOUD_INFO))

        # convert UUID:
        if self.UUID:
            setattr(self, "UUID", uuid(self.UUID))

        if self.UPDATED:
            setattr(self, "UPDATED", self.UPDATED == "Yes")

        # Convert IS_CLOUD_DEPLOYED to bool:
        if self.IS_CLOUD_DEPLOYED:
            setattr(self, "IS_CLOUD_DEPLOYED", self.IS_CLOUD_DEPLOYED == "1")

        if self.INTERFACE_SETTINGS:
            if isinstance(self.INTERFACE_SETTINGS, dict):
                setattr(
                    self,
                    "INTERFACE_SETTINGS",
                    InterfaceSettings.from_dict(self.INTERFACE_SETTINGS),
                )
            else:
                setattr(
                    self,
                    "INTERFACE_SETTINGS",
                    BaseList(
                        [
                            InterfaceSettings.from_dict(item)
                            for item in self.INTERFACE_SETTINGS
                        ]
                    ),
                )

        if self.PROXY_SETTINGS:
            if isinstance(self.PROXY_SETTINGS, dict):
                setattr(
                    self, "PROXY_SETTINGS", ProxySettings.from_dict(self.PROXY_SETTINGS)
                )
            else:
                setattr(
                    self,
                    "PROXY_SETTINGS",
                    BaseList(
                        [ProxySettings.from_dict(item) for item in self.PROXY_SETTINGS]
                    ),
                )

    def __str__(self):
        return self.NAME

    def __int__(self):
        return self.ID

    def __getitem__(self, key):
        return asdict(self)[key]

    def __setitem__(self, key, value):
        asdict(self)[key] = value
        return asdict(self)

    def valid_values(self):
        return {k: v for k, v in asdict(self).items() if v}
