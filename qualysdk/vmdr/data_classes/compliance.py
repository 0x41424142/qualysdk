"""
compliance.py - contains the Compliance dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *


@dataclass
class Compliance:
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

    def __dict__(self):
        return asdict(self)

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
        from_dict - create a Compliance object from a dictionary.

        Params:
            data (dict): The dictionary containing the data for the Compliance object.

        Returns:
            Compliance: The Compliance object created from the dictionary.
        """
        required_keys = {"_TYPE", "SECTION", "DESCRIPTION"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )
        return cls(**data)
