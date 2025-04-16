"""
Contains the BaseList class for the qualysdk package.

The BaseList class is used to contain custom class objects in a list.
"""

from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network

from .serializable_mixin import SerializableMixin

IP_TYPES = (IPv4Address, IPv6Address, IPv4Network, IPv6Network)


class BaseList(list, SerializableMixin):
    """
    BaseList - represents a base list class for the qualysdk package.

    Essentially, this is a regular Python list but with a custom __str__ method for better DB representation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        # instead of returning "[...]", return a comma-separated string of the objects in the list
        return ", ".join(str(obj) for obj in self) if self else "[]"
