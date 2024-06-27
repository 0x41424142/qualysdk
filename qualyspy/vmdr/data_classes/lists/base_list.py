"""
base_list.py - contains the BaseList class for the Qualyspy package.

The BaseList class is used as a base class for all list classes in the Qualyspy package.
"""

from dataclasses import dataclass, field
from typing import *


@dataclass(order=True)
class BaseList:
    """
    BaseList - represents a base list class for the Qualyspy package.

    This class is used as a base class for all list classes in the Qualyspy package.
    """

    _list: List = field(default_factory=list)

    def __iter__(self) -> Iterator:
        for item in self._list:
            yield item

    def __len__(self) -> int:
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]
    
    def __items__(self) -> List:
        return self._list
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._list})"


    def __setitem__(self, index, value) -> None:
        # do not allow duplicates:
        if value in self._list:
            raise ValueError("Cannot append duplicate items.")

        self._list[index] = value

    def __delitem__(self, index) -> None:
        del self._list[index]

    def __contains__(self, item) -> bool:
        return item in self._list

    def __str__(self) -> str:
        return ", ".join([str(item) for item in self._list])

    def __add__(self, other) -> Self:
        # do not allow duplicates:
        if any([item in self._list for item in other._list]):
            raise ValueError("Cannot append duplicate items.")

        return self.__class__(self._list + other._list)

    def __iadd__(self, other) -> Self:
        # do not allow duplicates:
        if any([item in self._list for item in other._list]):
            raise ValueError("Cannot append duplicate items.")

        self._list += other._list
        return self

    def __sub__(self, other) -> Self:
        return self.__class__([item for item in self._list if item not in other._list])

    def __isub__(self, other) -> Self:
        return self.__class__([item for item in self._list if item not in other._list])

    def append(self, item) -> None:
        # do not allow duplicates:
        if item in self._list:
            raise ValueError("Cannot append duplicate items.")

        self._list.append(item)

    def extend(self, items) -> None:
        # do not allow duplicates:
        to_extend_with = [item for item in items if item not in self._list]
        self._list.extend(to_extend_with)

    def insert(self, index, item) -> None:
        # do not allow duplicates:
        if item in self._list:
            raise ValueError("Cannot insert duplicate items.")

        self._list.insert(index, item)

    def remove(self, item) -> None:
        self._list.remove(item)

    def pop(self, index=-1) -> Any:
        return self._list.pop(index)

    def clear(self) -> None:
        self._list.clear()

    def copy(self) -> Self:
        return self.__class__([item for item in self._list])

    def is_empty(self) -> bool:
        return len(self._list) == 0

    def index(self, item) -> int:
        return self._list.index(item)
    
    def count(self, item) -> int:
        return self._list.count(item)
    
    
