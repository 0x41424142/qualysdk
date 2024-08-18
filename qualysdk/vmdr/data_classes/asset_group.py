"""
asset_group.py - contains the AssetGroup dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *
from datetime import datetime
from ipaddress import (
    IPv4Address,
    IPv6Address,
    IPv4Network,
    IPv6Network,
)

from .ip_converters import *
from .hosts import VMDRID
from ...base.base_list import BaseList


@dataclass(order=True)
class AssetGroup:
    """
    AssetGroup - represents a single asset group in Qualys.
    """

    ID: int = field(metadata={"description": "The ID of the asset group."})
    TITLE: Optional[str] = field(
        metadata={"description": "The title of the asset group."}, default=""
    )
    # NOTE: OWNER_ID contains either the raw XML's OWNER_ID or OWNER_USER_ID depending on value passed to get_ag_list(attributes=<>).
    OWNER_ID: Optional[int] = field(
        metadata={"description": "The ID of the owner of the asset group."},
        default=None,
    )
    OWNER_USER_ID: Optional[int] = field(
        metadata={"description": "The ID of the owner user of the asset group."},
        default=None,
    )
    UNIT_ID: Optional[int] = field(
        metadata={"description": "The ID of the unit of the asset group."}, default=None
    )
    LAST_UPDATE: Optional[Union[str, datetime]] = field(
        metadata={"description": "The datetime the asset group was last updated."},
        default=None,
    )
    NETWORK_ID: Optional[int] = field(
        metadata={
            "description": "The ID of the network of the asset group, if enabled in Qualys."
        },
        default=None,
    )
    IP_SET: Optional[
        BaseList[Union[IPv4Address, IPv6Address, IPv4Network, IPv6Network]]
    ] = field(
        metadata={"description": "The IP set of the asset group."},
        default=None,
    )
    BUSINESS_IMPACT: Optional[str] = field(
        metadata={"description": "The business impact of the asset group."},
        default=None,
    )
    DEFAULT_APPLIANCE_ID: Optional[int] = field(
        metadata={"description": "The default appliance ID of the asset group."},
        default=None,
    )
    APPLIANCE_IDS: Optional[BaseList[int]] = field(
        metadata={"description": "The appliance IDs of the asset group."},
        default=None,
    )
    DNS_LIST: Optional[BaseList[str]] = field(
        metadata={"description": "The DNS list of the asset group."},
        default=None,
    )
    NETBIOS_LIST: Optional[BaseList[str]] = field(
        metadata={"description": "The NetBIOS list of the asset group."},
        default=None,
    )
    HOST_IDS: Optional[BaseList[VMDRID]] = field(
        metadata={
            "description": "The host IDs of the asset group. BaseList of VMDRID objects."
        },
        default=None,
    )
    ASSIGNED_USER_IDS: Optional[BaseList[int]] = field(
        metadata={"description": "The assigned user IDs of the asset group."},
        default=None,
    )
    ASSIGNED_UNIT_IDS: Optional[BaseList[int]] = field(
        metadata={"description": "The assigned unit IDs of the asset group."},
        default=None,
    )
    OWNER_USER_NAME: Optional[str] = field(
        metadata={"description": "The owner user name of the asset group."},
        default=None,
    )
    CVSS_ENVIRO_CDP: Optional[str] = field(
        metadata={"description": "The CVSS environmental CDP of the asset group."},
        default=None,
    )
    CVSS_ENVIRO_TD: Optional[str] = field(
        metadata={"description": "The CVSS environmental TD of the asset group."},
        default=None,
    )
    CVSS_ENVIRO_CR: Optional[str] = field(
        metadata={"description": "The CVSS environmental CR of the asset group."},
        default=None,
    )
    CVSS_ENVIRO_IR: Optional[str] = field(
        metadata={"description": "The CVSS environmental IR of the asset group."},
        default=None,
    )
    CVSS_ENVIRO_AR: Optional[str] = field(
        metadata={"description": "The CVSS environmental AR of the asset group."},
        default=None,
    )
    EC2_IDS: Optional[BaseList[str]] = field(
        metadata={"description": "The EC2 IDs of the asset group."},
        default=None,
    )
    COMMENTS: Optional[BaseList[str]] = field(
        metadata={"description": "The comments of the asset group."},
        default=None,
    )
    DOMAIN_LIST: Optional[BaseList[str]] = field(
        metadata={"description": "The domain list of the asset group."},
        default=None,
    )

    def __post_init__(self):
        # Thanks Qualys for the inconsistency in naming conventions:
        if self.OWNER_USER_ID:
            self.OWNER_ID = self.OWNER_USER_ID
            del self.OWNER_USER_ID

        # Do data conversions:
        INT_FIELDS = ["ID", "OWNER_ID", "UNIT_ID", "NETWORK_ID", "DEFAULT_APPLIANCE_ID"]
        DT_FIELDS = ["LAST_UPDATE"]
        INT_LISTS = ["APPLIANCE_IDS", "ASSIGNED_USER_IDS", "ASSIGNED_UNIT_IDS"]
        STR_LISTS = ["DNS_LIST", "NETBIOS_LIST", "EC2_IDS", "COMMENTS", "DOMAIN_LIST"]

        for field in STR_LISTS:
            if getattr(self, field):
                setattr(self, field, BaseList(getattr(self, field).split(",")))

        for field in INT_LISTS:
            if getattr(self, field):
                if isinstance(getattr(self, field), str):
                    setattr(
                        self,
                        field,
                        BaseList([int(x) for x in getattr(self, field).split(",")]),
                    )
                else:
                    setattr(
                        self, field, BaseList([int(x) for x in getattr(self, field)])
                    )

        for field in DT_FIELDS:
            if getattr(self, field):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        for field in INT_FIELDS:
            if getattr(self, field):
                setattr(self, field, int(getattr(self, field)))

        # Convert IP_SET to BaseList of ipaddress.* objs.:
        if self.IP_SET:
            final_ip_set = BaseList()
            if self.IP_SET.get("IP_RANGE"):
                if isinstance(self.IP_SET.get("IP_RANGE"), str):
                    # We can use single_range here because it's a single IP range.
                    final_ip_set.extend([single_range(self.IP_SET.get("IP_RANGE"))])
                else:
                    # We can use convert_ranges here because it's a list of IP ranges.
                    final_ip_set.extend(convert_ranges(self.IP_SET.get("IP_RANGE")))

            if self.IP_SET.get("IP"):
                if isinstance(self.IP_SET.get("IP"), str):
                    # We can use single_ip here because it's a single IP.
                    final_ip_set.extend([single_ip(self.IP_SET.get("IP"))])
                else:
                    # We can use convert_ips here because it's a list of IPs.
                    final_ip_set.extend(convert_ips(self.IP_SET.get("IP")))

            self.IP_SET = final_ip_set

        # Convert HOST_IDS to BaseList of VMDRID objs.:
        if self.HOST_IDS:
            final_host_ids = BaseList()
            if isinstance(self.HOST_IDS, str):
                final_host_ids.extend(
                    [
                        VMDRID(ID=host_id, TYPE="host")
                        for host_id in self.HOST_IDS.split(",")
                    ]
                )
            else:
                final_host_ids.extend(
                    [VMDRID(ID=host_id, TYPE="host") for host_id in self.HOST_IDS]
                )

            self.HOST_IDS = final_host_ids

    def __str__(self):
        return self.TITLE

    def __contains__(self, item):
        return (
            item in self.ID
            or item in self.TITLE
            or item in self.OWNER_ID
            or item in self.UNIT_ID
            or item in self.NETWORK_ID
            or item in self.IP_SET
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def copy(self):
        return AssetGroup(
            ID=self.ID,
            TITLE=self.TITLE,
            OWNER_ID=self.OWNER_ID,
            UNIT_ID=self.UNIT_ID,
            NETWORK_ID=self.NETWORK_ID,
            IP_SET=self.IP_SET,
        )

    def is_id(self, id: int):
        return self.ID == id

    def is_title(self, title: str):
        return self.TITLE == title

    def is_owner_id(self, owner_id: int):
        return self.OWNER_ID == owner_id

    def is_unit_id(self, unit_id: int):
        return self.UNIT_ID == unit_id

    def is_network_id(self, network_id: int):
        return self.NETWORK_ID == network_id

    def contains_ip(
        self, ip: Union[IPv4Address, IPv6Address, IPv4Network, IPv6Network]
    ):
        return ip in self.IP_SET

    def add_ip(self, ip: Union[IPv4Address, IPv6Address, IPv4Network, IPv6Network]):
        self.IP_SET.append(ip)

    def remove_ip(self, ip: Union[IPv4Address, IPv6Address, IPv4Network, IPv6Network]):
        self.IP_SET.remove(ip)

    def valid_values(self):
        """
        Return a dictionary of non-None attributes.
        """
        return {
            key: value
            for key, value in self.to_dict().items()
            if value is not None and value != [] and value != ""
        }

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    def to_dict(self):
        """
        to_dict - convert the AssetGroup object to a dictionary.

        This function is used to convert the AssetGroup object to a dictionary.
        """
        return asdict(self)

    def __dict__(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - create an AssetGroup object from a dictionary.

        This function is used to create an AssetGroup object from a dictionary.
        """
        required_keys = {"ID", "TITLE"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        return cls(**data)

    def to_sql(self) -> dict:
        """
        Prepare the dataclass for insertion into a SQL database
        by converting it to a dictionary with appropriate list
        and datetime conversions.
        """

        # TODO: NOTE: INSTEAD OF ASDICT, MAYBE TRY ACCESSING THE ATTRIBUTES DIRECTLY, MODIFYING THEM, AND THEN DOING ASDICT???
        # NOTE: ABOVE WORKS. DO IT.
        LIST_FIELDS = [
            "IP_SET",
            "APPLIANCE_IDS",
            "DNS_LIST",
            "HOST_IDS",
            "NETBIOS_LIST",
            "ASSIGNED_USER_IDS",
            "ASSIGNED_UNIT_IDS",
            "EC2_IDS",
            "COMMENTS",
            "DOMAIN_LIST",
        ]

        # Iterate over the attrs of the dataclass and convert them to the appropriate format for SQL insertion.

        for attr in self.__dataclass_fields__.keys():
            if getattr(self, attr):
                if attr in LIST_FIELDS:
                    setattr(self, attr, str(getattr(self, attr)))

        sql_dict = self.to_dict()

        return sql_dict
