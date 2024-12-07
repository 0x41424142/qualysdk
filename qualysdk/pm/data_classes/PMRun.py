"""
PMRun class shows high-level information about a
Patch Management run of a job
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime

from ...base.base_class import BaseClass


@dataclass
class PMRun(BaseClass):
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

    def __int__(self):
        return self.jobInstanceId
