"""
Evaluation data class - contains data on a cloud provider account's standing with a control.
"""

from typing import Literal, Union
from dataclasses import dataclass, asdict
from datetime import datetime

from ...base.base_list import BaseList


@dataclass
class Evaluation:
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
                except:
                    setattr(self, field, None)

    def to_dict(self):
        return asdict(self)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @staticmethod
    def from_dict(data):
        return Evaluation(**data)


@dataclass
class AccountLevelEvaluation:
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

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - create an AccountLevelEvaluation object from a dictionary
        """
        return cls(**data)
