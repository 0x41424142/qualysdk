"""
Contains the Comment class for WAS
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime

from ...base.base_class import BaseClass
from ...base import DONT_EXPAND


@dataclass
class Comment(BaseClass):
    """
    Represents a comment on a WAS object
    """

    contents: str = ""
    author: None = None
    author_id: Union[str, int] = None
    author_username: str = None
    author_firstName: str = None
    author_lastName: str = None
    createdDate: Union[str, datetime] = None

    def __post_init__(self):
        if self.createdDate and isinstance(self.createdDate, str):
            # format: 2023-12-08T09:57:51Z
            setattr(
                self,
                "createdDate",
                datetime.strptime(self.createdDate, "%Y-%m-%dT%H:%M:%SZ"),
            )

        if not DONT_EXPAND.flag:
            if self.author:
                setattr(self, "author_id", int(self.author.get("id")))
                setattr(self, "author_username", self.author.get("username"))
                setattr(self, "author_firstName", self.author.get("firstName"))
                setattr(self, "author_lastName", self.author.get("lastName"))
                setattr(self, "author", None)

        if self.author_id:
            try:
                self.author_id = int(self.author_id)
            except ValueError:
                raise ValueError("author_id must be numeric")

    def __str__(self) -> str:
        return self.contents
