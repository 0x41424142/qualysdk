"""
Contains the AuthRecord class for WAS
"""

from dataclasses import dataclass, asdict


@dataclass
class AuthRecord:
    """
    Represents a single tag in WAS
    """

    id: int = None
    name: str = None

    def __post_init__(self):
        if self.id and isinstance(self.id, str):
            try:
                self.id = int(self.id)
            except ValueError:
                raise ValueError("id must be numeric")

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @staticmethod
    def from_dict(data):
        return AuthRecord(**data)
