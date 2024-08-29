"""
static_searchlist.py - Contains the search list dataclasses for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *
from datetime import datetime

from ...base.base_list import BaseList
from ..data_classes.report_template import ReportTemplate
from .kb_entry import KBEntry


@dataclass
class StaticSearchList:
    """
    StaticSearchList - represents a single Static Search List in VMDR.
    """

    ID: int = field(
        metadata={"description": "The ID of the Static Search List."}, default=None
    )
    TITLE: str = field(
        metadata={"description": "The title of the Static Search List."}, default=None
    )
    GLOBAL: bool = field(
        metadata={"description": "Whether the Static Search List is global."},
        default=None,
    )
    OWNER: str = field(
        metadata={"description": "The owner of the Static Search List."}, default=None
    )
    CREATED: Union[str, datetime] = field(
        metadata={"description": "The date the Static Search List was created."},
        default=None,
    )
    MODIFIED: Union[str, datetime] = field(
        metadata={"description": "The date the Static Search List was last modified."},
        default=None,
    )
    MODIFIED_BY: str = field(
        metadata={"description": "The user who last modified the Static Search List."},
        default=None,
    )
    QIDS: BaseList[KBEntry] = field(
        metadata={"description": "The QIDs associated with the Static Search List."},
        default=None,
    )

    OPTION_PROFILES: BaseList[str] = field(
        metadata={
            "description": "The option profiles associated with the Static Search List."
        },
        default=None,
    )

    REPORT_TEMPLATES: BaseList[str] = field(
        metadata={
            "description": "The report templates associated with the Static Search List."
        },
        default=None,
    )

    REMEDIATION_POLICIES: BaseList[str] = field(
        metadata={
            "description": "The remediation policies associated with the Static Search List."
        },
        default=None,
    )

    DISTRIBUTION_GROUPS: BaseList[str] = field(
        metadata={
            "description": "The distribution groups associated with the Static Search List."
        },
        default=None,
    )

    COMMENTS: str = field(
        metadata={
            "description": "The comments associated with the Static Search List."
        },
        default=None,
    )

    def __post_init__(self):
        # self.OPTION_PROFILES = BaseList(self.OPTION_PROFILES, dict)
        # self.REPORT_TEMPLATES = BaseList(self.REPORT_TEMPLATES, dict)
        # self.REMEDIATION_POLICIES = BaseList(self.REMEDIATION_POLICIES, dict)
        # self.DISTRIBUTION_GROUPS = BaseList(self.DISTRIBUTION_GROUPS, dict)

        if self.QIDS:
            bl = BaseList()
            data = self.QIDS["QID"]
            # check for one QID
            if isinstance(data, dict):
                data = [data]
            for qid in data:
                bl.append(KBEntry(QID=qid))
            self.QIDS = bl

        if self.OPTION_PROFILES:
            bl = BaseList()
            data = self.OPTION_PROFILES["OPTION_PROFILE"]
            # check for one option profile
            if isinstance(data, dict):
                data = [data]
            for profile in data:
                bl.append(f"{profile.get('ID', None)}: {profile.get('TITLE', None)}")
            self.OPTION_PROFILES = bl

        if self.REPORT_TEMPLATES:
            bl = BaseList()
            data = self.REPORT_TEMPLATES["REPORT_TEMPLATE"]
            # check for one report template
            if isinstance(data, dict):
                data = [data]
            for template in data:
                bl.append(ReportTemplate(**template))
            self.REPORT_TEMPLATES = bl

        if self.REMEDIATION_POLICIES:
            bl = BaseList()
            data = self.REMEDIATION_POLICIES["REMEDIATION_POLICY"]
            # check for one remediation policy
            if isinstance(data, dict):
                data = [data]
            for policy in data:
                bl.append(str(policy))
            self.REMEDIATION_POLICIES = bl

        if self.DISTRIBUTION_GROUPS:
            bl = BaseList()
            data = self.DISTRIBUTION_GROUPS["DISTRIBUTION_GROUP"]
            # check for one distribution group
            if isinstance(data, dict):
                data = [data]
            for group in data:
                bl.append(f"{group.get('ID', None)}: {group.get('TITLE', None)}")
            self.DISTRIBUTION_GROUPS = bl

        DT_FIELDS = ["CREATED", "MODIFIED"]

        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        self.ID = int(self.ID)

        self.GLOBAL = True if self.GLOBAL != "No" else False

    def __str__(self):
        return self.TITLE

    def __dict__(self):
        return asdict(self)

    def __iter__(self):
        for key in self.to_dict():
            yield key, getattr(self, key)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def contains_qid(self, qid: int) -> bool:
        """
        contains_qid - Determines if the Static Search List contains a specific QID.

        :param qid: The QID to check for.
        :type qid: int
        :return: Whether the QID is in the Static Search List.
        :rtype: bool
        """
        return any(detection.QID == qid for detection in self.QIDS)


@dataclass
class DynamicSearchList:
    """
    Dynamic Search List in VMDR.
    """

    ID: int = field(
        metadata={"description": "The ID of the Dynamic Search List."}, default=None
    )
    TITLE: str = field(
        metadata={"description": "The title of the Dynamic Search List."}, default=None
    )
    GLOBAL: bool = field(
        metadata={"description": "Whether the Dynamic Search List is global."},
        default=None,
    )
    OWNER: str = field(
        metadata={"description": "The owner of the Dynamic Search List."}, default=None
    )
    CREATED: Union[str, datetime] = field(
        metadata={"description": "The date the Dynamic Search List was created."},
        default=None,
    )
    MODIFIED: Union[str, datetime] = field(
        metadata={"description": "The date the Dynamic Search List was last modified."},
        default=None,
    )
    MODIFIED_BY: str = field(
        metadata={"description": "The user who last modified the Dynamic Search List."},
        default=None,
    )

    QIDS: BaseList[int] = field(
        metadata={"description": "The QIDs associated with the Dynamic Search List."},
        default=None,
    )

    CRITERIA: BaseList[str] = field(
        metadata={
            "description": "The criteria associated with the Dynamic Search List."
        },
        default=None,
    )

    OPTION_PROFILES: BaseList[str] = field(
        metadata={
            "description": "The option profiles associated with the Dynamic Search List."
        },
        default=None,
    )

    REPORT_TEMPLATES: BaseList[ReportTemplate] = field(
        metadata={
            "description": "The report templates associated with the Dynamic Search List."
        },
        default=None,
    )

    REMEDIATION_POLICIES: BaseList[str] = field(
        metadata={
            "description": "The remediation policies associated with the Dynamic Search List."
        },
        default=None,
    )

    DISTRIBUTION_GROUPS: BaseList[str] = field(
        metadata={
            "description": "The distribution groups associated with the Dynamic Search List."
        },
        default=None,
    )

    COMMENTS: str = field(
        metadata={
            "description": "The comments associated with the Dynamic Search List."
        },
        default=None,
    )

    def __post_init__(self):
        DT_FIELDS = ["CREATED", "MODIFIED"]

        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        self.ID = int(self.ID)

        self.GLOBAL = True if self.GLOBAL != "No" else False

        if self.QIDS:
            bl = BaseList()
            data = self.QIDS["QID"]
            # check for one QID
            if isinstance(data, dict):
                data = [data]
            for qid in data:
                bl.append(KBEntry(QID=qid))
            self.QIDS = bl

        if self.CRITERIA:
            bl = BaseList()
            data = self.CRITERIA
            # check for one criteria
            if isinstance(data, dict):
                data = [data]
            for criteria in data:
                s = ""
                for k, v in criteria.items():
                    # last item does not get comma at end of string:
                    if k == list(criteria.keys())[-1]:
                        s += f"{k}: {v}"
                    else:
                        s += f"{k}: {v}, "
                bl.append(s)
            self.CRITERIA = bl

        if self.OPTION_PROFILES:
            bl = BaseList()
            data = self.OPTION_PROFILES["OPTION_PROFILE"]
            # check for one option profile
            if isinstance(data, dict):
                data = [data]
            for profile in data:
                bl.append(f"{profile.get('ID', None)}: {profile.get('TITLE', None)}")
            self.OPTION_PROFILES = bl

        if self.REPORT_TEMPLATES:
            bl = BaseList()
            data = self.REPORT_TEMPLATES["REPORT_TEMPLATE"]
            # check for one report template
            if isinstance(data, dict):
                data = [data]
            for template in data:
                bl.append(ReportTemplate(**template))
            self.REPORT_TEMPLATES = bl

        if self.REMEDIATION_POLICIES:
            bl = BaseList()
            data = self.REMEDIATION_POLICIES["REMEDIATION_POLICY"]
            # check for one remediation policy
            if isinstance(data, dict):
                data = [data]
            for policy in data:
                bl.append(str(policy))
            self.REMEDIATION_POLICIES = bl

        if self.DISTRIBUTION_GROUPS:
            bl = BaseList()
            data = self.DISTRIBUTION_GROUPS["DISTRIBUTION_GROUP"]
            # check for one distribution group
            if isinstance(data, dict):
                data = [data]
            for group in data:
                bl.append(f"{group.get('ID', None)}: {group.get('TITLE', None)}")
            self.DISTRIBUTION_GROUPS = bl

    def __str__(self):
        return self.TITLE

    def __dict__(self):
        return asdict(self)

    def to_dict(self):
        return asdict(self)

    def __int__(self):
        return self.ID

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def contains_qid(self, qid: int) -> bool:
        """
        contains_qid - Determines if the Dynamic Search List contains a specific QID.

        :param qid: The QID to check for.
        :type qid: int
        :return: Whether the QID is in the Dynamic Search List.
        :rtype: bool
        """
        return any(detection.QID == qid for detection in self.QIDS)
