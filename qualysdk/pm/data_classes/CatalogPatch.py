from dataclasses import dataclass
from datetime import datetime
from typing import Union

from ...base.base_class import BaseClass
from ...base.base_list import BaseList

DT_FIELDS = [
    "syncDateTime",
    "modifiedDate",
    "publishedDate",
]

BL_STR_FIELDS = [
    "appFamily",
    "product",
    "qid",
    "supersedes",
    "cve",
    "architecture",
    "supersededBy",
    "supportedOs",
]


@dataclass
class PackageDetail(BaseClass):
    """
    Linux package details.
    """

    packageName: str = None
    architecture: str = None
    patchId: str = None

    def __str__(self):
        return f"{self.packageName} ({self.architecture})"


@dataclass
class CatalogPatch(BaseClass):
    """
    A data class representing a patch in the Qualys Patch Management catalog.
    """

    patchId: str = None
    id: str = None
    title: str = None
    type: str = None
    appFamily: BaseList[str] = None
    vendor: str = None
    product: BaseList[str] = None
    platform: str = None
    kb: str = None
    isSuperseded: bool = None
    isSecurity: bool = None
    isRollback: bool = None
    servicePack: bool = None
    advisory: str = None
    vendorlink: str = None
    osIdentifier: str = None
    advisoryLink: str = None
    deleted: bool = None
    rebootRequired: bool = None
    vendorSeverity: str = None
    description: str = None
    qid: BaseList[int] = None
    enabled: bool = None
    downloadMethod: str = None
    supportedOs: str = None
    supersedes: BaseList[str] = None
    notification: str = None
    cve: BaseList[str] = None
    architecture: BaseList[str] = None
    packageDetails: BaseList[PackageDetail] = None
    patchFeedProviderId: int = None
    syncDateTime: Union[int, datetime] = None
    vendorPatchId: Union[str, int] = None
    modifiedDate: Union[int, datetime] = None
    publishedDate: Union[int, datetime] = None
    category: str = None
    isEsuPatch: bool = None
    supersededBy: BaseList[str] = None
    bulletin: str = None

    def __post_init__(self):
        for field in DT_FIELDS:
            if getattr(self, field):
                try:
                    setattr(
                        self,
                        field,
                        datetime.fromtimestamp(getattr(self, field) / 1000),
                    )
                except (TypeError, OSError, ValueError):
                    setattr(self, field, None)

        for field in BL_STR_FIELDS:
            if getattr(self, field):
                setattr(self, field, BaseList(getattr(self, field)))

        if self.notification:
            print(
                "CatalogPatch's notification attribute is currently not parsed and is set to a string. Please submit a PR adding the functionality to parse this attribute."
            )
            setattr(self, "notification", str(self.notification))

        if self.packageDetails:
            bl = BaseList()
            for pd in self.packageDetails:
                bl.append(PackageDetail(**pd))
            setattr(self, "packageDetails", bl)
