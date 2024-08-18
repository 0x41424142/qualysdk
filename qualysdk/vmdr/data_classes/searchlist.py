"""
static_searchlist.py - Contains the search list dataclasses for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *
from datetime import datetime

from ...base.base_list import BaseList
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

    OPTION_PROFILES: BaseList[dict] = field(
        metadata={
            "description": "The option profiles associated with the Static Search List."
        },
        default=None,
    )

    REPORT_TEMPLATES: BaseList[dict] = field(
        metadata={
            "description": "The report templates associated with the Static Search List."
        },
        default=None,
    )

    REMEDIATION_POLICIES: BaseList[dict] = field(
        metadata={
            "description": "The remediation policies associated with the Static Search List."
        },
        default=None,
    )

    DISTRIBUTION_GROUPS: BaseList[dict] = field(
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
            # check for one QID
            if isinstance(self.QIDS["QID"], str):
                self.QIDS = [self.QIDS["QID"]]
            else:
                # Raise ['QID'] list up a level
                self.QIDS = self.QIDS["QID"]

            for qid in self.QIDS:
                bl.append(KBEntry(QID=qid))
            self.QIDS = bl

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
        for key in self.__dict__():
            yield key, getattr(self, key)

    def keys(self):
        return self.__dict__().keys()

    def values(self):
        return self.__dict__().values()

    def items(self):
        return self.__dict__().items()

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
