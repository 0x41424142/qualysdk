"""
cve_list.py - contains the CVEList dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *

from ..cve import CVEID

from .base_list import BaseList


@dataclass(order=True)  # order=True allows us to compare CVEList objects
class CVEList(BaseList):
    """
    CVEList - represents a list of CVEIDs.

    This class is used to represent a list of CVEIDs.
    It is used as a dataclass underneath of a KBEntry object.
    """

    _list: List[CVEID] = field(
        default_factory=list,
        metadata={
            "description": "A list of CVEID objects that represents all CVEs affected by a vulnerability."
        },
    )

    def __repr__(self):
        return f"CVEList({self._list})"

    @classmethod
    def from_list(cls, cve_list: List[CVEID]) -> Self:
        """
        from_list - create a CVEList from a list of CVEID objects.

        This function is used to create a CVEList from a list of CVEID objects.

        Args:
            cve_list (List[CVEID]): A list of CVEID objects.

        Raises:
            TypeError: If any of the objects in the list are not CVEID objects.
            ValueError: If any of the objects in the list are duplicates.

        Returns:
            CVEList: A CVEList object.
        """
        # init. a class object:
        c = cls()

        # check that all things in the list are CVEID objects and unique:
        for cve in cve_list:
            if not isinstance(cve, CVEID):
                raise TypeError(
                    f"CVEList can only contain CVEID objects, not {type(cve)}"
                )
            if cve in c._list:
                raise ValueError(f"CVEList cannot contain duplicate CVEIDs: {cve}")

        # add all the CVEIDs to the list:
        c._list = cve_list

        return c
