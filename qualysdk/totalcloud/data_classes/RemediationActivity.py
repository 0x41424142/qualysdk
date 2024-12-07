"""
Contains the RemediationActivity dataclass.
"""

from dataclasses import dataclass
from typing import Union, Literal
from datetime import datetime

from ...base.base_class import BaseClass
from ...base.base_list import BaseList
from ...exceptions.Exceptions import *


@dataclass
class RemediationActivity(BaseClass):
    """
    Represents a remediation activity in TotalCloud.
    """

    resourceId: str = None
    controlId: int = None
    cloudType: Literal["AWS", "AZURE"] = None
    # accountId depends on the cloudType
    accountId: Union[str, int] = None
    region: str = None
    status: str = None
    resourceType: str = None
    remediationAction: str = None
    connectorName: str = None
    policyNames: BaseList[str] = None
    controlName: str = None
    triggeredOn: Union[str, datetime] = None
    Errors: str = None
    triggeredBy: str = None
    remediationReason: str = None

    def __post_init__(self):
        DT_FIELDS = ["triggeredOn"]

        for field in DT_FIELDS:
            if not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if self.cloudType:
            if self.cloudType.upper() == "AWS":
                self.accountId = int(self.accountId)

        if self.Errors:
            setattr(self, "errors", str(self.Errors))

        if self.policyNames:
            bl = BaseList()
            for policy in self.policyNames:
                bl.append(policy)
            setattr(self, "policyNames", bl)
