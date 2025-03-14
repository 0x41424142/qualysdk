"""
Contains the WebApp class for WAS
"""

from datetime import datetime
from typing import Union
from dataclasses import dataclass

from .Tag import WASTag
from .AuthRecord import AuthRecord
from .CrawlingScript import CrawlingScript
from .SwaggerFile import SwaggerFile
from .Comment import Comment
from .UrlEntry import UrlEntry
from .PostmanCollection import PostmanCollection
from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass
class WebApp(BaseClass):
    """
    Represents a single Web Application in WAS
    """

    id: int = None
    name: str = None
    url: str = None
    uris: BaseList = None
    riskScore: int = -1
    os: str = None
    owner: None = None
    # owner is parsed into below field:
    owner_id: int = None
    owner_username: str = None
    owner_firstName: str = None
    owner_lastName: str = None
    # end owner
    scope: str = None
    attributes: dict = None
    defaultProfile: None = None
    # defaultProfile is parsed into below field:
    defaultProfile_id: int = None
    defaultProfile_name: str = None
    # end defaultProfile
    defaultScanner: None = None
    # defaultScanner is parsed into below field:
    defaultScanner_id: int = None
    defaultScanner_name: str = None
    # end defaultScanner
    defaultScannerTags: None = None
    # defaultScannerTags is parsed into below field:
    defaultScannerTags_count: int = None
    defaultScannerTags_list: BaseList = None
    # end defaultScannerTags
    scannerLocked: bool = None
    progressiveScanning: bool = None
    urlExcludelist: BaseList = None
    urlAllowlist: BaseList = None
    postDataExcludelist: BaseList = None
    logoutRegexList: BaseList = None
    authRecords: BaseList = None
    dnsOverrides: BaseList = None
    useRobots: str = None
    useSitemap: bool = None
    malwareMonitoring: bool = None
    malwareNotification: bool = None
    tags: Union[list, BaseList] = None
    comments: BaseList = None
    isScheduled: bool = None
    lastScan: None = None
    # lastScan is parsed into below field:
    lastScan_id: int = None
    lastScan_name: str = None
    lastScan_summary_resultsStatus: str = None
    lastScan_summary_authStatus: str = None
    # end lastScan
    createdBy: None = None
    # createdBy is parsed into below field:
    createdBy_id: int = None
    createdBy_username: str = None
    createdBy_firstName: str = None
    createdBy_lastName: str = None
    # end createdBy
    createdDate: Union[str, datetime] = None
    updatedDate: Union[str, datetime] = None
    updatedBy: None = None
    # updatedBy is parsed into below field:
    updatedBy_id: int = None
    updatedBy_username: str = None
    updatedBy_firstName: str = None
    updatedBy_lastName: str = None
    # end updatedBy
    screenshot: str = None
    config: dict = None
    crawlingScripts: BaseList = None
    postmanCollection: BaseList = None
    headers: BaseList = None
    domains: BaseList = None
    subDomain: str = None
    swaggerFile: SwaggerFile = None
    redundancyLinks: BaseList = None
    maxRedundancyLinks: Union[str, int] = None

    def __post_init__(self):
        DT_FIELDS = ["createdDate", "updatedDate"]
        INT_FIELDS = [
            "id",
            "riskScore",
            "owner_id",
            "defaultProfile_id",
            "defaultScannerTags_count",
            "lastScan_id",
            "createdBy_id",
            "updatedBy_id",
            "maxRedundancyLinks",
        ]
        BOOL_FIELDS = [
            "scannerLocked",
            "progressiveScanning",
            "useSitemap",
            "malwareMonitoring",
            "malwareNotification",
            "isScheduled",
        ]

        for field in BOOL_FIELDS:
            value = getattr(self, field)
            if value:
                if isinstance(value, str):
                    if value.lower() == "true":
                        setattr(self, field, True)
                    elif value.lower() == "false":
                        setattr(self, field, False)
                elif not isinstance(value, bool):
                    raise ValueError(f"{field} must be a boolean, not {type(value)}")

        for field in DT_FIELDS:
            value = getattr(self, field)
            if value and not isinstance(value, datetime):
                setattr(self, field, datetime.fromisoformat(value))

        for field in INT_FIELDS:
            value = getattr(self, field)
            if value and not isinstance(value, int):
                setattr(self, field, int(value))

        if self.attributes and "list" in self.attributes.keys():
            bl = BaseList()
            data = self.attributes.get("list").get("Attribute")
            if isinstance(data, dict):
                data = [data]
            for attribute in data:
                bl.append(f"{attribute.get('name')}:{attribute.get('value')}")
            setattr(self, "attributes", bl)

        if self.postmanCollection:
            data = self.postmanCollection.get("collection")
            bl = BaseList()
            if isinstance(data, dict):
                data = [data]
            for collection in data:
                pm = PostmanCollection.from_dict(collection)
                bl.append(pm)
            setattr(self, "postmanCollection", bl)

        if self.headers and "list" in self.headers.keys():
            bl = BaseList()
            data = self.headers.get("list").get("WebAppHeader")
            if isinstance(data, str):
                data = [data]
            for header in data:
                bl.append(header)
            setattr(self, "headers", bl)

        if self.redundancyLinks:
            data = self.redundancyLinks
            bl = BaseList()
            if isinstance(data, str):
                data = data.split()
            for link in data:
                bl.append(link)

        if self.domains and "list" in self.domains.keys():
            bl = BaseList()
            data = self.domains.get("list").get("Domain")
            if isinstance(data, str):
                data = [data]
            for domain in data:
                bl.append(domain)
            setattr(self, "domains", bl)

        if self.owner:
            data = self.owner
            setattr(self, "owner_id", int(data.get("id")))
            setattr(self, "owner_username", data.get("username"))
            setattr(self, "owner_firstName", data.get("firstName"))
            setattr(self, "owner_lastName", data.get("lastName"))
            delattr(self, "owner")

        if self.defaultScanner:
            data = self.defaultScanner
            _id = data.get("id")
            if _id:
                setattr(self, "defaultScanner_id", int(_id))
            else:
                setattr(self, "defaultScanner_id", None)
            setattr(self, "defaultScanner_name", data.get("name"))
            delattr(self, "defaultScanner")

        if self.tags and "list" in self.tags.keys():
            bl = BaseList()
            data = self.tags.get("list").get("Tag")
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(WASTag.from_dict(tag))
            setattr(self, "tags", bl)
        else:
            setattr(self, "tags", None)

        if self.defaultProfile:
            data = self.defaultProfile
            _id = data.get("id")
            if _id:
                setattr(self, "defaultProfile_id", int(_id))
            setattr(self, "defaultProfile_name", data.get("name"))
            delattr(self, "defaultProfile")

        if self.defaultScannerTags and "list" in self.defaultScannerTags.keys():
            bl = BaseList()
            data = self.defaultScannerTags.get("list").get("Tag")
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(WASTag.from_dict(tag))
            setattr(self, "defaultScannerTags", bl)
        else:
            setattr(self, "defaultScannerTags", None)

        if self.urlExcludelist and "list" in self.urlExcludelist.keys():
            bl = BaseList()
            data = self.urlExcludelist.get("list").get("UrlEntry")
            if isinstance(data, dict):
                data = [data]
            for url in data:
                converted = {"regex": url.get("@regex"), "text": url.get("#text")}
                bl.append(UrlEntry.from_dict(converted))
            setattr(self, "urlExcludelist", bl)
        else:
            setattr(self, "urlExcludelist", None)

        if self.urlAllowlist and "list" in self.urlAllowlist.keys():
            bl = BaseList()
            data = self.urlAllowlist.get("list").get("UrlEntry")
            if isinstance(data, dict):
                data = [data]
            for url in data:
                converted = {"regex": url.get("@regex"), "text": url.get("#text")}
                bl.append(UrlEntry.from_dict(converted))
            setattr(self, "urlAllowlist", bl)
        else:
            setattr(self, "urlAllowlist", None)

        if self.postDataExcludelist and "list" in self.postDataExcludelist.keys():
            bl = BaseList()
            data = self.postDataExcludelist.get("list").get("UrlEntry")
            if isinstance(data, dict):
                data = [data]
            for url in data:
                converted = {"regex": url.get("@regex"), "text": url.get("#text")}
                bl.append(UrlEntry.from_dict(converted))
            setattr(self, "urlAllowlist", bl)
        else:
            setattr(self, "postDataExcludelist", None)

        if self.logoutRegexList and "list" in self.logoutRegexList.keys():
            bl = BaseList()
            data = self.logoutRegexList.get("list").get("UrlEntry")
            if isinstance(data, dict):
                data = [data]
            for url in data:
                converted = {"regex": url.get("@regex"), "text": url.get("#text")}
                bl.append(UrlEntry.from_dict(converted))
            setattr(self, "urlAllowlist", bl)
        else:
            setattr(self, "logoutRegexList", None)

        if self.authRecords and "list" in self.authRecords.keys():
            bl = BaseList()
            data = self.authRecords.get("list").get("WebAppAuthRecord")
            if isinstance(data, dict):
                data = [data]
            for authrecord in data:
                bl.append(AuthRecord.from_dict(authrecord))
            setattr(self, "authRecords", bl)

        if self.dnsOverrides and "list" in self.dnsOverrides.keys():
            bl = BaseList()
            data = self.dnsOverrides.get("list").get("DnsOverride")
            if isinstance(data, dict):
                data = [data]
            for dns in data:
                bl.append(WASTag.from_dict(dns))
            setattr(self, "dnsOverrides", bl)
        else:
            setattr(self, "dnsOverrides", None)

        if self.lastScan:
            data = self.lastScan
            _id = data.get("id")
            if _id:
                setattr(self, "lastScan_id", int(_id))
            else:
                setattr(self, "lastScan_id", None)
            setattr(self, "lastScan_name", data.get("name"))
            summary = data.get("summary")
            if summary:
                setattr(
                    self, "lastScan_summary_resultsStatus", summary.get("resultsStatus")
                )
                setattr(self, "lastScan_summary_authStatus", summary.get("authStatus"))
            else:
                setattr(self, "lastScan_summary_resultsStatus", None)
                setattr(self, "lastScan_summary_authStatus", None)
            delattr(self, "lastScan")

        if self.createdBy:
            data = self.createdBy
            _id = data.get("id")
            if _id:
                setattr(self, "createdBy_id", int(_id))
            else:
                setattr(self, "createdBy_id", None)
            setattr(self, "createdBy_username", data.get("username"))
            setattr(self, "createdBy_firstName", data.get("firstName"))
            setattr(self, "createdBy_lastName", data.get("lastName"))
            delattr(self, "createdBy")

        if self.updatedBy:
            data = self.updatedBy
            _id = data.get("id")
            if _id:
                setattr(self, "updatedBy_id", int(_id))
            else:
                setattr(self, "updatedBy_id", None)
            setattr(self, "updatedBy_username", data.get("username"))
            setattr(self, "updatedBy_firstName", data.get("firstName"))
            setattr(self, "updatedBy_lastName", data.get("lastName"))
            delattr(self, "updatedBy")

        if self.comments and "list" in self.comments.keys():
            bl = BaseList()
            data = self.comments.get("list").get("Comment")
            if isinstance(data, dict):
                data = [data]
            for comment in data:
                author_id = comment.get("author").get("id")
                author_username = comment.get("author").get("username")
                comment["author_id"] = author_id
                comment["author_username"] = author_username
                comment.pop("author")
                bl.append(Comment.from_dict(comment))
            setattr(self, "comments", bl)
        else:
            setattr(self, "comments", None)

        if self.crawlingScripts and "list" in self.crawlingScripts.keys():
            bl = BaseList()
            data = self.crawlingScripts.get("list").get("SeleniumScript")
            if isinstance(data, dict):
                data = [data]
            for script in data:
                bl.append(CrawlingScript.from_dict(script))
            setattr(self, "crawlingScripts", bl)
        else:
            setattr(self, "crawlingScripts", None)

        if self.uris and "list" in self.uris.keys():
            bl = BaseList()
            data = self.uris.get("list")
            if isinstance(data, dict) and not isinstance(data.get("Url"), list):
                data = [data]
                for uri in data:
                    bl.append(uri.get("Url"))
            else:
                data = data.get("Url")
                for uri in data:
                    bl.append(uri)
            setattr(self, "uris", bl)

        if self.swaggerFile:
            data = self.swaggerFile
            setattr(self, "swaggerFile", SwaggerFile.from_dict(data))

    def risk_rating(self) -> str:
        """
        Categorized risk rating based on riskScore.
        0-250: Low
        251-500: Medium
        501-750: High
        751-1000: Critical

        Returns:
            str: The risk rating.
        """

        if type(self.riskScore) not in [int, float]:
            raise ValueError(
                f"riskScore must be an integer or float, not {type(self.riskScore)}"
            )

        if self.riskScore < 251:
            return "Low"
        elif self.riskScore < 501:
            return "Medium"
        elif self.riskScore < 751:
            return "High"
        elif self.riskScore > 750:
            return "Critical"
        # Not needed, but added for clarity:
        else:
            return "Unknown"

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id
