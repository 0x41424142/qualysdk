"""
Contains resource dataclasses for Azure, such as SQL, VMs, etc.
"""

from dataclasses import dataclass, asdict
from typing import Union
from datetime import datetime
from json import loads
from urllib.parse import unquote

from ...base.base_list import BaseList
from .QID import QID


@dataclass
class BaseResource:
    """
    Base dataclass for all AWS resources in TotalCloud
    """

    resourceId: str = None
    name: str = None
    connectorUuids: BaseList[str] = None
    created: Union[str, datetime] = None
    subscriptionName: str = None
    subscriptionId: str = None
    uuid: str = None
    connectorUuid: str = None
    tags: BaseList[str] = None
    remediationEnabled: bool = None
    updated: Union[str, datetime] = None
    additionalDetails: dict = None
    cloudType: str = None
    region: str = None
    resourceType: str = None
    controlsFailed: int = None
    qualysTags: BaseList[str] = None
    customerId: str = None
    customers: BaseList[str] = None
    resourceGroupName: str = None
    scanUuid: str = None
    _type: str = None

    def __post_init__(self):
        """
        __post_init__ - post initialization method for the BaseResource dataclass
        """
        DT_FIELDS = ["created", "updated"]
        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if self.additionalDetails:
            setattr(self, "additionalDetails", str(self.additionalDetails))

        if self.connectorUuids:
            data = self.connectorUuids
            bl = BaseList()
            for uuid in data:
                bl.append(uuid)
            setattr(self, "connectorUuids", bl)

        if self.tags:
            data = self.tags
            bl = BaseList()
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(f"{tag.get('value', None)}")
            setattr(self, "tags", bl)

        if self.qualysTags:
            data = self.qualysTags
            bl = BaseList()
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(tag["tagName"])
            setattr(self, "qualysTags", bl)

        if self.remediationEnabled:
            data = self.remediationEnabled
            if not isinstance(data, bool):
                setattr(self, "remediationEnabled", data.lower() == "true")

    def to_dict(self):
        """
        to_dict - return the BaseResource as a dictionary
        """
        return asdict(self)

    def keys(self):
        """
        keys - return the keys of the BaseResource
        """
        return self.to_dict().keys()

    def values(self):
        """
        values - return the values of the BaseResource
        """
        return self.to_dict().values()

    def items(self):
        """
        items - return the items of the BaseResource
        """
        return self.to_dict().items()

    def __dict__(self):
        """
        __dict__ - return the BaseResource as a dictionary
        """
        return self.to_dict()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create a BaseResource object from a dictionary
        """
        return BaseResource(**data)


@dataclass
class AzureVM(BaseResource):
    """
    Represents an Azure VM in TotalCloud
    """

    arsScore: int = None
    vulnerabilityStats: dict = None
    computerName: str = None
    primaryPrivateIPAddress: str = None
    primaryPublicIPAddress: str = None
    primaryPublicIPAddressId: str = None
    statuses: BaseList[str] = None
    criticalityScore: int = None
    availabilitySetId: str = None
    provisioningState: str = None
    licenseType: str = None
    size: str = None
    osType: str = None
    networkSecurityGroupId: str = None
    imageData: BaseList[str] = None
    resourceType: str = "VIRTUAL_MACHINE"

    def __post_init__(self):
        """
        __post_init__ - post initialization method for the AzureVM dataclass
        """
        super().__post_init__()

        if self.vulnerabilityStats:
            data = self.vulnerabilityStats
            setattr(self, "vulnerabilityStats", QID(**data))

        if self.statuses:
            data = self.statuses
            bl = BaseList()
            for status in data:
                bl.append(
                    f"{status.get('code')}:{status.get('level')}:{status.get('displayStatus')}:{status.get('message')}:{status.get('time')}"
                )
            setattr(self, "statuses", bl)

        if self.imageData:
            data = self.imageData
            bl = BaseList()
            for image in data:
                bl.append(
                    f"{image.get('id')}:{image.get('offer')}:{image.get('publisher')}:{image.get('version')} (sku:{image.get('sku')})"
                )
            setattr(self, "imageData", bl)

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AzureVM object from a dictionary
        """
        return AzureVM(**data)


@dataclass
class AzureWebApp(BaseResource):
    """
    Represents an Azure Web App in TotalCloud
    """

    redundancyMode: str = None
    repositorySiteName: str = None
    enabled: bool = None
    enabledHosts: BaseList[str] = None
    clientCertEnabled: bool = None
    subKinds: BaseList[str] = None
    usageState: str = None
    isDefaultContainer: bool = None
    appServicePlan: dict = None
    deploymentId: str = None
    httpsonly: bool = None
    clientAffinityEnabled: bool = None
    state: str = None
    key: str = None
    defaultHostName: str = None
    availabilityState: str = None
    kind: str = None
    resourceType: str = "WEB_APP"

    def __post_init__(self):
        super().__post_init__()

        if self.enabledHosts:
            data = self.enabledHosts
            bl = BaseList()
            for host in data:
                bl.append(host)
            setattr(self, "enabledHosts", bl)

        if self.subKinds:
            data = self.subKinds
            bl = BaseList()
            for kind in data:
                bl.append(kind)
            setattr(self, "subKinds", bl)

    @staticmethod
    def from_dict(data):
        return AzureWebApp(**data)
