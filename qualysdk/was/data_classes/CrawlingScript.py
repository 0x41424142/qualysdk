"""
Contains the CrawlingScript class for WAS
"""

from dataclasses import dataclass, asdict
from typing import Union


@dataclass
class CrawlingScript:
    """
    Represents a crawl scriptin WAS
    """

    id: int = None
    name: str = None
    data: str = None
    regex: str = None
    requiresAuthentication: Union[str, bool] = None
    startingUrl: str = None
    startingUrlRegex: Union[str, bool] = None

    def __post_init__(self):
        if self.id and isinstance(self.id, str):
            try:
                self.id = int(self.id)
            except ValueError:
                raise ValueError("id must be numeric")

        if self.requiresAuthentication and isinstance(self.requiresAuthentication, str):
            match self.requiresAuthentication.lower():
                case "true":
                    self.requiresAuthentication = True
                case "false":
                    self.requiresAuthentication = False
                case _:
                    raise ValueError("requiresAuthentication must be a boolean")

        if self.startingUrlRegex and isinstance(self.startingUrlRegex, str):
            match self.startingUrlRegex.lower():
                case "true":
                    self.startingUrlRegex = True
                case "false":
                    self.startingUrlRegex = False
                case _:
                    raise ValueError("startingUrlRegex must be a boolean")

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

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
        return CrawlingScript(**data)
