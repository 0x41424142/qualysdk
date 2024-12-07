"""
Contains the WASTag class for WAS
"""

from dataclasses import dataclass

from ...base.base_class import BaseClass


@dataclass
class WASTag(BaseClass):
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
