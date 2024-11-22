"""
Asset data class
"""

from dataclasses import dataclass, asdict
from typing import Union

from ...base.base_list import BaseList

"""
TODO: Move BaseCls into the package's base module
so it can be used universally. Things you realize 
months into a project...
"""


@dataclass
class BaseCls:
    pass

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
    def from_dict(cls, d: dict):
        return cls(**d)


@dataclass
class hostInstance(BaseCls):
    id: int = None
    port: int = None
    fqdn: str = None
    protocol: str = None
    service: str = None
    grade: str = None

    def __str__(self):
        return str(getattr(self, "id", ""))

    def __int__(self):
        return int(getattr(self, "id", 0))


@dataclass
class assetInterface(BaseCls):
    hostname: str = None
    address: str = None

    def __str__(self):
        return self.hostname if self.hostname else self.address


@dataclass
class Tag(BaseCls):
    name: str = None
    uuid: str = None

    def __str__(self):
        return self.name if self.name else self.uuid


@dataclass
class Asset(BaseCls):
    """
    Represents an asset in CERT,
    underneath a certificate
    data class.
    """

    id: int = None
    uuid: str = None
    netbiosName: str = None
    name: str = None
    operatingSystem: str = None
    hostInstances: Union[list[dict], BaseList[object]] = None
    assetInterfaces: Union[list[dict], BaseList[object]] = None
    tags: Union[list[str], BaseList[str]] = None
    primaryIp: str = None

    def __post_init__(self):
        if self.hostInstances:
            setattr(
                self,
                "hostInstances",
                BaseList([hostInstance(**x) for x in self.hostInstances]),
            )

        if self.assetInterfaces:
            setattr(
                self,
                "assetInterfaces",
                BaseList([assetInterface(**x) for x in self.assetInterfaces]),
            )

        if self.tags:
            setattr(self, "tags", BaseList([Tag(**x) for x in self.tags]))

    def __str__(self):
        return getattr(self, "name", "")
