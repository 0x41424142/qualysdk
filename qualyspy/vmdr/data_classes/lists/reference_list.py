"""
reference_list.py - contains the ReferenceList dataclass for the Qualys VMDR module.

ReferenceLists are used as a dataclass underneath of a KBEntry object to represent the vendor bulletin references for a vulnerability.
"""

from dataclasses import dataclass, field
from typing import *

from ..vendor_reference import VendorReference

from .base_list import BaseList


@dataclass(order=True)  # order=True allows us to compare ReferenceList objects
class ReferenceList(BaseList):
    """
    ReferenceList - represents a list of vendor bulletin references for a vulnerability.

    This class is used to represent a list of vendor bulletin references for a vulnerability.
    It is used as a dataclass underneath of a KBEntry object.
    """

    _list: List[VendorReference] = field(default_factory=list)

    def __post_init__(self):
        # make sure that all elements in the list are VendorReference objects:
        for reference in self._list:
            if not isinstance(reference, VendorReference):
                raise TypeError(
                    f"ReferenceList can only contain VendorReference objects, not {type(reference)}"
                )

    def __repr__(self):
        return f"ReferenceList({self._list})"

    def is_id(self, id: int) -> bool:
        """
        is_id - check if the list contains a reference with a specific ID.

        This function is used to check if the list contains a reference with a specific ID.
        """
        return any(reference.is_id(id) for reference in self._list)

    def is_url(self, url: str) -> bool:
        """
        is_url - check if the list contains a reference with a specific URL.

        This function is used to check if the list contains a reference with a specific URL.
        """
        return any(reference.is_url(url) for reference in self._list)

    @classmethod
    def from_dict(cls, data: List[dict]) -> "ReferenceList":
        """
        from_dict - create a ReferenceList object from a list of dictionaries.

        This function is used to create a ReferenceList object from a list of dictionaries.
        """
        return cls([VendorReference.from_dict(reference) for reference in data])
