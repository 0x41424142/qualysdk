"""
qds.py - contains the QDS dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *


@dataclass(frozen=True, order=True)
class QDS:
    """
    QDS - represents a single QDS score.

    This class is frozen, meaning that once an object is created, it cannot be modified.
    It can be used as a key in a dictionary or as an element in a set.
    """

    SEVERITY: str = field(
        metadata={"description": "The rating of the QDS score."}, compare=False
    )
    SCORE: int = field(
        metadata={"description": "The actual score itself as an int."},
        default=0,
    )

    def __post_init__(self):
        # make sure that the SEVERITY is a str:
        if not isinstance(self.SEVERITY, str):
            raise TypeError(f"QDS SEVERITY must be a str, not {type(self.SEVERITY)}")
        # and that text is an int:
        if not isinstance(self.SCORE, int):
            raise TypeError(f"QDS SCORE must be an int, not {type(self.SCORE)}")

    def __str__(self):
        return str(self.SCORE)

    def __contains__(self, item):
        return item in self.SEVERITY or item in self.SCORE

    def copy(self):
        return QDS(SEVERITY=self.SEVERITY, SCORE=self.SCORE)

    def is_severity(self, severity: str):
        return self.SEVERITY == severity

    def get_severity(self):
        return self.SEVERITY

    def get_score(self):
        return self.SCORE

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - create a QDS object from a dictionary.

        Args:
            data (dict): The dictionary containing the data for the QDS object.

        Returns:
            QDS: The QDS object created from the dictionary.
        """
        required_keys = {"SEVERITY", "SCORE"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )
        return cls(**data)