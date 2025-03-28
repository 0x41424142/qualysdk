"""
Contains the Container dataclass.
"""

from dataclasses import dataclass, asdict
from typing import Union
from datetime import datetime
from ipaddress import ip_address

from ...base.base_class import BaseClass
from ...base.base_list import BaseList
from ...exceptions.Exceptions import *


@dataclass
class Container(BaseClass):
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
    cluster: dict = None
    # cluster is parsed into below fields:
    cluster_name: str = None
    cluster_uid: str = None
    # End cluster fields
    users: list[dict] = None
    compliance: dict = None
    # compliance is parsed into below fields:
    compliance_failCount: int = None
    compliance_passCount: int = None
    compliance_errorCount: int = None
    # End compliance fields
    lastComplianceScanned: Union[str, datetime] = None
    cloudProvider: str = None
    exceptions: BaseList[str] = None
    riskScore: int = None
    riskScoreCalculatedDate: Union[str, datetime] = None
    formulaUsed: str = None
    maxQdsScore: int = None
    qdsSeverity: str = None
    scanTypes: list[str] = None
    criticality: str = None
    criticalityUpdated: Union[str, datetime] = None
    isExposedToWorld: bool = None
    k8sExposure: dict = None

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
            "riskScoreCalculatedDate",
            "criticalityUpdated",
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

        if self.cluster:
            setattr(self, "cluster_name", self.cluster.get("name"))
            setattr(self, "cluster_uid", self.cluster.get("uid"))
        del self.cluster

        if self.compliance:
            setattr(self, "compliance_failCount", self.compliance.get("failCount"))
            setattr(self, "compliance_passCount", self.compliance.get("passCount"))
            setattr(self, "compliance_errorCount", self.compliance.get("errorCount"))
        del self.compliance

        if self.portMapping:
            data = self.portMapping
            bl = BaseList()
            if isinstance(data, dict):
                data = [data]
            for item in data:
                bl.append(item)
            setattr(self, "portMapping", bl)

        # NOTE: I have yet to see any of the commented
        # out fields below. I will update this as needed.
        attributes_to_check = [
            "cloudProvider",
            "exceptions",
            "cluster",
            "isRoot",
            "softwares",
            "vulnerabilities",
            "drift",
            "arguments",
            "environment",
            "lastScanned",
            "operatingSystem",
            "users",
            "services",
            "hostArchitecture",
            "macAddress",
            "path",
            "label",
            "scanTypes",
            "criticality",
            "criticalityUpdated",
            "isExposedToWorld",
            "k8sExposure",
        ]

        for attribute in attributes_to_check:
            if getattr(self, attribute, None):
                print(
                    f"The {attribute} attribute does not have a defined structure. "
                    "Please submit a bug report if you see this message, or a PR with the attribute parsed out."
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
