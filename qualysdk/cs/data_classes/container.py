"""
Contains the Container dataclass.
"""

from dataclasses import dataclass, asdict
from typing import Union, Literal
from datetime import datetime
from ipaddress import ip_address

from ...base.base_list import BaseList
from ...exceptions.Exceptions import *


@dataclass
class Container:
    """
    Represents a Docker container.
    """

    imageId: str = None
    imageUuid: str = None
    containerId: str = None
    created: Union[str, datetime] = None
    updated: Union[str, datetime] = None
    label: str = None
    uuid: str = None
    sha: str = None
    privileged: bool = None
    path: str = None
    imageSha: str = None
    macAddress: str = None
    customerUuid: str = None
    ipv4: ip_address = None
    ipv6: ip_address = None
    name: str = None
    host: dict = None
    # host is parsed into below fields:
    host_sensorUuid: str = None
    host_hostname: str = None
    host_ipAddress: ip_address = None
    host_uuid: str = None
    host_lastUpdated: Union[str, datetime] = None
    # End host fields
    hostArchitecture: str = None
    state: str = None
    portMapping: list[dict] = None
    stateChanged: Union[str, datetime] = None
    services: list[dict] = None
    operatingSystem: str = None
    lastScanned: Union[str, datetime] = None
    source: str = None
    environment: str = None
    arguments: str = None
    command: str = None
    drift: dict = None
    vulnerabilities: dict = None
    softwares: dict = None
    isDrift: bool = None
    isRoot: bool = None
    cluster: str = None
    users: list[dict] = None
    lastComplianceScanned: Union[str, datetime] = None
    cloudProvider: str = None
    exceptions: BaseList[str] = None

    def __post_init__(self):
        """
        Post-initialization function for the Container class.
        """

        # Convert any datetime strings to datetime objects using fromtimestamp:
        DT_FIELDS = [
            "created",
            "updated",
            "stateChanged",
            "lastScanned",
            "lastComplianceScanned",
        ]
        for field in DT_FIELDS:
            if isinstance(getattr(self, field), str):
                setattr(
                    self,
                    field,
                    datetime.fromtimestamp(int(getattr(self, field)) / 1000),
                )

        # Convert any IP address strings to ip_address objects:
        IP_FIELDS = ["ipv4", "ipv6"]
        for field in IP_FIELDS:
            if isinstance(getattr(self, field), str):
                setattr(self, field, ip_address(getattr(self, field)))

        if self.label:
            print(
                "The label attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.path:
            print(
                "The path attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.macAddress:
            print(
                "The macAddress attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.host:
            host_dt_fields = ["lastUpdated"]
            for field in host_dt_fields:
                if isinstance(self.host.get(field), str):
                    setattr(
                        self.host,
                        f"host_{field}",
                        datetime.fromtimestamp(int(self.host[field]) / 1000),
                    )

            if self.host.get("ipAddress"):
                setattr(self, "host_ipAddress", ip_address(self.host["ipAddress"]))

            host_fields = ["sensorUuid", "hostname", "uuid"]
            for field in host_fields:
                if self.host.get(field):
                    setattr(self, f"host_{field}", self.host[field])

            # Set the original host field to None:
            setattr(self, "host", None)

        # NOTE: I have yet to see any of the commented
        # out fields below. I will update this as needed.
        if self.hostArchitecture:
            print(
                "The hostArchitecture attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.services:
            print(
                "The services attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.users:
            print(
                "The users attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.operatingSystem:
            print(
                "The operatingSystem attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.lastScanned:
            print(
                "The lastScanned attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.environment:
            print(
                "The environment attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.arguments:
            print(
                "The arguments attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.drift:
            print(
                "The drift attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.vulnerabilities:
            print(
                "The vulnerabilities attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.softwares:
            print(
                "The softwares attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.isRoot:
            print(
                "The isRoot attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.cluster:
            print(
                "The cluster attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.portMapping:
            data = self.portMapping
            bl = BaseList()
            if isinstance(data, dict):
                data = [data]
            for item in data:
                bl.append(item)
            setattr(self, "portMapping", bl)

        if self.cloudProvider:
            print(
                "The cloudProvider attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

        if self.exceptions:
            print(
                "The exceptions attribute does not have a defined structure. Please submit a bug report if you see this message, or a PR with the attribute parsed out."
            )

    def has_drift(self) -> bool:
        """
        Check if the container has drift.

        Returns:
            bool: True if the container has drift, False otherwise.
        """
        return self.isDrift

    def is_root(self) -> bool:
        """
        Check if the container is running as root.

        Returns:
            bool: True if the container is running as root, False otherwise.
        """
        return self.isRoot

    def __dict__(self) -> dict:
        """
        Return the object as a dictionary.

        Returns:
            dict: The object as a dictionary.
        """
        return asdict(self)

    def to_dict(self) -> dict:
        """
        Return the object as a dictionary.

        Returns:
            dict: The object as a dictionary.
        """
        return asdict(self)

    def keys(self) -> list[str]:
        """
        Return the keys of the object.

        Returns:
            list[str]: The keys of the object.
        """
        return self.to_dict().keys()

    def values(self) -> list:
        """
        Return the values of the object.

        Returns:
            list: The values of the object.
        """
        return self.to_dict().values()

    def items(self) -> list[tuple]:
        """
        Return the items of the object.

        Returns:
            list[tuple]: The items of the object.
        """
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
