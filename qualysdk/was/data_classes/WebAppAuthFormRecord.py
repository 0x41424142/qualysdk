"""
Contains the WebAppAuthFormRecord class for the WAS
"""

from dataclasses import dataclass
from typing import Union

from ...base.base_class import BaseClass


@dataclass
class WebAppAuthFormRecord(BaseClass):
    """
    Represents a single form authentication record
    in Qualys WAS
    """

    id: Union[str, int] = None
    name: str = None
    secured: bool = None
    value: str = None

    def __post_init__(self):
        if not isinstance(self.id, (str, int)):
            raise ValueError("id must be a string or integer")
        setattr(self, "id", int(self.id))

        setattr(self, "secured", self.secured == "true")

    def __str__(self):
        return f"{self.name} : {self.value}"

    def redact_password(self):
        """
        Obfuscates the password
        """
        if self.name.lower() == "password" or self.secured:
            setattr(self, "value", "REDACTED")
