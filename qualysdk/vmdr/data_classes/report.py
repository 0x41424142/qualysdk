"""
report.py - contains the VMDRReport dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import Union, Dict
from datetime import datetime

from ...base.base_class import BaseClass


@dataclass(order=True)
class VMDRReport(BaseClass):
    """
    Represents a VMDR report.
    """

    ID: int = field(
        metadata={"description": "The unique ID of the report."}, default=None
    )

    TITLE: str = field(
        metadata={"description": "The title of the report."}, default=None
    )

    TYPE: str = field(metadata={"description": "The type of the report."}, default=None)

    USER_LOGIN: str = field(
        metadata={"description": "The user that launched the report."}, default=None
    )

    LAUNCH_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the report was launched."},
        default=None,
    )

    OUTPUT_FORMAT: str = field(
        metadata={"description": "The output format of the report."}, default=None
    )

    SIZE: Union[str, float] = field(
        metadata={"description": "The size of the report. Gets normalized to MB."},
        default=None,
    )

    STATUS: Union[Dict, str] = field(
        metadata={"description": "The status of the report."}, default=None
    )

    STATE: str = field(
        metadata={"description": "The state of the report."}, default=None
    )

    EXPIRATION_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the report will expire."},
        default=None,
    )

    def __post_init__(self):
        DT_FIELDS = ["LAUNCH_DATETIME", "EXPIRATION_DATETIME"]
        for dt_field in DT_FIELDS:
            if getattr(self, dt_field):
                setattr(self, dt_field, datetime.fromisoformat(getattr(self, dt_field)))

        self.ID = int(self.ID)

        self.STATE = self.STATUS.get("STATE")

        if self.SIZE:
            # Now for the fun part. SIZE can be KB, MB, or maybe even GB. Let's convert it to bytes and then to MB.
            # incoming string will contain the unit, so we can just strip it off and convert to bytes.

            if self.SIZE == "-":
                self.SIZE = 0
                return

            # Split SIZE into the value and unit
            size_value, size_unit = self.SIZE.split(" ")
            size_value = float(size_value)
            size_unit = size_unit.upper()

            # Convert size to bytes
            match size_unit:
                case "MB":
                    # If we are already in MB, we can just return the value
                    self.SIZE = size_value
                    return

                case "KB":
                    size_in_bytes = size_value * 1024
                case "GB":
                    size_in_bytes = size_value * 1024**3
                case "BYTES":
                    size_in_bytes = size_value
                case _:
                    raise ValueError(f"Invalid unit {size_unit} for report size.")

            # Convert bytes to MB
            self.SIZE = size_in_bytes / 1024**2

    def __int__(self):
        return self.ID

    def __str__(self):
        return f"{self.ID}: {self.TITLE}"

    def valid_values(self):
        """
        valid_values - returns a dictionary of attributes that have non-None values.
        """
        return {k: v for k, v in self.to_dict().items() if v}


@dataclass(order=True)
class VMDRScheduledReport(BaseClass):
    """
    Represents a VMDR scheduled report.
    """

    ID: int = field(
        metadata={"description": "The unique ID of the report."}, default=None
    )

    TITLE: str = field(
        metadata={"description": "The title of the report."}, default=None
    )

    OUTPUT_FORMAT: str = field(
        metadata={"description": "The output format of the report."}, default=None
    )

    TEMPLATE_TITLE: str = field(
        metadata={"description": "The title of the report template."}, default=None
    )

    ACTIVE: Union[bool, str] = field(
        metadata={"description": "Whether the report is active."}, default=None
    )

    SCHEDULE: dict = field(
        metadata={"description": "The schedule of the report."}, default=None
    )

    START_DATE_UTC: Union[str, datetime] = field(
        metadata={"description": "The start date of the report."}, default=None
    )

    START_HOUR: int = field(
        metadata={"description": "The start hour of the report."}, default=None
    )

    START_MINUTE: int = field(
        metadata={"description": "The start minute of the report."}, default=None
    )

    TIME_ZONE: dict = field(
        metadata={"description": "The time zone of the report."}, default=None
    )

    TIME_ZONE_CODE: str = field(
        metadata={"description": "The time zone code of the report."}, default=None
    )

    TIME_ZONE_DETAILS: str = field(
        metadata={"description": "The time zone details of the report."}, default=None
    )

    DST_SELECTED: Union[bool, str] = field(
        metadata={"description": "Whether DST is selected."}, default=None
    )

    def __post_init__(self):
        self.ID = int(self.ID)

        if self.ACTIVE:
            self.ACTIVE = bool(self.ACTIVE)

        if self.SCHEDULE:
            # First, do all the conversions.
            self.START_DATE_UTC = datetime.fromisoformat(
                self.SCHEDULE["START_DATE_UTC"]
            )
            self.START_HOUR = int(self.SCHEDULE["START_HOUR"])
            self.START_MINUTE = int(self.SCHEDULE["START_MINUTE"])
            self.TIME_ZONE = self.SCHEDULE["TIME_ZONE"]
            self.TIME_ZONE_CODE = self.TIME_ZONE["TIME_ZONE_CODE"]
            self.TIME_ZONE_DETAILS = self.TIME_ZONE["TIME_ZONE_DETAILS"]
            self.DST_SELECTED = bool(self.SCHEDULE["DST_SELECTED"])
            # Finally, remove all the above keys from the SCHEDULE dict,
            # leaving us only with the frequency data.
            for key in [
                "START_DATE_UTC",
                "START_HOUR",
                "START_MINUTE",
                "TIME_ZONE",
                "DST_SELECTED",
            ]:
                self.SCHEDULE.pop(key)

    def __int__(self):
        return self.ID

    def __str__(self):
        return f"{self.ID}: {self.TITLE}"

    def valid_values(self):
        """
        valid_values - returns a dictionary of attributes that have non-None values.
        """
        return {k: v for k, v in self.to_dict().items() if v}
