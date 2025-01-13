"""
kb_entry.py - contains the KBEntry class for the qualysdk package.

This class is used to represent a single entry in the Qualys KnowledgeBase (KB).
"""

from dataclasses import dataclass, field
from typing import *
from datetime import datetime
from warnings import catch_warnings, simplefilter

from bs4 import BeautifulSoup


from .bugtraq import Bugtraq
from .software import Software
from .vendor_reference import VendorReference
from .cve import CVEID
from .threat_intel import ThreatIntel
from .compliance import Compliance
from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass(order=True)
class KBEntry(BaseClass):
    """
    KBEntry - represents a single entry in the Qualys KnowledgeBase (KB).

    Made with order=True to allow sorting.
    """

    QID: Union[str, int] = field(
        compare=True,
        metadata={"description": "The Qualys ID of the vulnerability."},
        default=None,
    )
    VULN_TYPE: str = field(
        metadata={"description": "The type of vulnerability."}, default="Vulnerability"
    )
    SEVERITY_LEVEL: int = field(
        metadata={"description": "The severity level of the vulnerability."},
        default=None,
    )
    TITLE: str = field(
        metadata={"description": "The title of the vulnerability."}, default=None
    )
    CATEGORY: str = field(
        metadata={"description": "The category of the vulnerability."},
        default=None,
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
    BUGTRAQ_LIST: Optional[BaseList] = field(
        metadata={
            "description": "A list of Bugtraq IDs affected by the vulnerability."
        },
        default=None,
    )
    PATCHABLE: Optional[bool] = field(
        metadata={"description": "Whether the vulnerability is patchable."},
        default=False,
    )
    SOFTWARE_LIST: Optional[BaseList] = field(
        metadata={"description": "A list of software affected by the vulnerability."},
        default=None,
    )
    VENDOR_REFERENCE_LIST: Optional[BaseList] = field(
        metadata={
            "description": "A list of vendor bulletin references for the vulnerability."
        },
        default=None,
    )
    CVE_LIST: Optional[BaseList] = field(
        metadata={"description": "A list of CVEIDs affected by the vulnerability."},
        default=None,
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
    THREAT_INTELLIGENCE: Optional[BaseList] = field(
        metadata={
            "description": "The threat intelligence details of the vulnerability."
        },
        default=None,
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
    COMPLIANCE_LIST: Optional[BaseList] = field(
        metadata={
            "description": "The list of compliance frameworks for the vulnerability."
        },
        default=None,
    )
    LAST_CUSTOMIZATION: Optional[datetime] = field(
        metadata={"description": "The date the vulnerability was last customized."},
        default=None,
    )
    SOLUTION_COMMENT: Optional[str] = field(
        metadata={"description": "The solution comment for the vulnerability."},
        default=None,
    )
    PATCH_PUBLISHED_DATE: Optional[datetime] = field(
        metadata={"description": "The date the patch was published."},
        default=None,
    )

    def __post_init__(self):
        # convert certain fields out of string format:
        if self.QID is not None and not isinstance(self.QID, int):
            self.QID = int(self.QID)

        if self.SEVERITY_LEVEL and not isinstance(self.SEVERITY_LEVEL, int):
            self.SEVERITY_LEVEL = int(self.SEVERITY_LEVEL)

        DATE_FIELDS = [
            "LAST_SERVICE_MODIFICATION_DATETIME",
            "PUBLISHED_DATETIME",
            "CODE_MODIFIED_DATETIME",
            "LAST_CUSTOMIZATION",
            "PATCH_PUBLISHED_DATE",
        ]

        BOOL_FIELDS = ["PATCHABLE", "PCI_FLAG", "IS_DISABLED"]

        HTML_FIELDS = ["DIAGNOSIS", "CONSEQUENCE", "SOLUTION"]

        for dt_field in DATE_FIELDS:
            if getattr(self, dt_field) is not None and not isinstance(
                getattr(self, dt_field), datetime
            ):
                # special case for LAST_CUSTOMIZATION:
                if dt_field == "LAST_CUSTOMIZATION":
                    if isinstance(getattr(self, dt_field), dict):
                        setattr(
                            self,
                            dt_field,
                            datetime.fromisoformat(getattr(self, dt_field)["DATETIME"]),
                        )
                    else:
                        setattr(
                            self,
                            dt_field,
                            datetime.fromisoformat(getattr(self, dt_field)),
                        )
                else:
                    setattr(
                        self, dt_field, datetime.fromisoformat(getattr(self, dt_field))
                    )

        for bool_field in BOOL_FIELDS:
            if getattr(self, bool_field) and not isinstance(
                getattr(self, bool_field), bool
            ):
                setattr(self, bool_field, bool(getattr(self, bool_field)))

        with catch_warnings():
            simplefilter("ignore")  # ignore the warning about the html.parser
            for html_field in HTML_FIELDS:
                if getattr(self, html_field):
                    soup = BeautifulSoup(getattr(self, html_field), "html.parser")
                    for a_tag in soup.find_all("a"):
                        if a_tag.has_attr("href"):
                            a_tag.replace_with(a_tag["href"])
                    setattr(self, html_field, soup.get_text())
                    # setattr(
                    #    self,
                    #    html_field,
                    #    BeautifulSoup(
                    #        getattr(self, html_field), "html.parser"
                    #    ).get_text(),
                    # )

        # convert the lists to BaseList objects:
        if self.BUGTRAQ_LIST:
            final_bugtraq_list = BaseList()
            data = self.BUGTRAQ_LIST["BUGTRAQ"]
            if isinstance(data, dict):
                # Put into a list for easier processing:
                data = [data]

            for bugtraq in data:
                final_bugtraq_list.append(Bugtraq.from_dict(bugtraq))

            self.BUGTRAQ_LIST = final_bugtraq_list

        if self.SOFTWARE_LIST:
            final_software_list = BaseList()
            data = self.SOFTWARE_LIST["SOFTWARE"]
            if isinstance(data, dict):
                # Put into a list for easier processing:
                data = [data]

            for sw in data:
                final_software_list.append(Software.from_dict(sw))

            self.SOFTWARE_LIST = final_software_list

        if self.VENDOR_REFERENCE_LIST:
            final_vendor_reference_list = BaseList()
            data = self.VENDOR_REFERENCE_LIST["VENDOR_REFERENCE"]
            if isinstance(data, dict):
                # Put into a list for easier processing:
                data = [data]

            for vendor_ref in data:
                final_vendor_reference_list.append(
                    VendorReference.from_dict(vendor_ref)
                )

            self.VENDOR_REFERENCE_LIST = final_vendor_reference_list

        if self.CVE_LIST:
            final_cve_list = BaseList()
            data = self.CVE_LIST["CVE"]
            if isinstance(data, dict):
                # Put into a list for easier processing:
                data = [data]

            for cve in data:
                final_cve_list.append(CVEID.from_dict(cve))

            self.CVE_LIST = final_cve_list

        if self.THREAT_INTELLIGENCE:
            final_threat_intel_list = BaseList()
            data = self.THREAT_INTELLIGENCE["THREAT_INTEL"]
            if isinstance(data, dict):
                # Put into a list for easier processing:
                data = [data]

            for threat_intel in data:
                # Ensure @id-> ID and #text-> TEXT
                threat_intel["ID"] = threat_intel.pop("@id")
                threat_intel["TEXT"] = threat_intel.pop("#text")

                final_threat_intel_list.append(ThreatIntel.from_dict(threat_intel))

            self.THREAT_INTELLIGENCE = final_threat_intel_list

        if self.COMPLIANCE_LIST:
            final_compliance_list = BaseList()
            data = self.COMPLIANCE_LIST["COMPLIANCE"]
            if isinstance(data, dict):
                # Put into a list for easier processing:
                data = [data]

            for compliance in data:
                # Ensure TYPE -> _TYPE
                compliance["_TYPE"] = compliance.pop("TYPE")
                final_compliance_list.append(Compliance.from_dict(compliance))

            self.COMPLIANCE_LIST = final_compliance_list

    def __str__(self):
        return f"{self.QID}"

    def __eq__(self, other):
        return self.QID == other.QID

    def __hash__(self):
        return hash(self.QID)

    def __iter__(self):
        for key, value in self.items():
            yield key, value

    def __contains__(self, item):
        return item in self.QID or item in self.TITLE

    def copy(self):
        return KBEntry.from_dict(self.to_dict())

    def is_qid(self, qid: int):
        return self.QID == qid
