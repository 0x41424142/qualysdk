"""
Contains the RemediationActivity dataclass.
"""

from dataclasses import dataclass, asdict
from typing import Union, Literal
from datetime import datetime

from ...base.base_list import BaseList
from ...exceptions.Exceptions import *


@dataclass
class RemediationActivity:
    """
    Represents a remediation activity in TotalCloud.
    """

    resourceId: str = None
    controlId: int = None
    cloudType: Literal["AWS", "AZURE"] = None
    # accountId depends on the cloudType
    accountId: Union[str, int] = None
    region: str = None
    status: str = None
    resourceType: str = None
    remediationAction: str = None
    connectorName: str = None
    policyNames: BaseList[str] = None
    controlName: str = None
    triggeredOn: Union[str, datetime] = None
    Errors: str = None
    triggeredBy: str = None
    remediationReason: str = None

    def __post_init__(self):
        DT_FIELDS = ["triggeredOn"]

        for field in DT_FIELDS:
            if not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if self.cloudType:
            if self.cloudType.upper() == "AWS":
                self.accountId = int(self.accountId)

        if self.Errors:
            setattr(self, "errors", str(self.Errors))

        if self.policyNames:
            bl = BaseList()
            for policy in self.policyNames:
                bl.append(policy)
            setattr(self, "policyNames", bl)

    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary.

        Returns:
            dict: The object as a dictionary.
        """
        return asdict(self)

    def __dict__(self) -> dict:
        return self.to_dict()

    def keys(self) -> list:
        """
        Returns the keys of the object.

        Returns:
            list: The keys of the object.
        """
        return self.to_dict().keys()

    def values(self) -> list:
        """
        Returns the values of the object.

        Returns:
            list: The values of the object.
        """
        return self.to_dict().values()

    def items(self) -> list:
        """
        Returns the items of the object.

        Returns:
            list: The items of the object.
        """
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a RemediationActivity object from a dictionary.

        Args:
            data (dict): The dictionary to create the object from.

        Returns:
            RemediationActivity: The object created from the dictionary.
        """
        return cls(**data)
