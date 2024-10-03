"""
Contains the UrlEntry class for WAS
"""

from dataclasses import dataclass, asdict
from typing import Union


@dataclass
class UrlEntry:
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
        return UrlEntry(**data)
