from dataclasses import dataclass, asdict
from json import dumps
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network

from .base_list import BaseList

IP_TYPES = (IPv4Address, IPv6Address, IPv4Network, IPv6Network)


def _process_value(value):
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, IP_TYPES):
        return str(value)
    # types that need recursive processing:
    elif hasattr(value, "to_dict"):  # Check if it's another dataclass
        return {k: _process_value(v) for k, v in value.to_dict().items()}
    elif isinstance(
        value, (list, BaseList)
    ):  # Handle lists of dataclasses or other types
        return [_process_value(item) for item in value]
    elif isinstance(value, dict):  # Handle dictionaries
        return {k: _process_value(v) for k, v in value.items()}
    else:
        return value


@dataclass
class BaseClass:
    """
    Base class for all data classes
    to easily define basic common methods.
    """

    def to_dict(self):
        return asdict(self)

    def to_serializable_dict(self):
        """
        Converts the dataclass to a serializable dictionary.
        """
        return {key: _process_value(value) for key, value in self.to_dict().items()}

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    def dump_json(self, indent=2):
        """
        Dumps the object as a JSON string, recursively processing dataclass attributes.

        NOTE: for use with `json.dump`, you should use `to_serializable_dict()` instead.
        """
        data = self.to_serializable_dict()
        return dumps(data, indent=indent)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
