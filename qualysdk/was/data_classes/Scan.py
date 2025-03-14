"""
Contains the WASScan class, representing a scan in the Qualys WAS module.
"""

from dataclasses import dataclass
from typing import Dict, Union
from datetime import datetime

from ...base.post_init_parser import parse_fields
from ...base.base_class import BaseClass
from ...base.base_list import BaseList


@dataclass
class WASScan(BaseClass):
    """
    Represents a scan in the Qualys WAS module.
    """

    id: int = None
    name: str = None
    reference: str = None
    type: str = None
    mode: str = None
    multi: bool = None
    target: Dict = None
    # target is parsed into below fields:
    target_id: int = None
    target_name: str = None
    # end of target parsing
    launchedDate: Union[datetime, str] = None
    launchedBy: Dict = None
    # launchedBy is parsed into below fields:
    launchedBy_id: int = None
    launchedBy_username: str = None
    launchedBy_firstName: str = None
    launchedBy_lastName: str = None
    # end of launchedBy parsing
    status: str = None
    consolidatedStatus: str = None
    summary: Dict = None
    # summary is parsed into below fields:
    summary_crawlDuration: int = None
    summary_testDuration: int = None
    summary_linksCrawled: int = None
    summary_nbRequests: int = None
    summary_resultsStatus: str = None
    summary_authStatus: str = None
    # end of summary parsing
    cancelMode: str = None
    canceledBy: Dict = None
    # canceledBy is parsed into below fields:
    canceledBy_id: int = None
    canceledBy_username: str = None
    # end of canceledBy parsing
    profile: Dict = None
    # profile is parsed into below fields:
    profile_id: int = None
    profile_name: str = None
    # end of profile parsing
    options: Dict = None
    # options is parsed into below fields:
    options_count: int = None
    options_list: list = None
    # end of options parsing
    scanDuration: int = None
    sendMail: bool = None
    sendOneMail: bool = None
    enableWAFAuth: bool = None
    progressiveScanning: str = None

    def __post_init__(self):
        parse_fields(
            self,
            self.launchedBy,
            "launchedBy",
            ["id", "username", "firstname", "lastname"],
        )
        parse_fields(
            self,
            self.summary,
            "summary",
            [
                "crawlDuration",
                "testDuration",
                "linksCrawled",
                "nbRequests",
                "resultsStatus",
                "authStatus",
            ],
        )
        parse_fields(self, self.canceledBy, "canceledBy", ["id", "username"])
        parse_fields(self, self.profile, "profile", ["id", "name"])
        parse_fields(self, self.target.get("webApp"), "target", ["id", "name"])
        parse_fields(self, self.options, "options", ["count", "list"])
        parse_fields(
            self,
            self.launchedBy,
            "launchedBy",
            ["id", "username", "firstName", "lastName"],
        )

        FIELD_TYPES = {
            "id": int,
            "launchedBy_id": int,
            "canceledBy_id": int,
            "profile_id": int,
            "multi": bool,
            "launchedDate": lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
            if x
            else None,
            "target_id": int,
            "summary_crawlDuration": int,
            "summary_testDuration": int,
            "summary_linksCrawled": int,
            "summary_nbRequests": int,
            "options_count": int,
            "scanDuration": int,
            "sendMail": bool,
            "sendOneMail": bool,
            "enableWAFAuth": bool,
        }

        for field, field_type in FIELD_TYPES.items():
            value = getattr(self, field)
            if value:
                setattr(self, field, field_type(value))

        if self.options_list:
            # raise data:
            options_list = self.options_list
            if isinstance(options_list, dict):
                options_list = options_list.get("WasScanOption")
            bl = BaseList()
            for option in options_list:
                bl.append(f"{option.get('name')}:{option.get('value')}")
            setattr(self, "options_list", bl)

    def __str__(self) -> str:
        return self.name

    def __int__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id
