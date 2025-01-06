"""
Contains the Patch class
"""

from typing import Union
from datetime import datetime
from dataclasses import dataclass

from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass
class PackageDetail(BaseClass):
    """
    A package detail object in Qualys Patch Management
    """

    packageName: str = None
    architecture: str = None

    def __str__(self):
        return self.packageName


@dataclass
class Patch(BaseClass):
    """
    A patch object in Qualys Patch Management
    """

    id: str = None
    title: str = None
    type: str = None
    platform: str = None
    architecture: BaseList[str] = None
    bulletin: str = None
    category: str = None
    cve: BaseList[str] = None
    kb: str = None
    modifiedDate: Union[int, datetime] = None
    appFamily: str = None
    product: BaseList[str] = None
    publishedDate: Union[int, datetime] = None
    qid: BaseList[int] = None
    rebootRequired: bool = None
    supersededBy: BaseList[str] = None
    supersedes: BaseList[str] = None
    vendor: str = None
    vendorSeverity: str = None
    vendorlink: str = None
    missingCount: int = None
    installedCount: int = None
    downloadMethod: str = None
    advisory: str = None
    enabled: bool = None
    packageDetails: BaseList[PackageDetail] = None
    isSecurity: bool = None
    isSuperseded: bool = None
    isRollback: bool = None
    isCustomizedDownloadUrl: bool = None

    def __post_init__(self):
        DT_FIELDS = ["modifiedDate", "publishedDate"]
        BL_FIELDS = [
            "architecture",
            "product",
            "cve",
            "supersedes",
            "supersededBy",
            "qid",
        ]

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

        for field in BL_FIELDS:
            if field != "qid" and getattr(self, field):
                setattr(self, field, BaseList(getattr(self, field)))
            elif field == "qid" and getattr(self, field):
                setattr(
                    self, field, BaseList([int(qid) for qid in getattr(self, field)])
                )

        if getattr(self, "packageDetails"):
            bl = BaseList()
            for package in self.packageDetails:
                bl.append(PackageDetail(**package))
            setattr(self, "packageDetails", bl)
