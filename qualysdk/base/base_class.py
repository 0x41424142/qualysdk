from dataclasses import dataclass, asdict

from .serializable_mixin import SerializableMixin


@dataclass
class BaseClass(SerializableMixin):
    """
    Base class for all data classes
    to easily define basic common methods.
    """

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
