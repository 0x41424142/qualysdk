"""
qds_factor.py - contains the QDSFactor dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *


@dataclass
class QDSFactor:
    """
    QDSFactor - represents a single Qualys Detection Score (QDS) factor.
    """

    NAME: int = field(metadata={"description": "The name of the factor."})
    VALUE: Union[str, int, float] = field(
        metadata={
            "description": "The value of the factor. Can be a str or number depending on what the @name is."
        },
        default="",
    )

    def __post_init__(self):
        # make sure that the ID is an integer:
        if not isinstance(self.NAME, str):
            raise TypeError(f"QDSFactor NAME must be a string, not {type(self.NAME)}")
        # check if the VALUE can be interpreted as a number:
        for val in (float, int):
            try:
                # special case for CVSS version, as qualys prepends as 'v' to the number:
                if self.NAME == "CVSS":
                    self.VALUE = self.VALUE[1:]

                self.VALUE = val(self.VALUE)
                break
            except ValueError:
                pass

    def __str__(self):
        return str(self.VALUE)

    def __contains__(self, item):
        return item in self.NAME or item in self.VALUE

    def copy(self):
        return QDSFactor(ID=self.NAME, TEXT=self.VALUE)

    def is_id(self, id: int):
        return self.NAME == id

    def is_text(self, text: str):
        return self.VALUE == text

    def has_rti(self):
        return self.NAME == "RTI"

    def has_cvss_score(self):
        return self.NAME == "CVSS"

    def has_epss(self):
        return self.NAME == "epss"

    def get_epss(self):
        if self.has_epss():
            return self.VALUE

    def get_cvss_score(self):
        if self.has_cvss_score():
            return self.VALUE

    def has_malware_hash(self):
        return self.NAME == "malware_hash"

    def get_malware_hash(self):
        if self.has_malware_hash():
            return self.VALUE

    def get_rti(self):
        if self.has_rti():
            return self.VALUE

    def get_name(self):
        return self.NAME

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
        from_dict - create a QDSFactor object from a dictionary.

        Params:
            data (dict): The dictionary containing the data for the QDSFactor object.

        Returns:
            QDSFactor: The QDSFactor object created from the dictionary.
        """
        required_keys = {"NAME", "VALUE"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )
        return cls(**data)
