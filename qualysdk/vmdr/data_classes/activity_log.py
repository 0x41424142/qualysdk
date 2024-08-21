"""
activity_log.py - Contains the ActivityLog class, which represents
a single activity log entry.
"""

from dataclasses import dataclass, field, asdict
from typing import Union, Optional
from datetime import datetime
from ipaddress import ip_address, IPv4Address, IPv6Address


@dataclass(order=True)
class ActivityLog:
    """
    Represents a single activity log entry.
    """

    Date: Union[str, datetime] = field(default=None)
    Action: Optional[str] = field(default=None, compare=False)
    Module: Optional[str] = field(default=None, compare=False)
    Details: Optional[str] = field(default=None, compare=False)
    User_Name: Optional[str] = field(default=None, compare=False)
    User_Role: Optional[str] = field(default=None, compare=False)
    User_IP: Optional[Union[str, ip_address]] = field(default=None, compare=False)

    def __post_init__(self):
        if isinstance(self.Date, str):
            self.Date = datetime.fromisoformat(self.Date)

        if self.User_IP and not type(self.User_IP) in [IPv4Address, IPv6Address]:
            try:
                self.User_IP = ip_address(self.User_IP)
            except ValueError:
                if self.User_IP == "N/A":
                    self.User_IP = None
                else:
                    raise ValueError(f"Invalid IP address string: {self.User_IP}")

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return self.to_dict()

    def __str__(self):
        return f"{self.Date} - {self.Action} - {self.Module} - {self.Details} - {self.User_Name} - {self.User_Role} - {self.User_IP}"

    def get_action(self):
        return self.Action

    def get_module(self):
        return self.Module

    def from_dict(data: dict):
        return ActivityLog(**data)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()
