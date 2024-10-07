"""
Contains the WebAppAuthRecord class for the WAS module.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Union, Literal


@dataclass
class WebAppAuthRecord:
    """
    Represents an authentication record
    in Qualys WAS
    """

    id: Union[str, int] = None
    name: str = None
    owner: None = None
    # owner is parsed into below fields:
    owner_id: Union[str, int] = None
    owner_username: str = None
    owner_firstName: str = None
    owner_lastName: str = None
    # end owner
    tags: None = None
    # tags is parsed into below fields:
    tags_count: Union[str, int] = 0
    # end tags
    createdDate: Union[str, datetime] = None
    updatedDate: Union[str, datetime] = None

    def __post_init__(self):
        setattr(self, "id", int(self.id))

        DT_FIELDS = ["createdDate", "updatedDate"]

        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if self.owner:
            self.owner_id = int(self.owner.get("id"))
            self.owner_username = self.owner.get("username")
            self.owner_firstName = self.owner.get("firstName")
            self.owner_lastName = self.owner.get("lastName")
            setattr(self, "owner", None)

        if self.tags:
            self.tags_count = len(self.tags)
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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
