"""
Contains the UrlEntry class for WAS
"""

from dataclasses import dataclass
from typing import Union

from ...base.base_class import BaseClass


@dataclass
class UrlEntry(BaseClass):
    """
    Represents a single URL entry in WAS
    """

    regex: Union[str, bool] = None
    text: str = None

    def __post_init__(self):
        if self.regex and isinstance(self.regex, str):
            match self.regex.lower():
                case "true":
                    self.regex = True
                case "false":
                    self.regex = False
                case _:
                    raise ValueError("regex must be a boolean")
        else:
            self.regex = False

    def __str__(self):
        return self.text
