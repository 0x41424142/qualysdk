"""
Contains the WASFinding class, representing a vulnerability on a web application.
"""

from dataclasses import dataclass, field
from typing import Dict, Literal
from datetime import datetime
from urllib.parse import unquote_plus
from base64 import b64decode

from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass
class PayloadRequest(BaseClass):
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
            try:
                self.headers = b64decode(self.headers).decode("utf-8")
            except UnicodeDecodeError:
                self.headers = self.headers

        if self.body:
            try:
                self.body = b64decode(self.body).decode("utf-8")
            except UnicodeDecodeError:
                self.body = self.body

    def __str__(self) -> str:
        return f"{self.method}={self.link}"


@dataclass
class PayloadResponce(BaseClass):
    offset: int = 0
    length: int = 0

    def __post_init__(self):
        if not isinstance(self.offset, int):
            self.offset = int(self.offset)
        if not isinstance(self.length, int):
            self.length = int(self.length)


@dataclass
class WASPayload(BaseClass):
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

    def __str__(self) -> str:
        return f"{self.payload}"


@dataclass
class FindingItem(BaseClass):
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

        for bool_field in BOOL_FIELDS:
            if getattr(self, bool_field):
                setattr(self, bool_field, bool_field == "true")

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


@dataclass
class ScanData(BaseClass):
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

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.reference


@dataclass
class WASCItem(BaseClass):
    """
    Represents a WASC item from within a
    WASFinding object.
    """

    name: str = None
    url: str = None
    code: str = None

    def __dict__(self) -> Dict:
        return self.to_dict()

    def __str__(self) -> str:
        return self.name


@dataclass
class WASFinding(BaseClass):
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
    group: str = None
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
    ignoredReason: str = None
    ignoredBy: str = None
    ignoredDate: datetime = None
    ignoredComment: str = None
    reactivateDate: datetime = None
    reactivateIn: int = None
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
    resultList_count: int = 0
    resultList_list: BaseList[str] = None
    patch: int = None
    # accessPath_count/list is an aggregate of each
    # object in resultList_list. As is
    # payloads_count/list
    accessPath_count: int = 0
    accessPath_list: BaseList[str] = field(default_factory=BaseList)
    payloads_count: int = 0
    payloads_list: BaseList[WASPayload] = field(default_factory=BaseList)
    # end of resultList
    cvssV3: dict = None
    # cvssV3 is parsed into below:
    cvssV3_base: float = None
    cvssV3_impact: float = None
    cvssV3_attackVector: str = None
    severityComment: str = None
    editedSeverityUser: str = None
    # end of cvssV3
    history: dict = None
    # history is parsed into below:
    history_list: BaseList[ScanData] = None
    # end of history
    wasc: dict = None
    # wasc is parsed into below:
    wasc_count: int = None
    wasc_list: BaseList[WASCItem] = None
    sslData: dict = None
    # sslData is parsed into below:
    sslData_protocol: str = None
    sslData_virtualhost: str = None
    sslData_ip: str = None
    sslData_port: int = None
    sslData_result: str = None
    sslData_list: BaseList[str] = None
    sslData_certificateFingerprint: BaseList[str] = None
    sslData_flags: str = None
    updatedDate: datetime = None
    retest: dict = None
    # retest is parsed into below:
    retestStatus: str = None
    retestedDate: datetime = None
    retestedUser_id: int = None
    retestedUser_username: str = None
    retestedUser_firstName: str = None
    retestedUser_lastName: str = None
    retestFindingStatus: str = None
    retestReason: str = None
    # end of retest

    def __post_init__(self):
        DT_FIELDS = [
            "firstDetectedDate",
            "lastDetectedDate",
            "lastTestedDate",
            "fixedDate",
            "updatedDate",
            "ignoredDate",
            "reactivateDate",
        ]
        INT_FIELDS = [
            "id",
            "qid",
            "detectionScore",
            "severity",
            "timesDetected",
            "webApp_id",
            "patch",
            "reactivateIn",
            "retestedUser_id",
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

        if self.ignoredBy:
            setattr(self, "ignoredBy", self.ignoredBy.get("id"))

        if self.editedSeverityUser:
            setattr(self, "editedSeverityUser", self.editedSeverityUser.get("id"))

        if self.findingType:
            setattr(self, "findingType", self.findingType.upper())

        if self.param:
            setattr(self, "param", unquote_plus(self.param))

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

            if bl:
                # Parse out accessPath_count/list, payloads_count/list
                for itm in bl:
                    if itm.accessPath_list:
                        self.accessPath_count += itm.accessPath_count
                        self.accessPath_list += itm.accessPath_list
                    if itm.payloads_list:
                        self.payloads_count += itm.payloads_count
                        self.payloads_list += itm.payloads_list

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

        if self.sslData:
            self.sslData_certificateFingerprint = BaseList()
            self.sslData_protocol = self.sslData.get("protocol")
            self.sslData_virtualhost = self.sslData.get("virtualhost")
            self.sslData_ip = self.sslData.get("ip")
            self.sslData_flags = self.sslData.get("flags")
            try:
                self.sslData_port = int(self.sslData.get("port"))
            except TypeError:
                self.sslData_port = None

            self.sslData_result = self.sslData.get("result")
            data = self.sslData.get("sslDataInfoList")
            if data:
                data = data["list"].get("SSLDataInfo")
                bl = BaseList()
                if not isinstance(data, list):
                    data = [data]
                for datapoint in data:
                    for itm, val in datapoint.items():
                        match itm:
                            case "sslDataCipherList":
                                if val:
                                    for cipher in val.get("list").get("SSLDataCipher"):
                                        # protocol, name, keyExchange, auth, mac, encryption, grade
                                        string = f"{cipher.get('protocol')}: {cipher.get('name')} (keyExchange: {cipher.get('keyExchange')}; auth: {cipher.get('auth')}; mac: {cipher.get('mac')}; encryption: {cipher.get('encryption')}; grade: {cipher.get('grade')})"
                                        bl.append(string) if string not in bl else None
                            case "sslDataKexList":
                                if val:
                                    for kex in val.get("list").get("SSLDataKex"):
                                        string = f"{kex.get('protocol')}: {kex.get('kex')} (keysize: {kex.get('keysize')}; fwdsec: {kex.get('fwdsec')}; classical: {kex.get('classical')}; quantum: {kex.get('quantum')})"
                                        bl.append(string) if string not in bl else None
                            case "sslDataPropList":
                                if val:
                                    for prop in val.get("list").get("SSLDataProp"):
                                        string = f"{prop.get('name')}: {prop.get('value')} ({prop.get('protocol')})"
                                        bl.append(string) if string not in bl else None
                            case "certificateFingerprint":
                                self.sslData_certificateFingerprint.append(val)

                self.sslData_list = bl
            setattr(self, "sslData", None)

        if self.retest:
            setattr(self, "retestStatus", self.retest.get("retestStatus"))
            date = self.retest.get("retestedDate")
            if date:
                setattr(self, "retestedDate", datetime.fromisoformat(date))
            user = self.retest.get("retestedUser")
            if user:
                setattr(self, "retestedUser_id", user.get("id"))
                setattr(self, "retestedUser_username", user.get("username"))
                setattr(self, "retestedUser_firstName", user.get("firstName"))
                setattr(self, "retestedUser_lastName", user.get("lastName"))
            setattr(self, "retestFindingStatus", self.retest.get("findingStatus"))
            setattr(self, "retestReason", self.retest.get("reason"))

        for int_field in INT_FIELDS:
            if getattr(self, int_field):
                setattr(self, int_field, int(getattr(self, int_field)))

        for bool_field in BOOL_FIELDS:
            if getattr(self, bool_field):
                setattr(self, bool_field, bool(getattr(self, bool_field)))

        for dt_field in DT_FIELDS:
            if getattr(self, dt_field):
                setattr(
                    self,
                    dt_field,
                    datetime.strptime(getattr(self, dt_field), "%Y-%m-%dT%H:%M:%SZ"),
                )

    def __int__(self) -> int:
        return self.id

    def __getitem__(self, key):
        return self.to_dict().get(key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __eq__(self, other):
        if not isinstance(other, WASFinding):
            return False
        return self.id == other.id
