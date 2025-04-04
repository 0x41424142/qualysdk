"""
Contains the Container dataclass.
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime
from ipaddress import ip_address

from .software import csSoftware
from .vulnerability import csVuln
from ...base.base_class import BaseClass
from ...base.base_list import BaseList


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
    host_sensorUuid: str = None
    host_hostname: str = None
    host_ipAddress: ip_address = None
    host_uuid: str = None
    host_lastUpdated: Union[str, datetime] = None
    hostArchitecture: str = None
    state: str = None
    portMapping: list[dict] = None
    stateChanged: Union[str, datetime] = None
    services: list[dict] = None
    operatingSystem: str = None
    lastScanned: Union[str, datetime] = None
    source: str = None
    environment: str = None
    arguments: BaseList[str] = None
    command: str = None
    drift: dict = None
    drift_category: BaseList[str] = None
    drift_reason: BaseList[str] = None
    drift_software: BaseList[csSoftware] = None
    drift_vulnerability: BaseList[csVuln] = None
    vulnerabilities: BaseList[csVuln] = None
    softwares: BaseList[csSoftware] = None
    isDrift: bool = None
    isRoot: bool = None
    cluster: dict = None
    cluster_name: str = None
    cluster_uid: str = None
    users: list[dict] = None
    compliance: dict = None
    compliance_failCount: int = None
    compliance_passCount: int = None
    compliance_errorCount: int = None
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
        self._convert_datetime_fields(
            [
                "created",
                "updated",
                "stateChanged",
                "lastScanned",
                "lastComplianceScanned",
                "riskScoreCalculatedDate",
                "criticalityUpdated",
            ]
        )
        self._convert_ip_fields(["ipv4", "ipv6"])
        self._process_host_fields()
        self._process_nested_fields(
            "host",
            "host",
            ["sensorUuid", "hostname", "uuid"],
            {"key": "ipAddress", "func": ip_address},
        )
        self._process_nested_fields("cluster", "cluster", ["name", "uid"])
        self._process_nested_fields(
            "compliance", "compliance", ["failCount", "passCount", "errorCount"]
        )
        self._process_drift_fields()
        self._process_field("softwares", csSoftware, add_sha=True)
        self._process_field("vulnerabilities", csVuln, add_sha=True)
        self._process_simple_fields(
            [
                "portMapping",
                "arguments",
                "environment",
                "hostArchitecture",
                "scanTypes",
                "users",
            ]
        )
        self._check_undefined_attributes()

    def _convert_datetime_fields(self, fields):
        for field in fields:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, datetime.fromtimestamp(int(value) / 1000))

    def _convert_ip_fields(self, fields):
        for field in fields:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, ip_address(value))

    def _process_host_fields(self):
        if self.host:
            for field in ["lastUpdated"]:
                value = self.host.get(field)
                if isinstance(value, str):
                    try:
                        setattr(
                            self,
                            f"host_{field}",
                            datetime.fromtimestamp(int(value) / 1000),
                        )
                    except ValueError:
                        setattr(self, f"host_{field}", datetime.fromisoformat(value))

    def _process_nested_fields(
        self, parent_field, target_prefix, fields, transform=None, wipe_parent=True
    ):
        parent_data = getattr(self, parent_field, {})
        if not parent_data:
            return

        if (
            transform
            and callable(transform.get("func"))
            and parent_data.get(transform["key"])
        ):
            setattr(
                self,
                f"{target_prefix}_{transform['key']}",
                transform["func"](parent_data[transform["key"]]),
            )

        for field in fields:
            if parent_data.get(field):
                value = parent_data[field]
                if isinstance(value, list):
                    setattr(self, f"{target_prefix}_{field}", BaseList(value))
                else:
                    setattr(self, f"{target_prefix}_{field}", value)

        if wipe_parent:
            setattr(self, parent_field, None)

    def _process_drift_fields(self):
        if self.drift:
            bl = BaseList()
            for vuln in self.drift.get("vulnerability", []):
                vuln["containerSha"] = self.sha
                bl.append(csVuln.from_dict(vuln))
            self.drift_vulnerability = bl
            self._process_nested_fields(
                "drift",
                "drift",
                ["category", "reason"],
                {
                    "key": "software",
                    "func": lambda x: BaseList(csSoftware.from_dict(x)),
                },
            )

    def _process_field(self, field_name, cls=None, add_sha=False):
        data = getattr(self, field_name, None)
        if not data:
            return
        bl = BaseList()
        if isinstance(data, dict):
            data = [data]
        for item in data:
            if add_sha:
                item["containerSha"] = self.sha
            bl.append(cls.from_dict(item) if cls else item)
        setattr(self, field_name, bl)

    def _process_simple_fields(self, fields):
        for field in fields:
            self._process_field(field)

    def _check_undefined_attributes(self):
        attributes_to_check = [
            "cloudProvider",
            "exceptions",
            "cluster",
            "services",
            "label",
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
