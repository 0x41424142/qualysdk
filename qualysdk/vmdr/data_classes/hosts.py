"""
hosts.py - contains the VMDRHosts class for the qualysdk package.
"""

from dataclasses import dataclass, field, asdict
from typing import *
from datetime import datetime

from ipaddress import IPv4Address, IPv6Address

from ...base.base_list import BaseList
from .tag import Tag, CloudTag
from .detection import Detection


@dataclass(order=True)
class VMDRHost:
    """
    Host - represents a Qualys VMDR host record.
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

    LAST_SCAN_DATETIME: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last scan date of the host."},
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

    LAST_PC_SCANNED_DATE: Union[str, datetime] = field(
        default=None,
        metadata={"description": "The last PC scanned date of the host."},
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

    DETECTION_LIST: Optional[BaseList[Detection]] = field(
        default=None,
        metadata={"description": "The detection list of the host."},
        compare=False,
    )

    ASSET_RISK_SCORE: Optional[Union[str, int]] = field(
        default=None,
        metadata={"description": "The asset risk score of the host."},
        compare=False,
    )

    TRURISK_SCORE: Optional[Union[str, int]] = field(
        default=None,
        metadata={"description": "The TruRisk score of the host."},
        compare=False,
    )

    TRURISK_SCORE_FACTORS: Optional[dict] = field(
        default=None,
        metadata={"description": "The TruRisk score factors of the host."},
        compare=False,
    )

    ASSET_CRITICALITY_SCORE: Optional[Union[str, int]] = field(
        default=None,
        metadata={"description": "The asset criticality score of the host."},
        compare=False,
    )

    CLOUD_GROUP_NAME: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud group name of the host."},
        compare=False,
    )

    CLOUD_INSTANCE_STATE: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud instance state of the host."},
        compare=False,
    )

    CLOUD_INSTANCE_TYPE: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud instance type of the host."},
        compare=False,
    )

    CLOUD_IS_SPOT_INSTANCE: Optional[bool] = field(
        default=None,
        metadata={"description": "The cloud is spot instance of the host."},
        compare=False,
    )

    CLOUD_ARCHITECTURE: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud architecture of the host."},
        compare=False,
    )

    CLOUD_IMAGE_ID: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud image ID of the host."},
        compare=False,
    )

    CLOUD_REGION: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud region of the host."},
        compare=False,
    )

    CLOUD_AMI_ID: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud AMI ID of the host."},
        compare=False,
    )

    CLOUD_PUBLIC_HOSTNAME: Optional[str] = field(
        default=None,
        metadata={"description": "The cloud public hostname of the host."},
        compare=False,
    )

    CLOUD_PUBLIC_IPV4: Optional[Union[str, IPv4Address]] = field(
        default=None,
        metadata={"description": "The cloud public IPv4 of the host."},
        compare=False,
    )

    CLOUD_ACCOUNT_ID: Optional[Union[str, int]] = field(
        default=None,
        metadata={"description": "The cloud account ID of the host."},
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
            "LAST_SCAN_DATETIME",
            "LAST_VULN_SCAN_DATETIME",
            "LAST_VM_SCANNED_DATE",
            "LAST_VM_AUTH_SCANNED_DATE",
            "LAST_VM_AUTH_SCANNED_DATE",
            "LAST_COMPLIANCE_SCAN_DATETIME",
            "LAST_VULN_SCAN_DATE",
            "LAST_ACTIVITY",
            "LAST_PC_SCANNED_DATE",
        ]
        INT_FIELDS = [
            "ID",
            "ASSET_ID",
            "LAST_VM_SCANNED_DURATION",
            "ASSET_RISK_SCORE",
            "TRURISK_SCORE",
            "ASSET_CRITICALITY_SCORE",
        ]

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

        if self.TRURISK_SCORE_FACTORS:
            s = ""
            for sev_level in self.TRURISK_SCORE_FACTORS.get("VULN_COUNT"):
                s += f"sev_{sev_level.get('@qds_severity')}: {sev_level.get('#text')}, "
            # Pinch off the trailing comma and space:
            s = s[:-2]
            self.TRURISK_SCORE_FACTORS = s

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
                ("ACCOUNT_ID", "latest/dynamic/instance-identity/document/accountId"),
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
                            setattr(
                                self,
                                f"CLOUD_{key[0]}",
                                (
                                    item["VALUE"]
                                    if item["VALUE"] not in ["", {}, []]
                                    else None
                                ),
                            )  # if item['VALUE'] seems to leave behind empties, hence the list
                            break
                else:
                    if (
                        self.METADATA[key_selector]["ATTRIBUTE"]["NAME"]
                        and self.METADATA[key_selector]["ATTRIBUTE"]["NAME"] == key
                    ):
                        setattr(
                            self,
                            f"CLOUD_{key[0]}",
                            self.METADATA[key_selector]["ATTRIBUTE"]["VALUE"],
                        )

        for INT_FIELD in INT_FIELDS:
            if getattr(self, INT_FIELD) and not isinstance(
                getattr(self, INT_FIELD), int
            ):
                setattr(self, INT_FIELD, int(getattr(self, INT_FIELD)))

        if self.CLOUD_PUBLIC_IPV4 and not isinstance(
            self.CLOUD_PUBLIC_IPV4, IPv4Address
        ):
            self.CLOUD_PUBLIC_IPV4 = IPv4Address(self.CLOUD_PUBLIC_IPV4)

        if self.CLOUD_IS_SPOT_INSTANCE:
            self.CLOUD_IS_SPOT_INSTANCE = bool(self.CLOUD_IS_SPOT_INSTANCE)

        # check for a detections list and convert it to a BaseList of Detection objects (used in hld):
        if self.DETECTION_LIST:
            detections_bl = BaseList()
            data = self.DETECTION_LIST["DETECTION"]

            if isinstance(data, dict):
                data = [data]

            for detection in data:
                # Append the host's ID attr to the detection dictionary
                # to allow for a relationship:
                detection["ID"] = self.ID
                detections_bl.append(Detection.from_dict(detection))

            self.DETECTION_LIST = detections_bl

    def __str__(self) -> str:
        """
        String representation of the host object.
        """
        return str(self.ID)

    def __int__(self) -> int:
        return self.ID

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
        for key, value in self.to_dict().items():
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
        return VMDRHost.from_dict(self.to_dict())

    def valid_values(self) -> list:
        """
        Return a list of keys that have values.
        """
        return {k: v for k, v in self.items() if v}

    def to_dict(self) -> dict:
        """
        Convert the host object to a dictionary.
        """
        return asdict(self)

    def __dict__(self) -> dict:
        """
        Convert the host object to a dictionary.
        """
        return asdict(self)

    def keys(self) -> list:
        """
        Return the keys of the host object.
        """
        return self.to_dict().keys()

    def values(self) -> list:
        """
        Return the values of the host object.
        """
        return self.to_dict().values()

    def items(self) -> list:
        """
        Return the items of the host object.
        """
        return self.to_dict().items()

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

        self.ID = int(self.ID)

    def __str__(self) -> str:
        return str(self.ID)

    def __int__(self) -> int:
        return self.ID

    def __repr__(self) -> str:
        if self.TYPE == "asset":
            return f"VMDRID({self.ID}, type='asset')"
        else:
            return f"VMDRID({self.ID}, type='host')"

    def __dict__(self) -> dict:
        return asdict(self)

    def to_dict(self) -> dict:
        return asdict(self)

    def __iter__(self):
        """
        Iterate over the fields of the host object.
        """
        for key, value in self.to_dict().items():
            yield key, value

    def values(self):
        """
        Return the values of the object.
        """
        return self.to_dict().values()

    def keys(self):
        """
        Return the keys of the object.
        """
        return self.to_dict().keys()

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
