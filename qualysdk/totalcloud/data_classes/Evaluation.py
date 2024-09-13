"""
Evaluation data class - contains data on a cloud provider account's standing with a control.
"""

from typing import Literal, Union
from dataclasses import dataclass, asdict
from datetime import datetime


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
                    pass

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
