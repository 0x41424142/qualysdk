"""
threat_intel.py - contains the ThreatIntel dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *


@dataclass
class ThreatIntel:
    """
    ThreatIntel - represents a single threat intel entry in a ThreatIntelList.
    """

    ID: int = field(metadata={"description": "The ID of the threat intel."})
    TEXT: str = field(
        metadata={"description": "The text of the threat intel."},
        default="",
        compare=False,
    )

    def __post_init__(self):
        # make sure that the ID is an integer:
        if not isinstance(self.ID, int):
            self.ID = int(self.ID)
        # and that text is a string:
        if not isinstance(self.TEXT, str):
            self.TEXT = str(self.TEXT)

    def __str__(self):
        return str(self.TEXT)

    def __contains__(self, item):
        return item in self.ID or item in self.TEXT

    def copy(self):
        return ThreatIntel(ID=self.ID, TEXT=self.TEXT)

    def is_id(self, id: int):
        return self.ID == id

    def is_text(self, text: str):
        return self.TEXT == text

    def to_dict(self):
        return asdict(self)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - create a ThreatIntel object from a dictionary.

        Params:
            data (dict): The dictionary containing the data for the ThreatIntel object.

        Returns:
            ThreatIntel: The ThreatIntel object created from the dictionary.
        """
        required_keys = {"ID"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )
        return cls(**data)
