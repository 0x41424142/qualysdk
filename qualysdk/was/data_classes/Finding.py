"""
Contains the WASFinding class, representing a vulnerability on a web application.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Literal
from datetime import datetime
from urllib.parse import unquote_plus
from base64 import b64decode

from ...base.base_list import BaseList


@dataclass
class PayloadRequest:
    """
    Represents a payload request from within a
    WASPayload object.
    """

    method: str = None
    link: str = None
    headers: str = None
    body: str = None

    def __post_init__(self):
        if self.headers:
            self.headers = b64decode(self.headers).decode("utf-8")

        if self.body:
            self.body = b64decode(self.body).decode("utf-8")

    def to_dict(self) -> Dict:
        """
        Returns the PayloadRequest as a dictionary.
        """
        return asdict(self)

    def __str__(self) -> str:
        return f"{self.method}={self.link}"

    def __dict__(self) -> Dict:
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Returns a PayloadRequest object from a dictionary.
        """
        return cls(**data)


@dataclass
class PayloadResponce:
    offset: int = 0
    length: int = 0

    def __post_init__(self):
        if not isinstance(self.offset, int):
            self.offset = int(self.offset)
        if not isinstance(self.length, int):
            self.length = int(self.length)

    def to_dict(self) -> Dict:
        """
        Returns the PayloadResponce as a dictionary.
        """
        return asdict(self)

    def __dict__(self) -> Dict:
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Returns a PayloadResponce object from a dictionary.
        """
        return cls(**data)


@dataclass
class WASPayload:
    """
    Represents a payload from within a
    FindingItem object.
    """

    payload: str = None
    request: PayloadRequest = None
    response: str = None
    payloadResponce: PayloadResponce = None

    def __post_init__(self):
        # if self.headers:
        #    self.headers = b64decode(self.headers).decode("utf-8")

        if self.request:
            self.request = PayloadRequest.from_dict(self.request)

        if self.payloadResponce:
            self.payloadResponce = PayloadResponce.from_dict(self.payloadResponce)

    def to_dict(self) -> Dict:
        """
        Returns the WASPayload as a dictionary.
        """
        return asdict(self)

    def __str__(self) -> str:
        return f"{self.method}={self.link}"

    def __dict__(self) -> Dict:
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Returns a WASPayload object from a dictionary.
        """
        return cls(**data)


@dataclass
class FindingItem:
    """
    Represents a finding from within a
    WASFinding object.
    """

    authentication: bool = False
    accessPath: dict = None
    # accessPath is parsed into below:
    accessPath_count: int = None
    accessPath_list: BaseList[str] = None
    # end of accessPath
    ajax: bool = False
    ajaxRequestId: str = None
    payloads: dict = None
    # payloads is parsed into below:
    payloads_count: int = None
    payloads_list: BaseList[WASPayload] = None
    # end of payloads
    formLocation: str = None

    def __post_init__(self):
        BOOL_FIELDS = ["ajax", "authentication"]

        for field in BOOL_FIELDS:
            if getattr(self, field):
                setattr(self, field, field == "true")

        if self.accessPath:
            self.accessPath_count = int(self.accessPath.get("count"))
            self.accessPath_list = BaseList()
            if self.accessPath_count > 0:
                data = self.accessPath.get("list").get("Url")
                if not isinstance(data, list):
                    data = [data]
                for itm in data:
                    self.accessPath_list.append(itm)
            setattr(self, "accessPath", None)

        if self.payloads:
            self.payloads_count = int(self.payloads.get("count"))
            self.payloads_list = BaseList()
            if self.payloads_count > 0:
                try:
                    data = (
                        self.payloads.get("list").get("PayloadInstance").get("request")
                    )
                    if data:
                        self.payloads_list.append(PayloadRequest.from_dict(data))
                except AttributeError:
                    data = self.payloads.get("list").get("PayloadInstance")
                    if not isinstance(data, list):
                        data = [data]
                    for itm in data:
                        self.payloads_list.append(WASPayload.from_dict(itm))
            setattr(self, "payloads", None)

    def to_dict(self) -> Dict:
        """
        Returns the FindingItem as a dictionary.
        """
        return asdict(self)

    def __dict__(self) -> Dict:
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Returns a FindingItem object from a dictionary.
        """
        return cls(**data)


@dataclass
class ScanData:
    """
    Represents a scan data object from within
    a WASFinding object.
    """

    id: int = None
    reference: str = None
    launchedDate: datetime = None

    def __post_init__(self):
        if self.id:
            setattr(self, "id", int(self.id))
        if self.launchedDate:
            setattr(
                self,
                "launchedDate",
                datetime.strptime(self.launchedDate, "%Y-%m-%dT%H:%M:%SZ"),
            )

    def to_dict(self) -> Dict:
        """
        Returns the ScanData as a dictionary.
        """
        return asdict(self)

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.reference

    def __dict__(self) -> Dict:
        return self.to_dict()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Returns a ScanData object from a dictionary.
        """
        return cls(**data)


@dataclass
class WASCItem:
    """
    Represents a WASC item from within a
    WASFinding object.
    """

    name: str = None
    url: str = None
    code: str = None

    def __dict__(self) -> Dict:
        return self.to_dict()

    def to_dict(self) -> Dict:
        """
        Returns the WASCItem as a dictionary.
        """
        return asdict(self)

    def __str__(self) -> str:
        return self.name

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Returns a WASCItem object from a dictionary.
        """
        return cls(**data)


@dataclass
class WASFinding:
    """
    Represents a vulnerability on
    a web application in WAS.
    """

    id: int = None
    uniqueId: str = None
    qid: int = None
    detectionScore: int = None
    name: str = None
    type: Literal["VULNERABILITY", "SENSITIVE_CONTENT", "INFORMATION_GATHERED"] = None
    potential: bool = None
    findingType: Literal["QUALYS", "CUSTOM"] = None
    severity: Literal[1, 2, 3, 4, 5] = None
    url: str = None
    status: Literal["NEW", "ACTIVE", "REOPENED", "FIXED", "PROTECTED"] = None
    firstDetectedDate: datetime = None
    lastDetectedDate: datetime = None
    lastTestedDate: datetime = None
    fixedDate: datetime = None
    timesDetected: int = None
    webApp: dict = None
    # webApp is parsed into below:
    webApp_id: int = None
    webApp_name: str = None
    webApp_url: str = None
    # end of webApp
    isIgnored: bool = None
    param: str = None
    cwe: dict = None
    # cwe is parsed into below:
    cwe_count: int = None
    cwe_list: BaseList[int] = None
    # end of cwe
    owasp: dict = None
    # owasp is parsed into below:
    owasp_count: int = None
    owasp_list: BaseList[str] = None
    # end of owasp
    resultList: dict = None
    # resultList is parsed into below:
    resultList_count: int = None
    resultList_list: BaseList[str] = None
    # end of resultList
    cvssV3: dict = None
    # cvssV3 is parsed into below:
    cvssV3_base: float = None
    cvssV3_impact: float = None
    cvssV3_attackVector: str = None
    # end of cvssV3
    history: dict = None
    # history is parsed into below:
    history_list: BaseList[ScanData] = None
    # end of history
    wasc: dict = None
    # wasc is parsed into below:
    wasc_count: int = None
    wasc_list: BaseList[WASCItem] = None
    updatedDate: datetime = None

    def __post_init__(self):
        DT_FIELDS = [
            "firstDetectedDate",
            "lastDetectedDate",
            "lastTestedDate",
            "fixedDate",
            "updatedDate",
        ]
        INT_FIELDS = [
            "id",
            "qid",
            "detectionScore",
            "severity",
            "timesDetected",
            "webApp_id",
        ]
        BOOL_FIELDS = ["potential", "isIgnored"]

        if self.webApp:
            self.webApp_id = self.webApp.get("id")
            self.webApp_name = self.webApp.get("name")
            self.webApp_url = self.webApp.get("url")
            setattr(self, "webApp", None)

        if self.status:
            setattr(self, "status", self.status.upper())

        if self.type:
            setattr(self, "type", self.type.upper())

        if self.findingType:
            setattr(self, "findingType", self.findingType.upper())

        if self.param:
            setattr(self, "param", unquote_plus(self.param))

        for field in INT_FIELDS:
            if getattr(self, field):
                setattr(self, field, int(getattr(self, field)))

        for field in BOOL_FIELDS:
            if getattr(self, field):
                setattr(self, field, bool(getattr(self, field)))

        for field in DT_FIELDS:
            if getattr(self, field):
                setattr(
                    self,
                    field,
                    datetime.strptime(getattr(self, field), "%Y-%m-%dT%H:%M:%SZ"),
                )

        if self.cwe:
            setattr(self, "cwe_count", int(self.cwe.get("count")))
            bl = BaseList()
            data = self.cwe.get("list").get("long")
            if data:
                if not isinstance(data, list):
                    data = [data]
                for itm in data:
                    bl.append(int(itm))
            setattr(self, "cwe_list", bl)
            setattr(self, "cwe", None)

        if self.owasp:
            setattr(self, "owasp_count", int(self.owasp.get("count")))
            bl = BaseList()
            data = self.owasp.get("list").get("OWASP")
            if data:
                if not isinstance(data, list):
                    data = [data]
                for itm in data:
                    owaspstr = (
                        f"{itm.get('name')} - {itm.get('url')} - code={itm.get('code')}"
                    )
                    bl.append(owaspstr)
            setattr(self, "owasp_list", bl)
            setattr(self, "owasp", None)

        if self.resultList:
            setattr(self, "resultList_count", int(self.resultList.get("count")))
            bl = BaseList()
            data = self.resultList.get("list").get("Result")
            if data:
                if not isinstance(data, list):
                    data = [data]
                for itm in data:
                    bl.append(FindingItem.from_dict(itm))
            setattr(self, "resultList_list", bl)
            setattr(self, "resultList", None)

        if self.cvssV3:
            self.cvssV3_base = float(self.cvssV3.get("base"))
            self.cvssV3_temporal = float(self.cvssV3.get("temporal"))
            self.cvssV3_attackVector = self.cvssV3.get("attackVector")
            setattr(self, "cvssV3", None)

        if self.history:
            data = self.history["set"]["WebAppFindingHistory"]
            bl = BaseList()
            if data:
                if not isinstance(data, list):
                    data = [data]
                for itm in data:
                    bl.append(ScanData.from_dict(itm["scanData"]))
            setattr(self, "history_list", bl)
            setattr(self, "history", None)

        if self.wasc:
            setattr(self, "wasc_count", int(self.wasc.get("count")))
            bl = BaseList()
            data = self.wasc.get("list").get("WASC")
            if data:
                if not isinstance(data, list):
                    data = [data]
                for itm in data:
                    bl.append(WASCItem.from_dict(itm))
            setattr(self, "wasc_list", bl)
            setattr(self, "wasc", None)

    def to_dict(self) -> Dict:
        """
        Returns the WASFinding as a dictionary.
        """
        return asdict(self)

    def __dict__(self) -> Dict:
        return self.to_dict()

    def __int__(self) -> int:
        return self.id

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    def __getitem__(self, key):
        return self.to_dict().get(key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __eq__(self, other):
        if not isinstance(other, WASFinding):
            return False
        return self.id == other.id

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Returns a WASFinding object from a dictionary.
        """
        return cls(**data)
