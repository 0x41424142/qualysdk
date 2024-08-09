"""
software.py - contains the Software dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *


@dataclass
class Software:
    """
    Software - represents a single software entry in a SoftwareList.

    This class is used to represent a single software entry in a SoftwareList,
    which is used to represent the software that is affected by a vulnerability.
    """

    PRODUCT: str = field(metadata={"description": "The name of the software."})
    VENDOR: str = field(
        metadata={"description": "The vendor of the software."},
        default="",
        compare=False,
    )

    def __str__(self):
        return self.PRODUCT

    def __contains__(
        self, item
    ):  # allows us to use the 'in' operator. for example, 'if "Adobe" in software'. this is a fuzzy search.
        # see if it was found in the name or vendor:
        return item in self.PRODUCT or item in self.VENDOR

    def copy(self):
        return Software(PRODUCT=self.PRODUCT, VENDOR=self.VENDOR)

    def is_vendor(self, vendor: str):
        return self.VENDOR.lower() == vendor.lower()

    def is_name(self, product: str):
        return self.PRODUCT.lower() == product.lower()

    def to_dict(self):
        return asdict(self)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Union[dict, list]):
        """
        from_dict - create a Software object from a dictionary.

        This function is used to create a Software object from a dictionary.
        """
        # make sure that the dictionary has the required keys and nothing else:
        required_keys = {"PRODUCT", "VENDOR"}

        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        return cls(**data)
