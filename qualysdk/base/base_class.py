from dataclasses import dataclass, asdict


@dataclass
class BaseClass:
    """
    Base class for all data classes
    to easily define basic common methods.
    """

    def to_dict(self):
        return asdict(self)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
