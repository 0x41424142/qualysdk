"""
TotalCloud QID class
"""

from dataclasses import dataclass, asdict
from typing import Union
from datetime import datetime


@dataclass
class QID:
    """
    Represents a Qualys QID for the TotalCloud module
    """

    qid: int = None
    patchAvailable: bool = None
    exploitability: str = None
    severity: int = None
    customerSeverity: int = None
    lastFound: Union[str, datetime] = None
    firstFound: Union[str, datetime] = None
    port: int = None
    protocol: str = None
    category: str = None
    hostOS: str = None
    typeDetected: str = None
    status: str = None
    disabled: bool = None
    ignored: bool = None

    def __post_init__(self):
        DT_FIELDS = ["lastFound", "firstFound"]
        for field in DT_FIELDS:
            if isinstance(getattr(self, field), str):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if getattr(self, "exploitability") and getattr(self, "exploitability") == "---":
            setattr(self, "exploitability", None)

    def __int__(self):
        return self.qid

    def __dict__(self):
        return asdict(self)

    def to_dict(self):
        return asdict(self)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
