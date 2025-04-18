"""
contains the Control dataclass for the TotalCloud API
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime

# suppress warning from bs4
import warnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

from ...base.base_list import BaseList
from ...base.base_class import BaseClass
from ...base import DONT_EXPAND

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


@dataclass
class Control(BaseClass):
    """
    Represents a single control that Qualys checks a cloud provider for.
    """

    cid: int = None
    controlName: str = None
    created: Union[str, datetime] = None
    modified: Union[str, datetime] = None
    controlType: str = None
    provider: str = None
    isCustomizable: bool = None
    serviceType: str = None
    criticality: str = None
    evaluation: None = None
    # BELOW FIELDS ARE PARSED OUT OF EVALUATION:
    evaluation_description: str = None  # NEEDS TO BE PARSED WITH BS4!
    evaluation_passMessage: str = None
    evaluation_failMessage: str = None
    evaluation_criteria: BaseList[str] = None  # come back to this one?
    # END OF EVALUATION FIELDS
    specification: str = None  # NEEDS TO BE PARSED WITH BS4!
    rationale: str = None  # NEEDS TO BE PARSED WITH BS4!
    manualRemediation: str = None  # NEEDS TO BE PARSED WITH BS4!
    references: str = None  # NEEDS TO BE PARSED WITH BS4!
    buildTimeRemediation: str = None  # NEEDS TO BE PARSED WITH BS4!
    resourceType: str = None
    remediationEnabled: bool = None
    policyNames: BaseList[str] = None
    executionType: str = None
    workflowBased: bool = None
    templateType: BaseList[str] = None

    def __post_init__(self):
        """
        __post_init__ - post initialization method for the Control dataclass
        """
        if self.created:
            setattr(self, "created", datetime.fromisoformat(self.created))

        if self.modified:
            setattr(self, "modified", datetime.fromisoformat(self.modified))

        if not DONT_EXPAND.flag:
            if self.evaluation:
                FIELDS = ["description", "passMessage", "failMessage"]
                for field in FIELDS:
                    if self.evaluation.get(field):
                        setattr(
                            self,
                            f"evaluation_{field}",
                            self.evaluation.get(field, None),
                        )
                if self.evaluation.get("criteria"):
                    setattr(
                        self,
                        "evaluation_criteria",
                        BaseList(self.evaluation.get("criteria")),
                    )
                self.evaluation = None

            BL_FIELDS = ["policyNames", "templateType"]
            for field in BL_FIELDS:
                if getattr(self, field):
                    setattr(self, field, BaseList(getattr(self, field)))

        BS4_FIELDS = [
            "specification",
            "rationale",
            "manualRemediation",
            "references",
            "evaluation_description",
            "buildTimeRemediation",
        ]
        for field in BS4_FIELDS:
            if getattr(self, field):
                setattr(
                    self,
                    field,
                    BeautifulSoup(getattr(self, field), "html.parser").get_text(),
                )

    def __int__(self):
        return self.cid


@dataclass
class AccountLevelControl(BaseClass):
    """
    Represents control on the
    cloud provider account level.
    """

    controlName: str = None
    controlId: int = None
    policyNames: BaseList[str] = None
    criticality: str = None
    service: str = None
    result: str = None
    passedResources: int = None
    failedResources: int = None
    passWithExceptionResources: int = None

    def __post_init__(self):
        if getattr(self, "controlId") and not isinstance(
            getattr(self, "controlId"), int
        ):
            setattr(self, "controlId", int(getattr(self, "controlId")))

        if not DONT_EXPAND.flag:
            if self.policyNames:
                data = self.policyNames
                bl = BaseList()
                if isinstance(data, dict):
                    data = [data]
                for name in data:
                    bl.append(name)

    def __int__(self):
        return self.controlId
