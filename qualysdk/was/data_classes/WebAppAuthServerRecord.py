"""
Contains the WebAppAuthServerRecord class for the WAS
"""

from dataclasses import dataclass
from typing import Union

from ...base.base_class import BaseClass


@dataclass
class WebAppAuthServerRecord(BaseClass):
    """
    Represents a single server authentication record
    in Qualys WAS
    """

    id: Union[str, int] = None
    type: str = None
    domain: str = None
    username: str = None
    password: str = None

    def __post_init__(self):
        if not isinstance(self.id, (str, int)):
            raise ValueError("id must be a string or integer")
        setattr(self, "id", int(self.id))

    def __str__(self):
        return f"{self.type} : {self.username}"

    def redact_password(self):
        """
        Obfuscates the password
        """
        if self.password:
            setattr(self, "password", "REDACTED")
