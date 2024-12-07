"""
Contains the CloudAgentTag data class for the Cloud Agent module.
"""

from dataclasses import dataclass, field

from ...base.base_class import BaseClass


@dataclass
class CloudAgentTag(BaseClass):
    """
    Represents one tag in a Qualys subscription.
    """

    id: int = field(default=None)
    name: str = field(default=None)

    def __post_init__(self):
        if not isinstance(self.id, int):
            self.id = int(self.id)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id
