"""
Contains the Tag class.
"""

from dataclasses import dataclass

from ...base.base_class import BaseClass


@dataclass
class Tag(BaseClass):
    """
    Represents a Tag in Patch Management.
    """

    name: str = ""
    id: str = None

    def __str__(self) -> str:
        return self.name if self.name else self.id if self.id else ""
