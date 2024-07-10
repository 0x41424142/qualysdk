"""
Software_list.py - contains the SoftwareList class for the Qualys VMDR module.

SoftwareLists are used as a dataclass underneath of a KBEntry object to represent the software that is affected by a vulnerability.
"""

from dataclasses import dataclass, field
from typing import *

from ..software import Software

from .base_list import BaseList


@dataclass(order=True)  # order=True allows us to compare SoftwareList objects
class SoftwareList(BaseList):
    """
    SoftwareList - represents a list of software that is affected by a vulnerability.

    Built by the KBEntry class to represent the software that is affected by a vulnerability.
    """

    _list: List[Software] = field(
        default_factory=list,
        metadata={
            "description": "A list of Software objects that represents all software affected by a vulnerability."
        },
    )

    def __repr__(self):
        return f"SoftwareList({self._list})"

    @classmethod
    def from_list(cls, software_list: List[Software]) -> Self:
        """
        from_list - create a SoftwareList from a list of Software objects.

        This function is used to create a SoftwareList from a list of Software objects.

        Args:
            software_list (List[Software]): A list of Software objects.

        Raises:
            TypeError: If any of the objects in the list are not Software objects.
            ValueError: If any of the objects in the list are duplicates.

        Returns:
            SoftwareList: A SoftwareList object.
        """
        # init. a class object:
        c = cls()

        # check that all things in the list are Software objects and unique:
        for software in software_list:
            if not isinstance(software, Software):
                raise TypeError(
                    f"SoftwareList can only contain Software objects, not {type(software)}"
                )
            # check that the software is not already in the list:
            if software in c._list:
                raise ValueError(
                    f"SoftwareList cannot contain duplicate Software objects. {software} is already in the list."
                )

            c.append(software)

        return c

    def contains_name(self, name: str, exact: bool = True) -> bool:
        """
        contains_name - check if a software name is in the SoftwareList.

        This function is used to check if a software name is in the SoftwareList.

        Args:
            name (str): The name of the software to check for.
            exact (bool): Whether to check for an exact match. Defaults to True.

        Returns:
            bool: True if the software is in the SoftwareList, False otherwise.
        """
        if not exact:
            for software in self._list:
                if name.lower() in software.PRODUCT.lower():
                    return True
            return False
        else:
            for software in self._list:
                if name.lower() == software.PRODUCT.lower():
                    return True
            return False

    def contains_vendor(self, vendor: str, exact: bool = True) -> bool:
        """
        contains_vendor - check if a software vendor is in the SoftwareList.

        This function is used to check if a software vendor is in the SoftwareList.

        Args:
            vendor (str): The vendor of the software to check for.
            exact (bool): Whether to check for an exact match. Defaults to True.

        Returns:
            bool: True if the vendor is in the SoftwareList, False otherwise.
        """
        if not exact:
            for software in self._list:
                if vendor.lower() in software.VENDOR.lower():
                    return True
            return False
        else:
            for software in self._list:
                if vendor.lower() == software.VENDOR.lower():
                    return True
            return False
