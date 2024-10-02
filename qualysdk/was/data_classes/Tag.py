"""
Contains the WASTag class for WAS
"""

from dataclasses import dataclass, asdict


@dataclass
class WASTag:
    """
    Represents a single tag in WAS
    """

    id: int = None
    name: str = None

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
        return WASTag(**data)
