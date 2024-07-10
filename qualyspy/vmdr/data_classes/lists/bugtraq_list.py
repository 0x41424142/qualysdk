"""
bugtraq_list.py - This module contains the BugtraqList class which is used to interact with the Qualys VMDR Bugtraq List API.
"""

from dataclasses import dataclass, field
from typing import *

from ..bugtraq import Bugtraq

from .base_list import BaseList


@dataclass(order=True)  # order=True allows us to compare BugtraqList objects
class BugtraqList(BaseList):
    """
    BugTraqList - represents a list of BugTraq entries for a vulnerability.

    This class is used to represent a list of BugTraq entries for a vulnerability.
    It is used as a dataclass underneath of a KBEntry object.
    """

    _list: List[Bugtraq] = field(
        default_factory=list,
        metadata={
            "description": "A list of Bugtraq objects that represents all BugTraq entries affected by a vulnerability."
        },
    )

    def __repr__(self):
        return f"BugTraqList({self._list})"

    @classmethod
    def from_list(cls, bugtraq_list: List[Bugtraq]) -> Self:
        """
        from_list - create a BugTraqList from a list of Bugtraq objects.

        This function is used to create a BugTraqList from a list of Bugtraq objects.

        Args:
            bugtraq_list (List[Bugtraq]): A list of Bugtraq objects.

        Raises:
            TypeError: If any of the objects in the list are not Bugtraq objects.
            ValueError: If any of the objects in the list are duplicates.

        Returns:
            BugTraqList: A BugTraqList object.
        """
        # init. a class object:
        c = cls()

        # check that all things in the list are Bugtraq objects and unique:
        for bugtraq in bugtraq_list:
            if not isinstance(bugtraq, Bugtraq):
                raise TypeError(
                    f"BugTraqList can only contain Bugtraq objects, not {type(bugtraq)}"
                )
            if bugtraq in c._list:
                raise ValueError(
                    f"BugTraqList cannot contain duplicate Bugtraqs: {bugtraq}"
                )
        return c
