"""
Contains the WebAppAuthServerRecord class for the WAS
"""

from dataclasses import dataclass, asdict
from typing import Union
from hashlib import sha256


@dataclass
class WebAppAuthServerRecord:
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
        return cls(**data)

    def set_password_to_sha256(self):
        """
        Hashes the password using SHA256 and saves to instance
        """
        setattr(self, "password", sha256(self.password.encode()).hexdigest())

    def sha256_password(self):
        """
        Returns the SHA256 hash of the password
        """
        return sha256(self.password.encode()).hexdigest()
