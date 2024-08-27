"""
Contains the CloudAgentTag data class for the Cloud Agent module.
"""

from dataclasses import dataclass, field, asdict


@dataclass
class CloudAgentTag:
    """
    Represents one tag in a Qualys subscription.
    """

    id: int = field(default=None)
    name: str = field(default=None)

    def __post_init__(self):
        if not isinstance(self.id, int):
            self.id = int(self.id)

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

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id
