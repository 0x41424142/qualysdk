"""
compliance.py - contains the Compliance dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *

from ...base.base_class import BaseClass


@dataclass
class Compliance(BaseClass):
    """
    Compliance - represents a compliance object.
    """

    _TYPE: str = field(metadata={"description": "The compliance framework name."})
    SECTION: str = field(metadata={"description": "The section name."})
    DESCRIPTION: str = field(
        metadata={"description": "The description of the compliance."}
    )

    def __str__(self):
        return f"{self._TYPE} - {self.SECTION}"

    def __contains__(self, item):
        return item in self._TYPE or item in self.SECTION or item in self.DESCRIPTION

    def copy(self):
        return Compliance(
            _TYPE=self._TYPE, SECTION=self.SECTION, DESCRIPTION=self.DESCRIPTION
        )

    def is_type(self, _type: str):
        return self._TYPE == _type

    def is_section(self, section: str):
        return self.SECTION == section

    def is_description(self, description: str):
        return self.DESCRIPTION == description
