"""
bugtraq.py - contains the BugTraq dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *


@dataclass(frozen=True)
class Bugtraq:
    """
    BugTraq - represents a single BugTraq entry in a BugTraqList.

    This class is used to represent a single BugTraq entry in a BugTraqList,
    which is used to represent the BugTraq that is affected by a vulnerability.

    This class is frozen, meaning that once an object is created, it cannot be modified.
    It can be used as a key in a dictionary or as an element in a set.
    """

    ID: int = field(metadata={"description": "The BugTraq ID."})
    URL: str = field(
        metadata={"description": "The URL of the BugTraq."}, default="", compare=False
    )

    def __post_init__(self):
        # make sure that the ID is an integer:
        if not isinstance(self.ID, int):
            raise TypeError(f"BugTraq ID must be an integer, not {type(self.ID)}")
        # and that url is a string:
        if not isinstance(self.URL, str):
            raise TypeError(f"BugTraq URL must be a string, not {type(self.URL)}")

    def __str__(self):
        return str(self.ID)

    def __contains__(self, item):
        return item in self.ID or item in self.URL

    def copy(self):
        return Bugtraq(ID=self.ID, URL=self.URL)

    def is_id(self, id: int):
        return self.ID == id

    def is_url(self, url: str):
        return self.URL == url

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - create a BugTraq object from a dictionary.

        This function is used to create a BugTraq object from a dictionary.
        """
        required_keys = {"ID"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        return cls(**data)
