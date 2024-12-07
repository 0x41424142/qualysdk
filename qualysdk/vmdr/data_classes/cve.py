"""
cve.py - contains the CVEID dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *
from re import match

from ...base.base_class import BaseClass


@dataclass
class CVEID(BaseClass):
    """
    CVEID - represents a single CVE ID in a CVEList.
    """

    ID: str = field(metadata={"description": "The ID of the CVE."}, compare=True)
    URL: Optional[str] = field(
        metadata={"description": "The URL of the CVE."}, default="", compare=False
    )

    def __post_init__(self):
        # make sure that the ID is a string:
        if not isinstance(self.ID, str):
            raise TypeError(f"CVEID ID must be a string, not {type(self.ID)}")
        # and that url is a string:
        if not isinstance(self.URL, str):
            raise TypeError(f"CVEID URL must be a string, not {type(self.URL)}")

    def __str__(self) -> str:
        return self.ID

    def __contains__(self, item):
        # see if it was found in the name or vendor:
        return item in self.ID

    def copy(self):
        return CVEID(id=self.ID)

    def is_id(self, id: str):
        return self.ID == id

    @classmethod
    def from_str(cls, cve_id: str):
        """
        from_str - create a CVEID object from a string.

        This function is used to create a CVEID object from a string.

        The string should be in the format "CVE-YYYY-NNNN".

        If the string is not in the correct format, a ValueError will be raised.
        """
        cve_regex = r"CVE-\d{4}-\d{4,}"
        if not match(cve_regex, cve_id):
            raise ValueError(f"Invalid CVE ID format: {cve_id}")

        return cls(ID=cve_id)
