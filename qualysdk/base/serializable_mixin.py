"""
The SerializableMixin class provides a mixin for serializing objects to JSON format.
"""

from dataclasses import is_dataclass
from datetime import datetime, timedelta
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
from json import dumps

_IP_TYPES = (IPv4Address, IPv6Address, IPv4Network, IPv6Network)
_DT_TYPES = (datetime, timedelta)


def _process_value(value):
    if isinstance(value, _DT_TYPES):
        return value.isoformat() if not isinstance(value, timedelta) else str(value)
    elif isinstance(value, _IP_TYPES):
        return str(value)
    # types that need recursive processing:
    elif hasattr(value, "to_dict"):  # Check if it's another dataclass
        return {k: _process_value(v) for k, v in value.to_dict().items()}
    elif (
        isinstance(
            # hacky way to get around circular import:
            value,
            list,
        )
        or "baselist" in str(value.__class__).lower()
    ):  # Handle lists of dataclasses or other types
        return [_process_value(item) for item in value]
    elif isinstance(value, dict):  # Handle dictionaries
        return {k: _process_value(v) for k, v in value.items()}
    else:
        return value


class SerializableMixin:
    """
    Provides a uniform interface
    for serializing BaseList, list,
    and qualySDK dataclasses to
    JSON format
    """

    def serialized(self) -> dict:
        """
        Return a JSON-serializable dictionary representation of the object.
        This method handles dataclasses, lists/BaseLists, and dictionaries recursively.
        """
        if is_dataclass(self):
            return {key: _process_value(value) for key, value in self.to_dict().items()}
        # hacky way to get around circular import:
        elif isinstance(self, list) or "baselist" in str(self.__class__).lower():
            return [_process_value(item) for item in self]
        elif isinstance(self, dict):
            return {k: _process_value(v) for k, v in self.items()}
        else:
            raise TypeError(
                f"Unsupported type for serialization method: {type(self)}. "
                "Expected dataclass, list/BaseList, or dictionary."
            )

    def dump_json(self, indent: int = 2):
        """
        Dumps the object as a JSON string, recursively processing dataclass attributes.

        Args:
            indent (int): The number of spaces to use for indentation in the JSON output. Defaults to 2.

        Returns:
            str: A JSON string representation of the object.
        """
        return dumps(self.serialized(), indent=indent)
