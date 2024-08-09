"""
bugtraq.py - contains the BugTraq dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *


@dataclass
class Bugtraq:
    """
    BugTraq - represents a single BugTraq entry in a BugTraqList.
    """

    ID: int = field(metadata={"description": "The BugTraq ID."})
    URL: str = field(
        metadata={"description": "The URL of the BugTraq."}, default="", compare=False
    )

    def __post_init__(self):
        # make sure that the ID is an integer:
        if not isinstance(self.ID, int):
            self.ID = int(self.ID)
        # and that url is a string:
        if not isinstance(self.URL, str):
            self.URL = str(self.URL)

    def __str__(self):
        return str(self.ID)

    def __dict__(self):
        return asdict(self)

    def __contains__(self, item):
        return item in self.ID or item in self.URL

    def copy(self):
        return Bugtraq(ID=self.ID, URL=self.URL)

    def is_id(self, id: int):
        return self.ID == id

    def is_url(self, url: str):
        return self.URL == url

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
        from_dict - create a BugTraq object from a dictionary.

        This function is used to create a BugTraq object from a dictionary.
        """
        required_keys = {"ID"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        return cls(**data)
