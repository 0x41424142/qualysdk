"""
Contains the PostmanCollection dataclass
"""

from dataclasses import dataclass
from typing import Union

from ...base.base_class import BaseClass


@dataclass
class PostmanCollection(BaseClass):
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
