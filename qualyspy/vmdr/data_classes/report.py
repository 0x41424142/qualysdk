"""
report.py - contains the VMDRReport dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import Union, Dict
from datetime import datetime

"""
<REPORT>
<ID>42703</ID>
<TITLE><![CDATA[Test now]]></TITLE>
<TYPE>Scan</TYPE>
<USER_LOGIN>acme_aa</USER_LOGIN>
<LAUNCH_DATETIME>2017-10-30T17:59:22Z</LAUNCH_DATETIME>
<OUTPUT_FORMAT>PDF</OUTPUT_FORMAT>
<SIZE>129.1 MB</SIZE>
<STATUS>
<STATE>Finished</STATE>
</STATUS>
<EXPIRATION_DATETIME>2017-11-
06T17:59:24Z</EXPIRATION_DATETIME>
</REPORT>
"""

@dataclass(order=True)
class VMDRReport:
    """
    Represents a VMDR report.
    """

    ID: int = field(metadata={"description": "The unique ID of the report."}, default=None)

    TITLE: str = field(metadata={"description": "The title of the report."}, default=None)

    TYPE: str = field(metadata={"description": "The type of the report."}, default=None)

    USER_LOGIN: str = field(metadata={"description": "The user that launched the report."}, default=None)

    LAUNCH_DATETIME: Union[str, datetime] = field(metadata={"description": "The date and time the report was launched."}, default=None)

    OUTPUT_FORMAT: str = field(metadata={"description": "The output format of the report."}, default=None)

    SIZE: Union[str, float] = field(metadata={"description": "The size of the report. Gets normalized to MB."}, default=None)

    STATUS: Union[Dict, str] = field(metadata={"description": "The status of the report."}, default=None)

    STATE: str = field(metadata={"description": "The state of the report."}, default=None)

    EXPIRATION_DATETIME: Union[str, datetime] = field(metadata={"description": "The date and time the report will expire."}, default=None)

    def __post_init__(self):
        DT_FIELDS = ["LAUNCH_DATETIME", "EXPIRATION_DATETIME"]
        for field in DT_FIELDS:
            if getattr(self, field):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        self.ID = int(self.ID)

        self.STATE = self.STATUS.get("STATE")

        if self.SIZE:

            # Now for the fun part. SIZE can be KB, MB, or maybe even GB. Let's convert it to bytes and then to MB.
            # incoming string will contain the unit, so we can just strip it off and convert to bytes.

            # Split SIZE into the value and unit
            size_value, size_unit = self.SIZE.split(' ')
            size_value = float(size_value)
            size_unit = size_unit.upper()

            # Convert size to bytes
            match size_unit:
                case 'MB':
                    # If we are already in MB, we can just return the value
                    self.SIZE = size_value
                    return
                
                case 'KB':
                    size_in_bytes = size_value * 1024
                case 'GB':
                    size_in_bytes = size_value * 1024 ** 3
                case 'BYTES':
                    size_in_bytes = size_value
                case _:
                    raise ValueError(f"Invalid unit {size_unit} for report size.")

            # Convert bytes to MB
            self.SIZE = size_in_bytes / 1024 ** 2

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - creates a VMDRReport object from a dictionary.
        """
        return cls(**data)
    
    def __dict__(self):
        return asdict(self)
    
    def keys(self):
        return asdict(self).keys()
    
    def values(self):
        return asdict(self).values()
    
    def items(self):
        return asdict(self).items()
    
    def valid_values(self):
        """
        valid_values - returns a dictionary of attributes that have non-None values.
        """
        return {
            k: v
            for k, v in self.__dict__.items()
            if v
        }
    