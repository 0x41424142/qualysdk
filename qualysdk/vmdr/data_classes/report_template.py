"""
report_template.py - Contains the ReportTemplate data class.
"""

from typing import Union
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class ReportTemplate:
    """
    A single report template in VMDR
    """

    ID: int = field(
        metadata={"description": "The unique ID of the report template."}, default=None
    )

    TYPE: str = field(
        metadata={"description": "The type of the report template."}, default=None
    )

    TEMPLATE_TYPE: str = field(
        metadata={"description": "The template type of the report template."},
        default=None,
    )

    TITLE: str = field(
        metadata={"description": "The title of the report template."}, default=None
    )

    USER: dict = field(
        metadata={"description": "The user that created the report template."},
        default=None,
    )

    LAST_UPDATE: Union[str, datetime] = field(
        metadata={"description": "The last time the report template was updated."},
        default=None,
    )

    GLOBAL: bool = field(
        metadata={"description": "If the report template is global."}, default=None
    )

    def __post_init__(self):
        if self.LAST_UPDATE:
            self.LAST_UPDATE = datetime.fromisoformat(self.LAST_UPDATE)

        self.ID = int(self.ID)
        self.GLOBAL = bool(self.GLOBAL)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a ReportTemplate object from a dictionary.
        """
        return cls(**data)

    def __dict__(self):
        return asdict(self)

    def to_dict(self):
        return asdict(self)

    def __int__(self):
        return self.ID

    def __str__(self):
        return f"{self.ID}: {self.TITLE}"

    def keys(self):
        return self.__dict__().keys()

    def values(self):
        return self.__dict__().values()

    def items(self):
        return self.__dict__().items()

    def valid_values(self):
        return {k: v for k, v in self.__dict__().items() if v}

    def to_dict(self):
        return asdict(self)
