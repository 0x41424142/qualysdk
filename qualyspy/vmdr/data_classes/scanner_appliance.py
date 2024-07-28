"""
scanner_appliance.py - Contains the ScannerAppliance data class.
"""

from dataclasses import dataclass, field, asdict
from uuid import UUID as uuid
from datetime import datetime

from .lists.base_list import BaseList
from .asset_group import AssetGroup
from .tag import Tag


@dataclass(order=True)
class ScannerAppliance:
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

    INTERFACE_SETTINGS: dict = field(
        metadata={"description": "Interface settings of the scanner appliance."},
        default=None,
    )

    PROXY_SETTINGS: dict = field(
        metadata={"description": "Proxy settings of the scanner appliance."},
        default=None,
    )

    IS_CLOUD_DEPLOYED: bool = field(
        metadata={"description": "Whether the scanner appliance is cloud deployed."},
        default=False,
    )

    CLOUD_INFO: dict = field(
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

        for field in INT_FIELDS:
            if getattr(self, field) not in ["", [], {}, None]:
                # Special case for polling interval. Split by space and take the first value.
                if field == "POLLING_INTERVAL":
                    setattr(self, field, int(getattr(self, field).split()[0]))
                else:
                    setattr(self, field, int(getattr(self, field)))

        for field in FLOAT_FIELDS:
            if getattr(self, field) is not None:
                setattr(self, field, float(getattr(self, field)))

        for field in DT_FIELDS:
            if getattr(self, field) is not None:
                setattr(
                    self,
                    field,
                    datetime.strptime(getattr(self, field), "%Y-%m-%dT%H:%M:%S%z"),
                )

        # convert UUID:
        if self.UUID is not None:
            setattr(self, "UUID", uuid(self.UUID))

        # Convert IS_CLOUD_DEPLOYED to bool:
        if self.IS_CLOUD_DEPLOYED is not None:
            setattr(self, "IS_CLOUD_DEPLOYED", self.IS_CLOUD_DEPLOYED == "1")

    def __str__(self):
        return self.NAME

    def __int__(self):
        return self.ID

    def __dict__(self):
        return asdict(self)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    def __getitem__(self, key):
        return asdict(self)[key]

    def __setitem__(self, key, value):
        asdict(self)[key] = value
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return asdict(self)

    def valid_values(self):
        return {
            k: v
            for k, v in asdict(self).items()
            if v is not None and v != "" and v != []
        }
