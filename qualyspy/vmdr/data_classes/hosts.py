"""
hosts.py - contains the VMDRHosts class for the Qualyspy package.
"""

from dataclasses import dataclass, field
from typing import *
from datetime import datetime

from ipaddress import IPv4Address, IPv6Address

from .lists import BaseList
from .tag import Tag, CloudTag
from .detection import Detection


@dataclass(order=True)
class VMDRHost:
    """
    Host - represents a Qualys GAV host record.

    due to the fact that some APIs have excludeFields and IncludeFields parameters,
    virtually all fields are optional other than assetId.
    """

    ID: Union[str, int] = field(
        default=None, metadata={"description": "The HOST ID of the host."}
    )  # this is the host ID, not the asset ID. add to post init to cast to int
    ASSET_ID: Union[str, int] = field(
        default=None, metadata={"description": "The asset ID of the host."}
    )  # add to post init to cast to int
    IP: Union[str, IPv4Address] = field(
        default=None,
        metadata={"description": "The IP address of the host."},
        compare=False,
    )
    IPV6: Union[str, IPv6Address] = field(
        default=None,
        metadata={"description": "The IPv6 address of the host."},
        compare=False,
    )
    TRACKING_METHOD: str = field(
        default=None,
        metadata={"description": "The tracking method of the host."},
        compare=False,
    )
    DNS: str = field(
        default=None,
        metadata={"description": "The DNS name of the host."},
        compare=False,
    )

    # DNS_DATA is a dictionary containing the keys HOSTNAME, DOMAIN, and FQDN. We will make these keys attributes of the class.
    DNS_DATA: Dict[str, str] = field(
        default=None,
        metadata={"description": "The DNS data of the host."},
        compare=False,
    )

    NETBIOS: str = field(
        default=None,
        metadata={"description": "The NetBIOS name of the host."},
        compare=False,
    )
    OS: str = field(
        default=None,
        metadata={"description": "The operating system of the host."},
        compare=False,
    )
    QG_HOSTID: str = field(
        default=None, metadata={"description": "The QualysGuard host ID of the host."}
    )
    LAST_BOOT: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last boot time of the host."},
        compare=False,
    )  # add to post init to cast to datetime
    SERIAL_NUMBER: str = field(
        default=None,
        metadata={"description": "The serial number of the host."},
        compare=False,
    )
    HARDWARE_UUID: str = field(
        default=None, metadata={"description": "The hardware UUID of the host."}
    )
    FIRST_FOUND_DATE: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The first found date of the host."},
        compare=False,
    )  # add to post init to cast to datetime
    LAST_ACTIVITY: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last activity date of the host."},
        compare=False,
    )
    LAST_ACTIVITY_DATE: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last activity date of the host."},
        compare=False,
    )  # add to post init to cast to datetime
    AGENT_STATUS: str = field(
        default=None,
        metadata={"description": "The agent status of the host."},
        compare=False,
    )
    CLOUD_AGENT_RUNNING_ON: str = field(
        default=None,
        metadata={"description": "The cloud agent running on of the host."},
        compare=False,
    )
    TAGS: Union[dict, BaseList] = field(
        default=None, metadata={"description": "The tags of the host."}, compare=False
    )  # add to post init to convert to BaseList (look at GAV lists for how to do this), as well as make a Tag class
    LAST_VULN_SCAN_DATETIME: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last vulnerability scan date of the host."},
        compare=False,
    )  # add to post init to cast to datetime
    LAST_VULN_SCAN_DATE: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last vulnerability scan date of the host."},
        compare=False,
    )  # add to post init to cast to datetime
    LAST_VM_SCANNED_DATE: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last VM scan date of the host."},
        compare=False,
    )
    LAST_VM_AUTH_SCANNED_DURATION: Union[str, int] = field(
        default=None,
        metadata={"description": "The last VM scanned duration of the host."},
        compare=False,
    )  # add to post init to cast to int
    LAST_VM_SCANNED_DURATION: Union[str, int] = field(
        default=None,
        metadata={"description": "The last VM scanned duration of the host."},
        compare=False,
    )  # add to post init to cast to int
    LAST_VM_AUTH_SCANNED_DATE: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last VM auth scanned date of the host."},
        compare=False,
    )  # add to post init to cast to datetime
    LAST_COMPLIANCE_SCAN_DATETIME: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last compliance scan date of the host."},
        compare=False,
    )  # add to post init to cast to datetime
    ASSET_GROUP_IDS: List[str] = field(
        default=None,
        metadata={"description": "The asset group IDs of the host."},
        compare=False,
    )
    USER_DEF: dict = field(
        default=None,
        metadata={"description": "The user def of the host."},
        compare=False,
    )
    OWNER: str = field(
        default=None, metadata={"description": "The owner of the host."}, compare=False
    )

    # CLOUD HOST FIELDS:
    CLOUD_PROVIDER: str = field(
        default=None,
        metadata={"description": "The cloud provider of the host."},
        compare=False,
    )
    CLOUD_SERVICE: str = field(
        default=None,
        metadata={"description": "The cloud service of the host."},
        compare=False,
    )
    CLOUD_RESOURCE_ID: str = field(
        default=None,
        metadata={"description": "The cloud resource ID of the host."},
        compare=False,
    )
    EC2_INSTANCE_ID: str = field(
        default=None,
        metadata={"description": "The EC2 instance ID of the host."},
        compare=False,
    )
    CLOUD_PROVIDER_TAGS: Union[dict, BaseList] = field(
        default=None,
        metadata={"description": "The cloud provider tags of the host."},
        compare=False,
    )

    # this METADATA field contains a lot of nested data, so we will need to parse it out in post init. The immediate key underneath is the cloud service, i.e. EC2, AZURE, etc.
    # and gets parsed in post init.
    METADATA: dict = field(
        default=None,
        metadata={"description": "The metadata of the host."},
        compare=False,
    )

    # DETECTION LIST FIELDS:
    DETECTION_LIST: Optional[Union[list[Detection], BaseList[Detection]]] = field(
        default=None,
        metadata={"description": "The detection list of the host."},
        compare=False,
    ) 

    def __post_init__(self):
        """
        Pull up nested dict values as attributes, convert IPs,
        put tags in a BaseList and convert strings to datetime objects.
        """
        DNS_DATA_FIELDS = ["HOSTNAME", "DOMAIN", "FQDN"]
        DATETIME_FIELDS = [
            "LAST_BOOT",
            "FIRST_FOUND_DATE",
            "LAST_ACTIVITY_DATE",
            "LAST_VULN_SCAN_DATETIME",
            "LAST_VM_SCANNED_DATE",
            "LAST_VM_AUTH_SCANNED_DATE",
            "LAST_VM_AUTH_SCANNED_DATE",
            "LAST_COMPLIANCE_SCAN_DATETIME",
            "LAST_VULN_SCAN_DATE",
            "LAST_ACTIVITY",
        ]
        INT_FIELDS = [
            "ID",
            "ASSET_ID",
            "LAST_VM_SCANNED_DURATION",
        ]  # (cloud) ACCOUNT_ID cannot go here as it is not initialized yet

        if self.DNS_DATA:
            for field in DNS_DATA_FIELDS:
                setattr(self, field, self.DNS_DATA.get(field))

        if self.IP and not isinstance(self.IP, IPv4Address):
            self.IP = IPv4Address(self.IP)

        if self.IPV6 and not isinstance(self.IPV6, IPv6Address):
            self.IPV6 = IPv6Address(self.IPV6)

        for DATE_FIELD in DATETIME_FIELDS:
            if getattr(self, DATE_FIELD) and not isinstance(
                getattr(self, DATE_FIELD), datetime
            ):
                setattr(
                    self, DATE_FIELD, datetime.fromisoformat(getattr(self, DATE_FIELD))
                )

        for INT_FIELD in INT_FIELDS:
            if getattr(self, INT_FIELD) and not isinstance(
                getattr(self, INT_FIELD), int
            ):
                setattr(self, INT_FIELD, int(getattr(self, INT_FIELD)))

        if self.TAGS:
            # if 'TAG' key's value is a list, it is a list of tag dicts. if it is a single tag dict, it is just a single tag.
            if isinstance(self.TAGS["TAG"], list):
                self.TAGS = BaseList([Tag.from_dict(tag) for tag in self.TAGS["TAG"]])
            else:  # if it is a single tag dict:
                self.TAGS = BaseList([Tag.from_dict(self.TAGS["TAG"])])

        if self.CLOUD_PROVIDER_TAGS:
            # if 'CLOUD_TAG' key's value is a list, it is a list of tag dicts. if it is a single tag dict, it is just a single tag.
            if isinstance(self.CLOUD_PROVIDER_TAGS["CLOUD_TAG"], list):
                self.CLOUD_PROVIDER_TAGS = BaseList(
                    [
                        CloudTag.from_dict(tag)
                        for tag in self.CLOUD_PROVIDER_TAGS["CLOUD_TAG"]
                    ]
                )
            else:  # if it is a single tag dict:
                self.CLOUD_PROVIDER_TAGS = BaseList(
                    [CloudTag.from_dict(self.CLOUD_PROVIDER_TAGS["CLOUD_TAG"])]
                )

        # CLOUD SPECIFIC FIELDS:
        if self.METADATA:
            match self.CLOUD_PROVIDER:
                case "AWS":
                    key_selector = "EC2"
                case "Azure":
                    key_selector = "AZURE"
                case "GCP":
                    key_selector = "GCP"
                case _:
                    raise ValueError(
                        f"Cloud provider {self.CLOUD_PROVIDER} is not supported."
                    )

            # for each tuple, [0] is the dataclass attribute name, [1] is how it is represented in the metadata dict.
            VALID_EC2_KEYS = [
                ("GROUP_NAME", "groupName"),
                ("INSTANCE_STATE", "instanceState"),
                ("INSTANCE_TYPE", "latest/meta-data/instance-type"),
                ("IS_SPOT_INSTANCE", "isSpotInstance"),
                (
                    "ARCHITECTURE",
                    "latest/dynamic/instance-identity/document/architecture",
                ),
                ("IMAGE_ID", "latest/dynamic/instance-identity/document/imageId"),
                ("REGION", "latest/dynamic/instance-identity/document/region"),
                ("AMI_ID", "latest/meta-data/ami-id"),
                ("PUBLIC_HOSTNAME", "latest/meta-data/public-hostname"),
                ("PUBLIC_IPV4", "latest/meta-data/public-ipv4"),
                ("ACCOUNT_ID", "asset.aws.ec2.accountId"),
            ]
            VALID_AZURE_KEYS = [
                ("PUBLIC_IPV4", "latest/meta-data/public-ipv4"),
                ("INSTANCE_STATE", "state"),
                ("GROUP_NAME", "resourceGroupName"),
                ("INSTANCE_TYPE", "vmSize"),
                ("REGION", "location"),
                ("ACCOUNT_ID", "subscriptionId"),
            ]
            VALID_GCP_KEYS = ...
            # map key_selector to the valid keys list:
            VALID_KEYS = {
                "EC2": VALID_EC2_KEYS,
                "AZURE": VALID_AZURE_KEYS,
                # "GCP": VALID_GCP_KEYS #not implemented as i have no access to a GCP environment.
            }

            for key in VALID_KEYS[key_selector]:
                # check for if self.METADATA[key_selector]['ATTRIBUTE'] is a list of dicts. if not, it is just a single dict.
                if isinstance(self.METADATA[key_selector]["ATTRIBUTE"], list):
                    for item in self.METADATA[key_selector]["ATTRIBUTE"]:
                        if item["NAME"] == key[1]:
                            setattr(self, f"CLOUD_{key[0]}", item["VALUE"])
                else:
                    if self.METADATA[key_selector]["ATTRIBUTE"]["NAME"] == key:
                        setattr(
                            self,
                            f"CLOUD_{key[0]}",
                            self.METADATA[key_selector]["ATTRIBUTE"]["VALUE"],
                        )

            #check for a detections list and convert it to a BaseList of Detection objects (used in hld):
            if self.DETECTION_LIST:
                if isinstance(self.DETECTION_LIST["DETECTION"], list):
                    self.DETECTION_LIST = BaseList(
                        [Detection.from_dict(detection) for detection in self.DETECTION_LIST["DETECTION"]]
                    )
                else:
                    self.DETECTION_LIST = BaseList(
                        [Detection.from_dict(self.DETECTION_LIST["DETECTION"])]
                    )

    def __str__(self) -> str:
        """
        String representation of the host object.
        """
        if self.ASSET_ID:
            return f"Host({self.ASSET_ID})"
        elif self.ID:
            return f"Host({self.ID})"
        else:
            # fall back to QG_HostID:
            return f"Host({self.QG_HOSTID})"
        
    def __int__(self) -> int:
        if self.ASSET_ID:
            return self.ASSET_ID
        elif self.ID:
            return self.ID
        else:
            raise ValueError("Host object does not have an asset ID or host ID.")

    def __repr__(self) -> str:
        """
        Breaking the unwritten rule of having repr be something
        that can create the object for terminal space's sake.
        """
        if self.ASSET_ID:
            return f"Host({self.ASSET_ID})"
        elif self.ID:
            return f"Host({self.ID})"
        else:
            # fall back to QG_HostID:
            return f"Host({self.QG_HOSTID})"

    def __iter__(self):
        """
        Allows for iteration over the host object.
        """
        for key, value in self.__dict__.items():
            yield key, value

    def has_agent(self) -> bool:
        """
        Check if the host has an agent.
        """
        return self.QG_HOSTID is not None

    def is_cloud_host(self) -> bool:
        """
        Check if the host is a cloud host.
        """
        return self.CLOUD_PROVIDER is not None

    def is_aws(self) -> bool:
        """
        Check if the host is an AWS host.
        """
        return self.CLOUD_PROVIDER == "AWS"

    def is_azure(self) -> bool:
        """
        Check if the host is an Azure host.
        """
        return self.CLOUD_PROVIDER == "Azure"

    def copy(self) -> "VMDRHost":
        """
        Create a copy of the host object.
        """
        return VMDRHost(**self.__dict__)

    def valid_values(self) -> list:
        """
        Return a list of keys that have values.
        """
        return [key for key, value in self.__dict__.items() if value is not None]

    @classmethod
    def from_dict(cls, data: dict) -> "VMDRHost":
        """
        Create a VMDRHost object from a dictionary.
        """
        return cls(**data)


@dataclass
class VMDRID:
    """
    ID - represents a Qualys GAV ID record.

    This class is used to represent a Qualys GAV ID record, either a host ID or an asset ID.
    This class is only ever used if details=None in a get_host_list or get_host_list_detections API call.
    """

    ID: Union[str, int] = field(
        metadata={"description": "The asset ID of the host."}
    )  # add to post init to cast to int
    TYPE: Literal["asset", "host"] = field(
        metadata={"description": "The type of ID. Valid values are 'asset' or 'host'."},
        compare=False,
    )  # field is required!

    def __post_init__(self):
        """
        Cast the asset ID and host ID to integers if they are not None.
        """

        if not self.ID:
            raise ValueError("ID attribute cannot be None.")

        if self.TYPE == "asset" and self.ID:
            self.ID = int(self.ID)
        elif self.TYPE == "host" and self.ID:
            self.ID = int(self.ID)
        else:
            raise ValueError(
                f"TYPE attribute must be 'asset' or 'host, not {self.TYPE}'"
            )

    def __str__(self) -> str:
        return str(self.ID)
    
    def __int__(self) -> int:
        return self.ID

    def __repr__(self) -> str:
        if self.TYPE == "asset":
            return f"VMDRID({self.ID}, type='asset')"
        else:
            return f"VMDRID({self.ID}, type='host')"

    def __iter__(self):
        """
        Iterate over the fields of the host object.
        """
        for key, value in self.__dict__.items():
            yield key, value

    def values(self):
        """
        Return the values of the object.
        """
        return self.__dict__.values()

    def keys(self):
        """
        Return the keys of the object.
        """
        return self.__dict__.keys()

    @classmethod
    def from_dict(cls, data: dict) -> "VMDRID":
        """
        Create a VMDRID object from a dictionary.
        """
        required_keys = {"ID", "TYPE"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        return cls(**data)
