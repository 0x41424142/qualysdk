"""
Contains the Tag class.
"""

from dataclasses import dataclass, asdict


@dataclass
class Tag:
    """
    Represents a Tag in Patch Management.
    """

    name: str = None
    id: str = None

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        return asdict(self)

    def __str__(self) -> str:
        return self.name if self.name else self.id

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Tag object from a dictionary.
        """
        # exclusion tags only return tag ID as a string
        if isinstance(data, str):
            return cls(id=data)
        else:
            return cls(**data)
