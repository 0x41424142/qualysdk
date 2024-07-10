"""
compliance_list.py - contains the ComplianceList dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *

from ..compliance import Compliance

from .base_list import BaseList


@dataclass
class ComplianceList(BaseList):
    """
    ComplianceList - represents a list of compliance objects.

    This class is used to represent a list of compliance objects.
    """

    _list: List[Compliance] = field(default_factory=list)

    def __post_init__(self):
        # make sure that all elements in the list are Compliance objects:
        for compliance in self._list:
            if not isinstance(compliance, Compliance):
                raise TypeError(
                    f"ComplianceList can only contain Compliance objects, not {type(compliance)}"
                )

    def __repr__(self):
        return f"ComplianceList({self._list})"

    def is_type(self, _type: str) -> bool:
        """
        is_type - check if the list contains a compliance with a specific type.

        This function is used to check if the list contains a compliance with a specific type.
        """
        return any(compliance.is_type(_type) for compliance in self._list)

    def is_section(self, section: str) -> bool:
        """
        is_section - check if the list contains a compliance with a specific section.

        This function is used to check if the list contains a compliance with a specific section.
        """
        return any(compliance.is_section(section) for compliance in self._list)

    def is_description(self, description: str) -> bool:
        """
        is_description - check if the list contains a compliance with specific description.

        This function is used to check if the list contains a compliance with specific description.
        """
        return any(compliance.is_description(description) for compliance in self._list)

    @classmethod
    def from_dict(cls, data: List[dict]) -> "ComplianceList":
        """
        from_dict - create a ComplianceList object from a list of dictionaries.

        This function is used to create a ComplianceList object from a list of dictionaries.
        """
        return cls([Compliance.from_dict(entry) for entry in data])
