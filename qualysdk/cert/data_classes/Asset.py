"""
Asset data class
"""

from dataclasses import dataclass, asdict
from typing import Union

from ...base.base_class import BaseClass
from ...base.base_list import BaseList


@dataclass
class hostInstance(BaseClass):
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
class assetInterface(BaseClass):
    hostname: str = None
    address: str = None

    def __str__(self):
        return self.hostname if self.hostname else self.address


@dataclass
class Tag(BaseClass):
    name: str = None
    uuid: str = None

    def __str__(self):
        return self.name if self.name else self.uuid


@dataclass
class Asset(BaseClass):
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
