"""
vmscans.py - Contains the VMScan data class.
"""

from typing import Union, Literal
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from .ip_converters import *
from ...base.base_list import BaseList
from ...base.base_class import BaseClass


def parse_duration(duration: str) -> timedelta:
    """
    Parse a duration string into a timedelta object.

    Params:
        duration (str): Duration string in the format HH:MM:SS or N days HH:MM:SS.

    Returns:
        timedelta: Timedelta object representing the duration.
    """
    if "days" in duration:
        days, time = duration.split(" days ")
        days = int(days)
    else:
        days = 0
        time = duration

    try:
        hours, minutes, seconds = map(int, time.split(":"))
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    except ValueError:
        return timedelta(days=days)


@dataclass(order=True)
class VMScan(BaseClass):
    """
    Data class to hold VM Scan data.
    """

    REF: str = field(
        metadata={
            "description": "Scan reference ID. Formatted like scan/1234567890123456, compliance/1234567890123456, or qscap/1234567890123456."
        },
        default=None,
    )
    TYPE: Literal["On-Demand", "API", "Scheduled"] = field(
        metadata={"description": "Type of scan. On-Demand, API, Scheduled."},
        default=None,
    )
    TITLE: str = field(metadata={"description": "Title of the scan."}, default=None)
    USER_LOGIN: str = field(
        metadata={"description": "Owner of the scan."}, default=None
    )
    LAUNCH_DATETIME: Union[str, datetime] = field(
        metadata={"description": "Datetime the scan was launched."}, default=None
    )  # post init to convert to datetime
    DURATION: Union[str, timedelta] = field(
        metadata={"description": "Duration of the scan."}, default=None
    )  # post init to convert to timedelta
    PROCESSING_PRIORITY: str = field(
        metadata={"description": "Processing priority of the scan."}, default=None
    )
    PROCESSED: bool = field(
        metadata={"description": "Whether the scan has been processed."}, default=None
    )
    STATUS: dict = field(
        metadata={"description": "Status of the scan."}, default=None
    )  # STATE is in this dict. get STATE in post init
    STATE: str = field(
        metadata={"description": "The state of the scan."}, init=False, default=None
    )  # populated in post init
    TARGET: Union[str, BaseList[str], BaseList[ip_address]] = field(
        metadata={"description": "Target of the scan."}, default=None
    )
    OPTION_PROFILE: dict = field(
        metadata={"description": "Option profile of the scan."}, default=None
    )
    ASSET_GROUP_TITLE_LIST: Union[str, BaseList[str]] = field(
        metadata={"description": "Asset group title list."}, default=None
    )

    def __post_init__(self):
        """
        Post init function to convert the LAUNCH_DATETIME and DURATION fields to datetime and timedelta objects.
        """
        if self.LAUNCH_DATETIME:
            self.LAUNCH_DATETIME = datetime.strptime(
                self.LAUNCH_DATETIME, "%Y-%m-%dT%H:%M:%SZ"
            )
        if self.DURATION:
            self.DURATION = (
                parse_duration(self.DURATION)
                if self.DURATION not in ["Pending", "Running"]
                else self.DURATION
            )

        if self.STATUS:
            self.STATE = self.STATUS["STATE"]

        # For the IPs/IP ranges in the TARGET field, determine if it is a single IP/range, or a comma separated string of IPs/ranges.
        if self.TARGET:
            final_list = BaseList()
            self.TARGET = self.TARGET.split(",")
            for t in self.TARGET:
                if "-" in t:
                    t = single_range(t)
                else:
                    t = single_ip(t)
                final_list.append(t)
            self.TARGET = final_list

        if self.PROCESSED:
            self.PROCESSED = bool(self.PROCESSED)

        # create the baselist for the asset group titles
        # first, check if [ASSET_GROUP_TITLE_LIST] is a dict. If it is, convert it to a list
        if self.ASSET_GROUP_TITLE_LIST:
            if isinstance(self.ASSET_GROUP_TITLE_LIST, dict):
                self.ASSET_GROUP_TITLE_LIST = [self.ASSET_GROUP_TITLE_LIST]
            # create the BaseList object
            final_list = BaseList()
            for ag in self.ASSET_GROUP_TITLE_LIST:
                final_list.append(ag["ASSET_GROUP_TITLE"])
            self.ASSET_GROUP_TITLE_LIST = final_list

    def __str__(self):
        return f"VMScan: {self.TITLE} - {self.REF}"

    def __int__(self):
        return int(self.REF.split("/")[-1])

    def valid_values(self):
        return {k: v for k, v in self.__dict__().items() if v}
