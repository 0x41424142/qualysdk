"""
qds.py - contains the QDS dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *


@dataclass(order=True)
class QDS:
    """
    QDS - represents a single QDS score.

    made with order=True to allow for sorting of QDS scores.
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

    def __int__(self):
        return self.SCORE

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
        from_dict - create a QDS object from a dictionary.

        Params:
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
