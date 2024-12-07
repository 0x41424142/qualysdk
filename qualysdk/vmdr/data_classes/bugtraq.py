"""
bugtraq.py - contains the BugTraq dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *

from ...base.base_class import BaseClass


@dataclass
class Bugtraq(BaseClass):
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

    def __contains__(self, item):
        return item in self.ID or item in self.URL

    def copy(self):
        return Bugtraq(ID=self.ID, URL=self.URL)

    def is_id(self, id: int):
        return self.ID == id

    def is_url(self, url: str):
        return self.URL == url
