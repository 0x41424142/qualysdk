"""
Contains the WebApp class for WAS
"""

from datetime import datetime
from typing import Union
from dataclasses import dataclass, asdict

from .Tag import WASTag
from ...base.base_list import BaseList


@dataclass
class WebApp:
    """
    Represents a single Web Application in WAS
    """

    id: int = None
    name: str = None
    url: str = None
    riskScore: int = None
    owner: Union[dict, int] = None
    tags: Union[list, BaseList] = None
    createdDate: Union[str, datetime] = None
    updatedDate: Union[str, datetime] = None

    def __post_init__(self):
        DT_FIELDS = ["createdDate", "updatedDate"]
        INT_FIELDS = ["id", "riskScore"]

        for field in DT_FIELDS:
            value = getattr(self, field)
            if not isinstance(value, datetime):
                setattr(self, field, datetime.fromisoformat(value))

        for field in INT_FIELDS:
            value = getattr(self, field)
            if value and not isinstance(value, int):
                setattr(self, field, int(value))

        if self.owner:
            data = int(self.owner.get("id"))
            setattr(self, "owner", data)

        if "list" in self.tags.keys():
            bl = BaseList()
            data = self.tags.get("list").get("Tag")
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(WASTag.from_dict(tag))
            setattr(self, "tags", bl)
        else:
            setattr(self, "tags", None)

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
        return WebApp(**data)
