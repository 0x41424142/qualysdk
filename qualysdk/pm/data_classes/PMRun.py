"""
PMRun class shows high-level information about a
Patch Management run of a job
"""

from dataclasses import dataclass, asdict
from typing import Union
from datetime import datetime


@dataclass
class PMRun:
    """
    Represents a run of a Patch Management job.
    """

    jobInstanceId: int = None
    jobId: str = None
    scheduledDateTime: Union[str, datetime] = None
    timezoneType: str = None

    def __post_init__(self):
        if self.scheduledDateTime and not isinstance(self.scheduledDateTime, datetime):
            setattr(
                self,
                "scheduledDateTime",
                datetime.fromisoformat(self.scheduledDateTime),
            )

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return asdict(self)

    def __int__(self):
        return asdict(self)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)
