"""
Evaluation data class - contains data on a cloud provider account's standing with a control.
"""

from typing import Literal, Union
from dataclasses import dataclass
from datetime import datetime

from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass
class Evaluation(BaseClass):
    """
    Evaluation statistics for a control on a single resource ID,
    on a single cloud provider account.
    """

    firstEvaluated: Union[str, datetime] = None
    lastEvaluated: Union[str, datetime] = None
    dateReopen: Union[str, datetime] = None
    dateFixed: Union[str, datetime] = None

    def __post_init__(self):
        fields = self.__dataclass_fields__.keys()

        for field in fields:
            value = getattr(self, field)
            if not isinstance(value, datetime):
                try:
                    setattr(self, field, datetime.fromisoformat(value))
                except (OSError, TypeError, ValueError, OverflowError):
                    setattr(self, field, None)

    def __str__(self):
        if self.dateFixed:
            return f"Fixed as of {self.dateFixed}"
        elif self.dateReopen:
            return f"Reopened as of {self.dateReopen}"
        elif self.lastEvaluated:
            return f"Last evaluated on {self.lastEvaluated}"
        elif self.firstEvaluated:
            return f"First evaluated on {self.firstEvaluated}"


@dataclass
class AccountLevelEvaluation(BaseClass):
    """
    Represents the evaluation of a control on a cloud provider account,
    across all resources under that account/control.
    """

    resourceId: str = None
    region: str = None
    accountId: str = None
    evaluatedOn: Union[str, datetime] = None
    evidences: list[dict[str, str]] = None
    resourceType: str = None
    connectorId: str = None
    result: Literal["PASS", "FAIL"] = None
    evaluationDates: Evaluation = None

    def __post_init__(self):
        if getattr(self, "evaluatedOn") and not isinstance(
            getattr(self, "evaluatedOn"), datetime
        ):
            setattr(
                self,
                "evaluatedOn",
                datetime.fromisoformat(getattr(self, "evaluatedOn")),
            )

        if self.evaluationDates:
            data = self.evaluationDates
            setattr(self, "evaluationDates", Evaluation.from_dict(data))

        if self.evidences:
            bl = BaseList()
            for evidence in self.evidences:
                bl.append(evidence)
            setattr(self, "evidences", bl)
