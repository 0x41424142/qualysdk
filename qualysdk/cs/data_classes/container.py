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
    arguments: BaseList[str] = None
    command: str = None
    drift: dict = None
    # drift is parsed into below fields:
    drift_category: BaseList[str] = None
    drift_reason: BaseList[str] = None
    drift_software: BaseList[csSoftware] = None
    drift_vulnerability: BaseList[csVuln] = None
    # End drift fields
    vulnerabilities: BaseList[csVuln] = None
    softwares: BaseList[csSoftware] = None
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
                    try:
                        setattr(
                            self,
                            f"host_{field}",
                            datetime.fromtimestamp(int(self.host[field]) / 1000),
                        )
                    except ValueError:
                        setattr(self, f"host_{field}", datetime.fromisoformat(self.host[field]))

        def process_nested_fields(parent_field, target_prefix, fields, transform=None, wipe_parent=True):
            """
            Process nested fields from the parent field into the target prefix.
            Args:
                parent_field (str): The name of the parent field.
                target_prefix (str): The prefix for the target fields.
                fields (list): List of fields to process.
                transform (dict, optional): A dictionary with a key and a function to transform the data.
                wipe_parent (bool, optional): Whether to wipe the parent field after processing.

            Returns:
                None
            """
            parent_data = getattr(self, parent_field, {})
            if not parent_data:
                return
            
            if transform and callable(transform) and parent_data.get(transform["key"]):
                setattr(self, f"{target_prefix}_{transform['key']}", transform["func"](parent_data[transform["key"]]))

            for field in fields:
                if parent_data.get(field):
                    # if a regular list, convert to BaseList:
                    if isinstance(parent_data[field], list):
                        bl = BaseList()
                        for item in parent_data[field]:
                            bl.append(item)
                        setattr(self, f"{target_prefix}_{field}", bl)
                    else:
                        setattr(self, f"{target_prefix}_{field}", parent_data[field])
            if wipe_parent:
                setattr(self, parent_field, None)
        
        process_nested_fields("host", "host", ["sensorUuid", "hostname", "uuid"], {"key": "ipAddress", "func": ip_address})
        process_nested_fields("cluster", "cluster", ["name", "uid"])
        process_nested_fields("compliance", "compliance", ["failCount", "passCount", "errorCount"])
        bl = BaseList()
        # doing drift vulns here as a special case since process_nested_fields
        # currently only handles one key
        for vuln in self.drift.get("vulnerability", []):
            vuln["containerSha"] = self.sha
            bl.append(csVuln.from_dict(vuln))
        setattr(self, "drift_vulnerability", bl)
        process_nested_fields("drift", "drift", ["category", "reason"], {"key": "software", "func": lambda x: BaseList(csSoftware.from_dict(x))})

        def process_field(field_name, cls=None, add_sha=False):
            data = getattr(self, field_name)
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
        
        process_field("softwares", csSoftware, add_sha=True)
        process_field("vulnerabilities", csVuln, add_sha=True)
        # process the simpler fields:
        [process_field(field) for field in ["portMapping", "arguments", "environment", "hostArchitecture", "scanTypes", "users"]]

        # NOTE: I have yet to see any of the commented
        # out fields below. I will update this as needed.
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
