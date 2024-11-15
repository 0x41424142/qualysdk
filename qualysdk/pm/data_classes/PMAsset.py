"""
Represents a Qualys Asset in Patch Management.
"""

from dataclasses import dataclass, asdict
from typing import Union
from datetime import datetime

from .Tag import Tag
from ...base.base_list import BaseList


@dataclass
class PMInterface:
    """
    Network Interface Data
    """

    interfaceName: str = None
    macAddress: str = None
    address: str = None
    gatewayAddress: str = None

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return asdict(self)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    def __str__(self):
        return self.address

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)


@dataclass
class PMAssetJobView:
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
                bl.append(PMInterface.from_dict(**interface))
            setattr(self, "interfaces", bl)

        if self.tags:
            bl = BaseList()
            for tag in self.tags:
                bl.append(Tag.from_dict(tag))
            setattr(self, "tags", bl)

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return asdict(self)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    def __str__(self):
        return self.name

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)
