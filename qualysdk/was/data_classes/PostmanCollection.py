"""
Contains the PostmanCollection dataclass
"""

from dataclasses import dataclass, asdict
from typing import Union


@dataclass
class PostmanCollection:
    """
    Represents a Postman Collection in WAS
    """

    id: Union[str, int] = None
    name: str = None
    content: str = None
    fileSize: Union[str, int] = None

    def __post_init__(self):
        if self.id and isinstance(self.id, str):
            try:
                self.id = int(self.id)
            except ValueError:
                raise ValueError("id must be numeric")

        if self.fileSize and isinstance(self.fileSize, str):
            try:
                self.fileSize = int(self.fileSize)
            except ValueError:
                raise ValueError("fileSize must be numeric")

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id

    def size(self) -> int:
        return self.fileSize

    def to_dict(self):
        """
        Converts the object to a dictionary
        """
        return asdict(self)

    def __dict__(self):
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a PostmanCollection object from a dictionary
        """
        return cls(**data)
