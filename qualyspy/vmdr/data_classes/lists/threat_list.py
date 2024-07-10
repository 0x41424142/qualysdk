"""
threat_list.py - contains the ThreatList dataclass for the Qualys VMDR module.

This file contains the ThreatList dataclass, which is used to represent a list of ThreatIntel objects.
"""

from dataclasses import dataclass, field
from typing import *

from ..threat_intel import ThreatIntel

from .base_list import BaseList


@dataclass(order=True)  # order=True allows us to compare ThreatList objects
class ThreatIntelList(BaseList):
    """
    ThreatIntelList - represents a list of threat intel objects.

    This class is used to represent a list of threat intel objects.
    """

    _list: List[ThreatIntel] = field(default_factory=list)

    def __post_init__(self):
        # make sure that all elements in the list are ThreatIntel objects:
        for threat in self._list:
            if not isinstance(threat, ThreatIntel):
                raise TypeError(
                    f"ThreatIntelList can only contain ThreatIntel objects, not {type(threat)}"
                )

    def __repr__(self):
        return f"ThreatIntelList({self._list})"

    def is_id(self, id: int) -> bool:
        """
        is_id - check if the list contains a threat with a specific ID.

        This function is used to check if the list contains a threat with a specific ID.
        """
        return any(threat.is_id(id) for threat in self._list)

    def is_text(self, text: str) -> bool:
        """
        is_text - check if the list contains a threat with specific text.

        This function is used to check if the list contains a threat with specific text.
        """
        return any(threat.is_text(text) for threat in self._list)

    @classmethod
    def from_dict(cls, data: List[dict]) -> "ThreatIntelList":
        """
        from_dict - create a ThreatIntelList object from a list of dictionaries.

        This function is used to create a ThreatIntelList object from a list of dictionaries.
        """
        return cls([ThreatIntel.from_dict(entry) for entry in data])
