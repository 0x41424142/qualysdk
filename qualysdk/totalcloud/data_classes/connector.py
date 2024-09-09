"""
connector.py - contains the dataclass for a Qualys Connector Type
"""

from dataclasses import dataclass, asdict
from typing import Optional, Union
from datetime import datetime

from ...base.base_list import BaseList


@dataclass
class Connector:
    """
    Connector - represents a Qualys Connector resource record.
    """

    name: Optional[str] = None
    connectorId: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[str] = None
    state: Optional[str] = None
    totalAssets: Optional[int] = None
    lastSyncedOn: Optional[Union[str, datetime]] = None
    nextSyncedOn: Optional[str] = None
    remediationEnabled: Optional[bool] = None
    qualysTags: Optional[BaseList[str]] = None
    isGovCloud: Optional[bool] = None
    isChinaRegion: Optional[bool] = None
    awsAccountId: Optional[Union[str, int]] = None
    accountAlias: Optional[str] = None
    isDisabled: Optional[bool] = None
    pollingFrequency: Optional[Union[dict, str]] = None
    error: Optional[str] = None
    baseAccountId: Optional[str] = None
    externalId: Optional[str] = None
    arn: Optional[str] = None
    portalConnectorUuid: Optional[str] = None
    isPortalConnector: Optional[bool] = None

    def __post_init__(self):
        """
        __post_init__ - post initialization method for the Connector dataclass
        """
        if self.pollingFrequency:
            s = f"{self.pollingFrequency.get('hours', 0)}h, {self.pollingFrequency.get('minutes', 0)}m"
            setattr(self, "pollingFrequency", s)

        if self.qualysTags:
            bl = BaseList()
            data = self.qualysTags
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(tag["tagName"])
            setattr(self, "qualysTags", bl)

        DT_FIELDS = ["lastSyncedOn", "nextSyncedOn"]

        for field in DT_FIELDS:
            if getattr(self, field):
                if isinstance(getattr(self, field), datetime):
                    continue
                else:
                    setattr(
                        self,
                        field,
                        datetime.strptime(
                            getattr(self, field), "%a %b %d %H:%M:%S %Z %Y"
                        ),
                    )

        INT_FIELDS = ["awsAccountId", "baseAccountId"]
        for field in INT_FIELDS:
            if getattr(self, field):
                setattr(self, field, int(getattr(self, field)))

    def to_dict(self):
        """
        to_dict - returns the Connector object as a dictionary
        """
        return asdict(self)

    def __int__(self):
        return self.connectorId

    def __dict__(self):
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    def __getitem__(self, key):
        return self.to_dict()[key]

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @classmethod
    def from_dict(cls, data):
        """
        from_dict - creates a Connector object from a dictionary
        """
        return cls(**data)
