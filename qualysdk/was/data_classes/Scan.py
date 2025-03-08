"""
Contains the WASScan class, representing a scan in the Qualys WAS module.
"""

# NOTE: THIS FILE IS TODO. IT NEEDS TO BE COMPLETED AND CHECKED.

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Literal
from datetime import datetime

from ...base.base_list import BaseList
from ...base.base_class import BaseClass


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
    webapps: BaseList = None
    profile: dict = None
    # profile is parsed into below fields:
    profile_id: int = None
    profile_name: str = None
    # end profile
    scanner: dict = None
    # scanner is parsed into below fields:
    scanner_id: int = None
    scanner_name: str = None
    scanner_type: str = None
    # end scanner
    scannerAppliance: dict = None
    # scannerAppliance is parsed into below fields:
    scannerAppliance_id: int = None
    scannerAppliance_name: str = None
    scannerAppliance_type: str = None
    # end scannerAppliance
    status: str = None
    launchedDate: datetime = None
    launchedBy: dict = None
    # launchedBy is parsed into below fields:
    launchedBy_id: int = None
    launchedBy_username: str = None
    launchedBy_firstName: str = None
    launchedBy_lastName: str = None
    # end launchedBy
    duration: int = None
    cancelledDate: datetime = None
    cancelledBy: dict = None
    # cancelledBy is parsed into below fields:
    cancelledBy_id: int = None
    cancelledBy_username: str = None
    cancelledBy_firstName: str = None
    cancelledBy_lastName: str = None
    # end cancelledBy
    progressPercentage: int = None
    resultsStatus: str = None
    authStatus: str = None
    crawlingStatus: str = None
    cancellable: bool = None
    target: dict = None
    # target is parsed into below fields:
    target_webapps: BaseList = None
    # end target
    options: dict = None
    # options is parsed into below fields:
    options_progressiveScanning: bool = None
    options_bruteforceOption: str = None
    options_crawlingScope: str = None
    # end options

    def __post_init__(self):
        """
        Parse nested dictionaries into flat attributes.
        """
        if self.profile:
            self.profile_id = self.profile.get("id")
            self.profile_name = self.profile.get("name")

        if self.scanner:
            self.scanner_id = self.scanner.get("id")
            self.scanner_name = self.scanner.get("name")
            self.scanner_type = self.scanner.get("type")

        if self.scannerAppliance:
            self.scannerAppliance_id = self.scannerAppliance.get("id")
            self.scannerAppliance_name = self.scannerAppliance.get("name")
            self.scannerAppliance_type = self.scannerAppliance.get("type")

        if self.launchedBy:
            self.launchedBy_id = self.launchedBy.get("id")
            self.launchedBy_username = self.launchedBy.get("username")
            self.launchedBy_firstName = self.launchedBy.get("firstName")
            self.launchedBy_lastName = self.launchedBy.get("lastName")

        if self.cancelledBy:
            self.cancelledBy_id = self.cancelledBy.get("id")
            self.cancelledBy_username = self.cancelledBy.get("username")
            self.cancelledBy_firstName = self.cancelledBy.get("firstName")
            self.cancelledBy_lastName = self.cancelledBy.get("lastName")

        if self.target:
            webapps = self.target.get("webapps", {}).get("list", [])
            if webapps:
                self.target_webapps = BaseList()
                for webapp in webapps:
                    self.target_webapps.append(webapp)

        if self.options:
            self.options_progressiveScanning = self.options.get("progressiveScanning")
            self.options_bruteforceOption = self.options.get("bruteforceOption")
            self.options_crawlingScope = self.options.get("crawlingScope")

        # Convert string dates to datetime objects
        if isinstance(self.launchedDate, str):
            try:
                self.launchedDate = datetime.fromisoformat(
                    self.launchedDate.replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                pass

        if isinstance(self.cancelledDate, str):
            try:
                self.cancelledDate = datetime.fromisoformat(
                    self.cancelledDate.replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                pass

    def __str__(self) -> str:
        return self.name

    def __int__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id
