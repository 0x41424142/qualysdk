from dataclasses import dataclass
from typing import Union
from datetime import datetime

from ...base.base_class import BaseClass
from ...base.base_list import BaseList


@dataclass
class TagSimple(BaseClass):
    id: int = None
    name: str = None

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name


@dataclass
class Tag(BaseClass):
    id: int = None
    name: str = None
    modified: Union[str, datetime] = None
    ruleType: str = None
    parentTagId: int = None
    ruleText: str = None
    created: Union[str, datetime] = None
    children: Union[dict, BaseList[TagSimple]] = None
    color: str = None
    criticalityScore: int = None
    description: str = None
    srcAssetGroupId: int = None
    srcBusinessUnitId: int = None
    provider: str = None

    def __post_init__(self):
        DT_FIELDS = ["modified", "created"]
        for field in DT_FIELDS:
            if getattr(self, field):
                setattr(
                    self,
                    field,
                    datetime.strptime(getattr(self, field), "%Y-%m-%dT%H:%M:%SZ"),
                )

        if self.children:
            bl = BaseList()
            for childTag in self.children.get("list", {}):
                bl.append(TagSimple.from_dict(childTag["TagSimple"]))
            self.children = bl

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name

    @property
    def parent(self):
        return self.parentTagId

    @property
    def has_parent(self):
        return self.parentTagId is not None

    # to make it a hashable type:
    def __hash__(self):
        return hash(self.id)
