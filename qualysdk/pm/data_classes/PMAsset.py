"""
Represents a Qualys Asset in Patch Management.
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime

from .Tag import Tag
from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass
class PMInterface(BaseClass):
    """
    Network Interface Data
    """

    interfaceName: str = None
    macAddress: str = None
    address: str = None
    gatewayAddress: str = None

    def __str__(self):
        return self.address


@dataclass
class PMAssetJobView(BaseClass):
    """
    Represents a Qualys Asset in Patch Management
    with additional job information attached.
    """

    id: str = None
    name: str = None
    operatingSystem: str = None
    jobId: str = None
    tags: BaseList[Tag] = None
    lastLoggedOnUser: str = None
    successPatches: int = None
    installedPatches: int = None
    failedPatches: int = None
    supersededPatches: int = None
    notApplicablePatches: int = None
    executing: Union[int, bool] = None
    pendingExecution: Union[int, bool] = None
    pendingReboot: Union[int, bool] = None
    pendingVerification: Union[int, bool] = None
    jobInstanceId: str = None
    interfaces: BaseList[PMInterface] = None
    skipPatchCount: int = None
    additionalFields: dict = None
    endDateTime: Union[int, datetime] = None
    startDateTime: Union[int, datetime] = None
    statusDateTime: Union[int, datetime] = None
    status: str = None
    statusCode: str = None
    jobSentOn: Union[int, datetime] = None
    installed: BaseList[str] = None
    failed: BaseList[str] = None
    success: BaseList[str] = None
    superseded: BaseList[str] = None
    notApplicable: BaseList[str] = None
    failedActionsCount: int = None
    successfulActionsCount: int = None
    skippedActionsCount: int = None
    interimResultStatus: str = None
    totalPatchCount: int = None
    runId: int = None
    scanDateTime: Union[int, datetime] = None
    pendingForRebootInAnotherJob: bool = None
    pendingForRebootInAnotherJobName: str = None
    osIdentifier: str = None

    def __post_init__(self):
        TO_BL_FIELDS = [
            "installed",
            "failed",
            "success",
            "superseded",
            "notApplicable",
        ]

        for bl_field in TO_BL_FIELDS:
            if getattr(self, bl_field):
                bl = BaseList()
                for obj in getattr(self, bl_field):
                    bl.append(obj)
                setattr(self, bl_field, bl)

        FROM_TIMESTAMP_FIELDS = [
            "endDateTime",
            "startDateTime",
            "statusDateTime",
            "jobSentOn",
            "scanDateTime",
        ]

        for timestamp_field in FROM_TIMESTAMP_FIELDS:
            if getattr(self, timestamp_field):
                setattr(
                    self,
                    timestamp_field,
                    datetime.fromtimestamp(getattr(self, timestamp_field) / 1000),
                )

        TO_BOOL_FIELDS = [
            "executing",
            "pendingExecution",
            "pendingReboot",
            "pendingVerification",
        ]

        for bool_field in TO_BOOL_FIELDS:
            if getattr(self, bool_field):
                setattr(self, bool_field, bool(getattr(self, bool_field)))

        if self.interfaces:
            bl = BaseList()
            for interface in self.interfaces:
                bl.append(PMInterface.from_dict(interface))
            setattr(self, "interfaces", bl)

        if self.tags:
            bl = BaseList()
            for tag in self.tags:
                bl.append(Tag.from_dict(tag))
            setattr(self, "tags", bl)

    def __str__(self):
        return self.name


@dataclass
class Asset(BaseClass):
    """
    Represents a Qualys Asset in Patch Management.
    """

    id: str = None
    name: str = None
    operatingSystem: str = None
    version: str = None
    platform: str = None
    osIdentifier: str = None
    tags: BaseList[Tag] = None
    interfaces: BaseList[PMInterface] = None
    scanStatus: str = None
    status: str = None
    statusCode: int = None
    installedPatchCount: int = None
    missingPatchCount: int = None
    nonSupersededMissingPatchCount: int = None
    activatedModules: BaseList[str] = None
    lastLoggedOnUser: str = None
    scanDateTime: Union[int, datetime] = None
    statusDateTime: Union[int, datetime] = None
    hardware: dict = None
    # hardware is parsed into below fields
    hardware_model: str = None
    hardware_manufacturer: str = None
    # end hardware
    architecture: str = None
    osNotSupportedForModules: BaseList[str] = None

    def __post_init__(self):
        # List of strings
        TO_BL_FIELDS = ["activatedModules", "osNotSupportedForModules"]

        for bl_field in TO_BL_FIELDS:
            if getattr(self, bl_field):
                bl = BaseList()
                for obj in getattr(self, bl_field):
                    bl.append(obj)
                setattr(self, bl_field, bl)

        FROM_TIMESTAMP_FIELDS = ["scanDateTime", "statusDateTime"]

        for timestamp_field in FROM_TIMESTAMP_FIELDS:
            if getattr(self, timestamp_field):
                try:
                    setattr(
                        self,
                        timestamp_field,
                        datetime.fromtimestamp(getattr(self, timestamp_field) / 1000),
                    )
                except (OSError, TypeError):
                    setattr(self, timestamp_field, None)

        if self.interfaces:
            bl = BaseList()
            for interface in self.interfaces:
                bl.append(PMInterface.from_dict(interface))
            setattr(self, "interfaces", bl)

        if self.tags:
            bl = BaseList()
            for tag in self.tags:
                bl.append(Tag.from_dict({"id": tag}))
            setattr(self, "tags", bl)

        if self.hardware:
            setattr(self, "hardware_model", self.hardware.get("model"))
            setattr(self, "hardware_manufacturer", self.hardware.get("manufacturer"))
            setattr(self, "hardware", None)
