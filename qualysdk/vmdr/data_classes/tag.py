"""
tag.py - contains the CloudTag and Tag dataclasses for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *
from datetime import datetime
from uuid import UUID

from ...base.base_class import BaseClass


@dataclass
class Tag(BaseClass):
    """
    Tag - represents a single tag in a TagList.

    This class is used to represent a single tag in a TagList, aka a tag on an asset.
    """

    TAG_ID: Union[str, int, UUID] = field(
        metadata={"description": "The ID of the tag."}
    )
    NAME: str = field(metadata={"description": "The name of the tag."})

    def __post_init__(self):
        # check that id is a string or int:
        if not isinstance(self.TAG_ID, (str, int, UUID)):
            raise TypeError(f"Tag ID must be a string or int, not {type(self.TAG_ID)}")

        # cast ID to an int if it is a string
        if isinstance(self.TAG_ID, str):
            self.TAG_ID = int(self.TAG_ID)

    def __str__(self) -> str:
        return self.NAME

    def __contains__(self, item):
        # see if it was found in the name or id:
        return item in self.TAG_ID or item in self.NAME

    def copy(self):
        return Tag(TAG_ID=self.TAG_ID, NAME=self.NAME)

    def is_id(self, id: int):
        return self.TAG_ID == id

    def is_name(self, name: str):
        return self.NAME == name

    def __iter__(self):
        yield self.TAG_ID
        yield self.NAME

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - create a Tag object from a dictionary.

        This function is used to create a Tag object from a dictionary.
        """
        # make sure that the dictionary has the required keys and nothing else:
        required_keys = {"TAG_ID", "NAME"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        # cast ID to an int if it is a string
        if isinstance(data["TAG_ID"], str):
            data["TAG_ID"] = int(data["TAG_ID"])

        return cls(**data)


@dataclass
class CloudTag(BaseClass):
    """
    CloudTag - represents a single tag in a CloudTagList.

    This class is used to represent a single tag in a CloudTagList, aka a tag on a cloud asset.
    """

    NAME: str = field(metadata={"description": "The name of the tag."})
    VALUE: str = field(metadata={"description": "The value of the tag."})
    LAST_SUCCESS_DATE: Optional[Union[str, datetime]] = field(
        default=None,
        metadata={"description": "The last successful date of the tag."},
    )

    def __post_init__(self):
        # check that the last success date is a string or datetime:
        if self.LAST_SUCCESS_DATE is not None and not isinstance(
            self.LAST_SUCCESS_DATE, (str, datetime)
        ):
            raise TypeError(
                f"Last success date must be a string or datetime, not {type(self.LAST_SUCCESS_DATE)}"
            )

        # cast last success date to a datetime if it is a string
        if isinstance(self.LAST_SUCCESS_DATE, str):
            self.LAST_SUCCESS_DATE = datetime.fromisoformat(self.LAST_SUCCESS_DATE)

    def __str__(self) -> str:
        return f"{self.NAME}:{self.VALUE}"

    def __contains__(self, item):
        # see if it was found in the name or value:
        return item in self.NAME or item in self.VALUE

    def copy(self):
        return CloudTag(NAME=self.NAME, VALUE=self.VALUE)

    def is_name(self, name: str):
        return self.NAME == name

    def is_value(self, value: str):
        return self.VALUE == value
