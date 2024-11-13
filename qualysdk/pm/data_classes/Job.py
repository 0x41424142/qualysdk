"""
Contains the data classes used for Patch Management Jobs.
"""

from dataclasses import dataclass, asdict
from typing import Union
from datetime import datetime
from string import digits

from .Tag import Tag
from ...base.base_list import BaseList


@dataclass
class PMJob:
    """
    Represents a deployment job in Patch Management.
    """

    id: str = None
    name: str = None
    coAuthorUserIds: BaseList[str] = None
    subCategory: str = None
    dynamicQQLType: int = None
    matchAllTags: BaseList[str] = None
    type: str = None
    recurringWeekDays: str = None
    totalAssetCount: int = None
    isDynamicPatchesQQL: bool = None
    assetCount: Union[int, None] = None
    customPatchUrlConfigured: bool = None
    linkedJobReferenceCount: Union[int, None] = None
    created: dict = None
    # created is parsed into below fields:
    created_date: Union[int, datetime] = None
    created_user_name: str = None
    created_user_id: str = None
    # end created
    triggerStatus: int = None
    recurringDayOfMonth: str = None
    jobSource: int = None
    readOnly: bool = None
    tags: BaseList[Tag] = None
    exclusionAssetIds: BaseList[str] = None
    scheduleType: str = None
    dayOfMonth: str = None
    disabledPatches: BaseList[str] = None
    filterType: str = None
    updated: dict = None
    # updated is parsed into below fields:
    updated_date: Union[int, datetime] = None
    updated_user_name: str = None
    updated_user_id: str = None
    # end updated
    additionalQQLS: BaseList[str] = None
    status: str = None
    timezone: str = None
    exclusionFilterType: str = None
    nextScheduleDateTime: Union[str, datetime] = None
    platform: str = None
    mitigationActionCount: int = None
    isPriorityJob: bool = None
    customerId: str = None
    exclusionTags: BaseList[Tag] = None
    taggedAssetCount: int = None
    patchCount: int = None
    applicableAssetCount: int = None
    patchTuesdayPlusXDays: int = None
    schemaVersion: float = None
    recurringLastDayOfMonth: bool = None
    recurringWeekDayOfMonth: str = None
    isRecurring: bool = None
    lastScheduleDateTime: Union[str, datetime] = None
    dynamicPatchesQQL: str = None
    startDateTime: Union[str, datetime] = None
    timezoneType: str = None
    deleted: bool = None
    monthlyRecurringType: int = None
    completionPercent: float = None
    category: int = None
    linkedJobId: str = None
    assetResultReceivedCount: int = None
    isVulnContext: bool = None
    isAssetImported: bool = None
    remediationQids: BaseList[str] = None

    def __post_init__(self):
        # Define attributes that need to be converted
        # in a specific way

        TO_INT_FIELDS = [
            "totalAssetCount",
            "assetResultReceivedCount",
            "applicableAssetCount",
        ]

        FROM_TIMESTAMP_FIELDS = [
            "nextScheduleDateTime",
            "lastScheduleDateTime",
        ]

        BREAKDOWN_DT_FIELDS = [
            "created",
            "updated",
        ]

        TAG_OBJ_FIELDS = [
            "tags",
            "exclusionTags",
        ]

        NON_STR_OR_OBJ_BASELIST_FIELDS = [
            "remediationQids",
        ]

        """
        CURRENT FIELDS THAT I HAVE NOT BEEN ABLE TO
        DETERMINE THE STRUCTURE OF:

        matchAllTags
        assetCount
        exclusionAssetIds
        disabledPatches
        additionalQQLS
        recurringLastDayOfMonth
        """

        if self.schemaVersion:
            setattr(self, "schemaVersion", float(self.schemaVersion))

        if self.completionPercent and all(
            [char in digits for char in str(self.completionPercent)]
        ):
            setattr(self, "completionPercent", float(self.completionPercent))

        if self.coAuthorUserIds:
            setattr(self, "coAuthorUserIds", BaseList(self.coAuthorUserIds))

        if self.startDateTime:
            setattr(
                self,
                "startDateTime",
                datetime.strptime(self.startDateTime, "%Y-%m-%d %I:%M:%S %p"),
            )

        for base_list_field in NON_STR_OR_OBJ_BASELIST_FIELDS:
            if getattr(self, base_list_field):
                setattr(self, base_list_field, BaseList(getattr(self, base_list_field)))

        for tag_obj in TAG_OBJ_FIELDS:
            if getattr(self, tag_obj):
                setattr(
                    self,
                    tag_obj,
                    BaseList([Tag.from_dict(tag) for tag in getattr(self, tag_obj)]),
                )

        for dt_field in BREAKDOWN_DT_FIELDS:
            if getattr(self, dt_field):
                setattr(
                    self,
                    f"{dt_field}_date",
                    datetime.fromtimestamp(getattr(self, dt_field)["date"] / 1000),
                )
                setattr(
                    self,
                    f"{dt_field}_user_name",
                    getattr(self, dt_field)["user"].get("name"),
                )
                setattr(
                    self,
                    f"{dt_field}_user_id",
                    getattr(self, dt_field)["user"].get("id"),
                )
                setattr(self, dt_field, None)

        for timestamp_field in FROM_TIMESTAMP_FIELDS:
            if getattr(self, timestamp_field):
                setattr(
                    self,
                    timestamp_field,
                    datetime.fromtimestamp(getattr(self, timestamp_field) / 1000),
                )

        for int_field in TO_INT_FIELDS:
            if getattr(self, int_field):
                setattr(self, int_field, int(getattr(self, int_field)))

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return asdict(self)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()
