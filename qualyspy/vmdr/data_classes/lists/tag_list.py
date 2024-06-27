"""
tag_list.py - contains the TagList and CloudTagList dataclasses.
"""

from dataclasses import dataclass, field
from typing import *
from typing import Iterator

from ..tag import Tag, CloudTag

from .base_list import BaseList


@dataclass
class TagList(BaseList):
    """
    TagList - represents a list of tag objects.

    This class is used to represent a list of tag objects.
    """

    _list: List[Tag] = field(default_factory=list)

    def __post_init__(self):
        # make sure that all elements in the list are Tag objects:
        for tag in self._list:
            if not isinstance(tag, Tag):
                raise TypeError(
                    f"TagList can only contain Tag objects, not {type(tag)}"
                )
            
    def __iter__(self) -> Iterator:
        return super().__iter__()
    
    def __len__(self) -> int:
        return super().__len__()

    def __repr__(self):
        return f"TagList({self._list})"

    def contains_id(self, id: int) -> bool:
        """
        contains_id - check if the list contains a tag with a specific ID.

        This function is used to check if the list contains a tag with a specific ID.
        """
        return any(tag.is_id(id) for tag in self._list)

    def contains_name(self, name: str) -> bool:
        """
        contains_name - check if the list contains a tag with a specific name.

        This function is used to check if the list contains a tag with a specific name.
        """
        return any(tag.is_name(name) for tag in self._list)

    @classmethod
    def from_dict(cls, data: List[dict]) -> "TagList":
        """
        from_dict - create a TagList object from a list of dictionaries.

        This function is used to create a TagList object from a list of dictionaries.
        """
        return cls([Tag.from_dict(tag) for tag in data])
    
@dataclass
class CloudTagList(BaseList):
    """
    CloudTagList - represents a list of cloud tag objects.

    This class is used to represent a list of cloud tag objects.
    """

    _list: List[CloudTag] = field(default_factory=list)

    def __post_init__(self):
        # make sure that all elements in the list are CloudTag objects:
        for tag in self._list:
            if not isinstance(tag, CloudTag):
                raise TypeError(
                    f"CloudTagList can only contain CloudTag objects, not {type(tag)}"
                )
            
    def __iter__(self) -> Iterator:
        return super().__iter__()
    
    def __len__(self) -> int:
        return super().__len__()

    def __repr__(self):
        return f"CloudTagList({self._list})"

    def contains_id(self, _id: int) -> bool:
        """
        contains_id - check if the list contains a cloud tag with a specific ID.

        This function is used to check if the list contains a cloud tag with a specific ID.
        """
        return any(tag.is_id(_id) for tag in self._list)

    def contains_name(self, name: str) -> bool:
        """
        contains_name - check if the list contains a cloud tag with a specific name.

        This function is used to check if the list contains a cloud tag with a specific name.
        """
        return any(tag.is_name(name) for tag in self._list)

    @classmethod
    def from_dict(cls, data: List[dict]) -> "CloudTagList":
        """
        from_dict - create a CloudTagList object from a list of dictionaries.

        This function is used to create a CloudTagList object from a list of dictionaries.
        """
        return cls([CloudTag.from_dict(tag) for tag in data])