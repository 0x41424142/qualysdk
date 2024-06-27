"""
kb_entry.py - contains the KBEntry class for the Qualyspy package.

This class is used to represent a single entry in the Qualys KnowledgeBase (KB).
"""

from dataclasses import dataclass, field
from typing import *
from datetime import datetime
from warnings import filterwarnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

from .lists import *

from .bugtraq import Bugtraq
from .software import Software
from .vendor_reference import VendorReference
from .cve import CVEID
from .threat_intel import ThreatIntel
from .compliance import Compliance
from .tag import Tag, CloudTag

#disable the warning for the bs4 module
filterwarnings("ignore", category=MarkupResemblesLocatorWarning, module="bs4")

def make_lists(data: dict) -> dict:
    """
    make_lists - identify what data is stored so we can create the
    appropriate <>List object.

    Args:
    - data (dict): The data dictionary to identify.

    Returns:
    - data (dict): The data dictionary with the appropriate <>List object created.
    """

    """
    needs_casted and rename_keys are optionally defined, but allow for dynamic casting of values in the list.
    
    these are necessary, as some data is returned as a string, but should be an int for example (needs_casted),
    or the key in the dictionary is different than the key in the object (rename_keys) thanks to xmltodict putting @ and # in front of keys.
    """
    LIST_TYPE_MAPPING = {
        "SOFTWARE_LIST": {
            "class": SoftwareList,
            "key": "SOFTWARE",
            "item_class": Software,
        },
        "CVE_LIST": {"class": CVEList, "key": "CVE", "item_class": CVEID},
        "VENDOR_REFERENCE_LIST": {
            "class": ReferenceList,
            "key": "VENDOR_REFERENCE",
            "item_class": VendorReference,
        },
        "BUGTRAQ_LIST": {
            "class": BugtraqList,
            "key": "BUGTRAQ",
            "item_class": Bugtraq,
            "needs_casted": ("ID", int),
        },
        "THREAT_INTELLIGENCE": {
            "class": ThreatIntelList,
            "key": "THREAT_INTEL",
            "item_class": ThreatIntel,
            "needs_casted": ("@id", int),
            "rename_keys": {"@id": "ID", "#text": "TEXT"},
        },
        "COMPLIANCE_LIST": {
            "class": ComplianceList,
            "key": "COMPLIANCE",
            "item_class": Compliance,
        },
        "TAG": {"class": TagList, "key": "TAG", "item_class": Tag},

        "CLOUD_TAG_LIST": {"class": CloudTagList, "key": "CLOUD_TAG", "item_class": CloudTag},

    }

    for LIST_TYPE in LIST_TYPE_MAPPING.keys():  # iterate through the valid list types
        if LIST_TYPE in data:
            list_info = LIST_TYPE_MAPPING[LIST_TYPE]

            # if there is a single item...
            if isinstance(data[LIST_TYPE][list_info["key"]], dict):
                # check if any of the items in the list need to be casted
                if "needs_casted" in list_info:
                    # holy painful to read... but it works
                    data[LIST_TYPE][list_info["key"]][
                        list_info["needs_casted"][0]
                    ] = list_info["needs_casted"][1](
                        data[LIST_TYPE][list_info["key"]][list_info["needs_casted"][0]]
                    )

                # check if any of the keys need to be renamed according to the mapping
                if "rename_keys" in list_info:
                    for key in list_info["rename_keys"]:
                        data[LIST_TYPE][list_info["key"]][
                            list_info["rename_keys"][key]
                        ] = data[LIST_TYPE][list_info["key"]].pop(key)

                # create the appropriate list object
                data[LIST_TYPE] = list_info["class"](
                    _list=[
                        list_info["item_class"].from_dict(
                            data[LIST_TYPE][list_info["key"]]
                        )
                    ]
                )

            elif isinstance(data[LIST_TYPE][list_info["key"]], list):
                # list (multiple items)
                if "needs_casted" in list_info:
                    for item in data[LIST_TYPE][list_info["key"]]:
                        # item["ID"] = list_info["needs_casted"](item["ID"])
                        item[list_info["needs_casted"][0]] = list_info["needs_casted"][
                            1
                        ](item[list_info["needs_casted"][0]])

                if "rename_keys" in list_info:
                    for item in data[LIST_TYPE][list_info["key"]]:
                        for key in list_info["rename_keys"]:
                            item[list_info["rename_keys"][key]] = item.pop(key)

                data[LIST_TYPE] = list_info["class"](
                    _list=[
                        list_info["item_class"].from_dict(item)
                        for item in data[LIST_TYPE][list_info["key"]]
                    ]
                )

            else:  # if there's nothing in the list, create an empty object:
                data[LIST_TYPE] = list_info["class"]()

    return data

filterwarnings(
    "ignore", category=MarkupResemblesLocatorWarning, module="bs4"
)  # supress bs4 warnings


@dataclass(order=True)
class KBEntry:
    """
    KBEntry - represents a single entry in the Qualys KnowledgeBase (KB).
    """

    QID: Union[str, int] = field(
        compare=True, metadata={"description": "The Qualys ID of the vulnerability."}
    )
    VULN_TYPE: str = field(
        metadata={"description": "The type of vulnerability."}, default="Vulnerability"
    )
    SEVERITY_LEVEL: int = field(
        metadata={"description": "The severity level of the vulnerability."}, default=1
    )
    TITLE: str = field(
        metadata={"description": "The title of the vulnerability."}, default="No Title"
    )
    CATEGORY: str = field(
        metadata={"description": "The category of the vulnerability."},
        default="No Category",
    )
    LAST_SERVICE_MODIFICATION_DATETIME: Optional[datetime] = field(
        metadata={
            "description": "The date the vulnerability was last modified by the service."
        },
        default=None,
    )
    PUBLISHED_DATETIME: Optional[datetime] = field(
        metadata={"description": "The date the vulnerability was published."},
        default=None,
    )
    CODE_MODIFIED_DATETIME: Optional[datetime] = field(
        metadata={"description": "The date the vulnerability code was last modified."},
        default=None,
    )
    BUGTRAQ_LIST: Optional[BugtraqList] = field(
        metadata={
            "description": "A list of Bugtraq IDs affected by the vulnerability."
        },
        default_factory=BugtraqList,
    )
    PATCHABLE: Optional[bool] = field(
        metadata={"description": "Whether the vulnerability is patchable."},
        default=False,
    )
    SOFTWARE_LIST: Optional[SoftwareList] = field(
        metadata={"description": "A list of software affected by the vulnerability."},
        default_factory=SoftwareList,
    )
    VENDOR_REFERENCE_LIST: Optional[ReferenceList] = field(
        metadata={
            "description": "A list of vendor bulletin references for the vulnerability."
        },
        default_factory=ReferenceList,
    )
    CVE_LIST: Optional[CVEList] = field(
        metadata={"description": "A list of CVEIDs affected by the vulnerability."},
        default_factory=CVEList,
    )
    DIAGNOSIS: Optional[str] = field(
        metadata={"description": "The diagnosis of the vulnerability."}, default=""
    )
    CONSEQUENCE: Optional[str] = field(
        metadata={"description": "The consequence of the vulnerability."}, default=None
    )
    SOLUTION: Optional[str] = field(
        metadata={"description": "The solution to the vulnerability."}, default=None
    )
    CORRELATION: Optional[dict] = field(
        metadata={"description": "The correlation details of the vulnerability."},
        default=None,
    )  # TODO... maybe...
    CVSS: Optional[dict] = field(
        metadata={"description": "The CVSS score of the vulnerability."}, default=None
    )
    CVSS_V3: Optional[dict] = field(
        metadata={"description": "The CVSS v3 score of the vulnerability."},
        default=None,
    )
    PCI_FLAG: Optional[bool] = field(
        metadata={"description": "Whether the vulnerability is a PCI flag."},
        default=False,
    )
    PCI_REASONS: Optional[dict] = field(
        metadata={
            "description": "The reasons the vulnerability is valid for PCI requirements."
        },
        default=None,
    )
    THREAT_INTELLIGENCE: Optional[ThreatIntelList] = field(
        metadata={
            "description": "The threat intelligence details of the vulnerability."
        },
        default_factory=ThreatIntelList,
    )
    SUPPORTED_MODULES: Optional[str] = field(
        metadata={"description": "The supported modules for the vulnerability."},
        default=None,
    )
    DISCOVERY: Optional[dict] = field(
        metadata={"description": "The discovery details of the vulnerability."},
        default=None,
    )
    IS_DISABLED: Optional[bool] = field(
        metadata={"description": "Whether the vulnerability is disabled."},
        default=False,
    )
    CHANGE_LOG: Optional[dict] = field(
        metadata={"description": "The change log of the vulnerability."}, default=None
    )
    TECHNOLOGY: Optional[str] = field(
        metadata={"description": "The technology of the vulnerability."},
        default=None,
    )
    COMPLIANCE_LIST: Optional[ComplianceList] = field(
        metadata={
            "description": "The list of compliance frameworks for the vulnerability."
        },
        default_factory=ComplianceList,
    )
    LAST_CUSTOMIZATION: Optional[datetime] = field(
        metadata={"description": "The date the vulnerability was last customized."},
        default=None,
    )
    SOLUTION_COMMENT: Optional[str] = field(
        metadata={"description": "The solution comment for the vulnerability."},
        default=None,
    )

    def __post_init__(self):

        # convert certain fields out of string format:
        if self.QID is not None and not isinstance(self.QID, int):
            self.QID = int(self.QID)

        if self.SEVERITY_LEVEL is not None and not isinstance(self.SEVERITY_LEVEL, int):
            self.SEVERITY_LEVEL = int(self.SEVERITY_LEVEL)

        if self.LAST_SERVICE_MODIFICATION_DATETIME is not None and not isinstance(
            self.LAST_SERVICE_MODIFICATION_DATETIME, datetime
        ):
            self.LAST_SERVICE_MODIFICATION_DATETIME = datetime.fromisoformat(
                self.LAST_SERVICE_MODIFICATION_DATETIME
            )

        if self.PUBLISHED_DATETIME is not None and not isinstance(
            self.PUBLISHED_DATETIME, datetime
        ):
            self.PUBLISHED_DATETIME = datetime.fromisoformat(self.PUBLISHED_DATETIME)

        if self.CODE_MODIFIED_DATETIME is not None and not isinstance(
            self.CODE_MODIFIED_DATETIME, datetime
        ):
            self.CODE_MODIFIED_DATETIME = datetime.fromisoformat(
                self.CODE_MODIFIED_DATETIME
            )

        if self.LAST_CUSTOMIZATION is not None and not isinstance(
            self.LAST_CUSTOMIZATION, datetime
        ):
            if isinstance(self.LAST_CUSTOMIZATION, dict):
                self.LAST_CUSTOMIZATION = datetime.fromisoformat(
                    self.LAST_CUSTOMIZATION["DATETIME"]
                )
            else:
                self.LAST_CUSTOMIZATION = datetime.fromisoformat(
                    self.LAST_CUSTOMIZATION
                )

        if self.PATCHABLE is not None and not isinstance(self.PATCHABLE, bool):
            self.PATCHABLE = bool(self.PATCHABLE)

        if self.PCI_FLAG is not None and not isinstance(self.PCI_FLAG, bool):
            self.PCI_FLAG = bool(self.PCI_FLAG)

        if self.IS_DISABLED is not None and not isinstance(self.IS_DISABLED, bool):
            self.IS_DISABLED = bool(self.IS_DISABLED)

        # parse certain fields that are returned as HTML:
        if self.DIAGNOSIS is not None:
            self.DIAGNOSIS = BeautifulSoup(self.DIAGNOSIS, "html.parser").get_text()

        if self.CONSEQUENCE is not None:
            self.CONSEQUENCE = BeautifulSoup(self.CONSEQUENCE, "html.parser").get_text()

        if self.SOLUTION is not None:
            self.SOLUTION = BeautifulSoup(self.SOLUTION, "html.parser").get_text()

    def __str__(self):
        return f"{self.QID}: {self.TITLE}"

    def __eq__(self, other):
        return self.QID == other.QID

    def __hash__(self):
        return hash(self.QID)

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def __contains__(self, item):
        return item in self.QID or item in self.TITLE

    def copy(self):
        return KBEntry(**self.__dict__)

    def is_qid(self, qid: int):
        return self.QID == qid

    def pop(self, key):
        return self.__dict__.pop(key)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        # return the values
        return self.__dict__.values()

    def extend(self, other):
        return self.__dict__.update(other.__dict__)

    @classmethod
    def from_dict(cls, data: dict):
        """
        from_dict - create a KBEntry object from a dictionary.

        This function is used to create a KBEntry object from a dictionary.
        """
        # make sure that the dictionary has the required keys and nothing else:
        required_keys = {"QID", "VULN_TYPE", "SEVERITY_LEVEL", "TITLE", "CATEGORY"}
        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        # convert the datetime strings to datetime objects:
        for key in [
            "PUBLISHED_DATETIME",
            "CODE_MODIFIED_DATETIME",
            "LAST_SERVICE_MODIFICATION_DATETIME",
        ]:
            if key in data:
                data[key] = datetime.fromisoformat(data[key])

        # call the make_lists function to create the appropriate list objects:
        data = make_lists(data)

        # and finally, create the KBEntry object:
        return cls(**data)
