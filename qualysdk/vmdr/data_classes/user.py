"""
user.py - Contains the User data class.
"""

from typing import Union
from datetime import datetime
from dataclasses import dataclass, field

from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass
class User(BaseClass):
    """
    A user login in Qualys.
    """

    USER_LOGIN: str = field(metadata={"description": "User login name."}, default=None)

    USER_ID: Union[str, int] = field(metadata={"description": "User ID."}, default=None)

    EXTERNAL_ID: str = field(metadata={"description": "External ID."}, default=None)

    CONTACT_INFO: dict = field(
        metadata={"description": "Contact information."}, default=None
    )

    # BELOW ARE PARSED OUT OF CONTACT_INFO

    FIRSTNAME: str = field(metadata={"description": "First name."}, default=None)

    LASTNAME: str = field(metadata={"description": "Last name."}, default=None)

    TITLE: str = field(metadata={"description": "Title."}, default=None)

    PHONE: str = field(metadata={"description": "Phone number."}, default=None)

    FAX: str = field(metadata={"description": "Fax number."}, default=None)

    EMAIL: str = field(metadata={"description": "Email address."}, default=None)

    COMPANY: str = field(metadata={"description": "Company name."}, default=None)

    ADDRESS1: str = field(metadata={"description": "Address line 1."}, default=None)

    ADDRESS2: str = field(metadata={"description": "Address line 2."}, default=None)

    CITY: str = field(metadata={"description": "City."}, default=None)

    COUNTRY: str = field(metadata={"description": "Country."}, default=None)

    STATE: str = field(metadata={"description": "State."}, default=None)

    ZIP_CODE: str = field(metadata={"description": "Zip code."}, default=None)

    TIME_ZONE_CODE: str = field(
        metadata={"description": "Time zone code."}, default=None
    )

    # END PARSED OUT OF CONTACT_INFO

    USER_STATUS: str = field(metadata={"description": "User status."}, default=None)

    CREATION_DATE: Union[str, datetime] = field(
        metadata={"description": "Creation date."}, default=None
    )

    LAST_LOGIN_DATE: Union[str, datetime] = field(
        metadata={"description": "Last login date."}, default=None
    )

    USER_ROLE: str = field(metadata={"description": "User role."}, default=None)

    BUSINESS_UNIT: str = field(metadata={"description": "Business unit."}, default=None)

    UNIT_MANAGER_POC: int = field(
        metadata={"description": "Unit manager point of contact."}, default=None
    )

    MANAGER_POC: int = field(
        metadata={"description": "Manager point of contact."}, default=None
    )

    UI_INTERFACE_STYLE: str = field(
        metadata={"description": "UI interface style."}, default=None
    )

    PERMISSIONS: dict = field(metadata={"description": "Permissions."}, default=None)

    # BELOW ARE PARSED OUT OF PERMISSIONS

    CREATE_OPTION_PROFILES: bool = field(
        metadata={"description": "Create option profiles."}, default=None
    )

    PURGE_INFO: bool = field(
        metadata={"description": "Purge information."}, default=None
    )

    ADD_ASSETS: bool = field(metadata={"description": "Add assets."}, default=None)

    EDIT_REMEDIATION_POLICY: bool = field(
        metadata={"description": "Edit remediation policy."}, default=None
    )

    EDIT_AUTH_RECORDS: bool = field(
        metadata={"description": "Edit authentication records."}, default=None
    )

    # END PARSED OUT OF PERMISSIONS

    NOTIFICATIONS: dict = field(
        metadata={"description": "Notifications."}, default=None
    )

    # BELOW ARE PARSED OUT OF NOTIFICATIONS
    LATEST_VULN: str = field(
        metadata={"description": "Latest vulnerability."}, default=None
    )

    MAP: str = field(metadata={"description": "Map."}, default=None)

    SCAN: str = field(metadata={"description": "Scan."}, default=None)

    DAILY_TICKETS: bool = field(
        metadata={"description": "Daily tickets."}, default=None
    )

    # END PARSED OUT OF NOTIFICATIONS

    ASSIGNED_ASSET_GROUPS: dict = field(
        metadata={"description": "Assigned asset groups."}, default=None
    )

    # BELOW ARE PARSED OUT OF ASSIGNED_ASSET_GROUPS

    ASSET_GROUP_TITLE: BaseList[str] = field(
        metadata={"description": "Asset group title."}, default=None
    )  # May need to be a list in the future?

    # END PARSED OUT OF ASSIGNED_ASSET_GROUPS

    def __post_init__(self):
        DT_FIELDS = ["CREATION_DATE", "LAST_LOGIN_DATE"]
        INT_FIELDS = ["USER_ID", "UNIT_MANAGER_POC", "MANAGER_POC"]
        BOOL_FIELDS = [
            "CREATE_OPTION_PROFILES",
            "PURGE_INFO",
            "ADD_ASSETS",
            "EDIT_REMEDIATION_POLICY",
            "EDIT_AUTH_RECORDS",
            "DAILY_TICKETS",
        ]

        # Parse out the nested fields

        if self.CONTACT_INFO:
            for key, value in self.CONTACT_INFO.items():
                setattr(self, key, value if value else None)

        if self.PERMISSIONS:
            for key, value in self.PERMISSIONS.items():
                setattr(self, key, value if value else None)

        if self.NOTIFICATIONS:
            for key, value in self.NOTIFICATIONS.items():
                setattr(self, key, value if value else None)

        if self.ASSIGNED_ASSET_GROUPS:
            for key, value in self.ASSIGNED_ASSET_GROUPS.items():
                setattr(self, key, value if value else None)

        # Convert the fields to the correct types

        for dt_field in DT_FIELDS:
            if getattr(self, dt_field):
                if getattr(self, dt_field) == "N/A":  # Some fields have N/A as a value
                    setattr(self, dt_field, None)
                else:
                    setattr(
                        self,
                        dt_field,
                        datetime.strptime(
                            getattr(self, dt_field), "%Y-%m-%dT%H:%M:%S%z"
                        ),
                    )

        for int_field in INT_FIELDS:
            if getattr(self, int_field):
                setattr(self, int_field, int(getattr(self, int_field)))

        for bool_field in BOOL_FIELDS:
            if getattr(self, bool_field):
                setattr(self, bool_field, bool(getattr(self, bool_field)))

        if self.ASSET_GROUP_TITLE:
            bl = BaseList()
            data = self.ASSET_GROUP_TITLE
            if not isinstance(data, list):
                data = [data]
            for item in data:
                bl.append(item)
            self.ASSET_GROUP_TITLE = bl

        if self.MAP == "none":
            self.MAP = None

        if self.SCAN == "none":
            self.SCAN = None

    def __str__(self):
        return self.USER_LOGIN

    def valid_values(self):
        return {k: v for k, v in self.__dict__().items() if v}
