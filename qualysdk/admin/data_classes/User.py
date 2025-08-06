"""
Represents a single user in the Qualys platform from the Administration module.
"""

from dataclasses import dataclass, field
from typing import Union, Optional

from ...base.base_class import BaseClass
from ...base.base_list import BaseList


@dataclass
class AdminDataPoint(BaseClass):
    """
    Represents a single scope tag or role in the Qualys platform.
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


@dataclass
class User(BaseClass):
    id: int
    username: str
    firstName: str
    lastName: str
    emailAddress: str
    title: str
    scopeTags: Optional[Union[list[AdminDataPoint], BaseList[AdminDataPoint]]] = field(
        default_factory=BaseList
    )
    roleList: Optional[Union[list[AdminDataPoint], BaseList[AdminDataPoint]]] = field(
        default_factory=BaseList
    )

    def __post_init__(self):
        # grab roleList:
        if self.roleList and "list" not in self.roleList:
            role = AdminDataPoint(**self.roleList)
            self.roleList = BaseList([role])
        elif self.roleList:
            self.roleList = BaseList(
                [AdminDataPoint(**role["RoleData"]) for role in self.roleList["list"]]
            )
        # grab scopeTags:
        if self.scopeTags and "list" not in self.scopeTags:
            tag = AdminDataPoint(**self.scopeTags)
            self.scopeTags = BaseList([tag])
        elif self.scopeTags:
            self.scopeTags = BaseList(
                [AdminDataPoint(**tag["TagData"]) for tag in self.scopeTags["list"]]
            )

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.username})"

    def __int__(self):
        return self.id
