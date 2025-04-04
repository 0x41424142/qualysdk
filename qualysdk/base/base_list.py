"""
Contains the BaseList class for the qualysdk package.

The BaseList class is used to contain custom class objects in a list.
"""

from json import dumps
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network

IP_TYPES = (IPv4Address, IPv6Address, IPv4Network, IPv6Network)


class BaseList(list):
    """
    BaseList - represents a base list class for the qualysdk package.

    Essentially, this is a regular Python list but with a custom __str__ method for better DB representation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        # instead of returning "[...]", return a comma-separated string of the objects in the list
        return ", ".join(str(obj) for obj in self) if self else "[]"

    def dump_json(self, indent=2) -> str:
        """
        Dumps the list as a JSON string.
        """

        def process_value(value):
            if isinstance(value, datetime):
                return value.isoformat()
            elif isinstance(value, IP_TYPES):
                return str(value)
            elif hasattr(value, "to_dict"):
                return {k: process_value(v) for k, v in value.to_dict().items()}
            elif isinstance(value, (list, BaseList)):
                return [process_value(item) for item in value]
            elif isinstance(value, dict):
                return {k: process_value(v) for k, v in value.items()}
            else:
                return value

        processed_data = [process_value(item) for item in self]
        return dumps(processed_data, indent=indent)

    def to_serializable_list(self):
        """
        Converts the list to a serializable list.
        """
        return [
            item.to_serializable_dict()
            if hasattr(item, "to_serializable_dict")
            else item
            for item in self
        ]
