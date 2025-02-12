"""
detection.py - contains the Detection and CVEDetection dataclasses for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *
from datetime import datetime
from warnings import catch_warnings, simplefilter

from bs4 import BeautifulSoup

from .qds_factor import QDSFactor
from .qds import QDS as qds
from ...base.base_list import BaseList
from ...base.base_class import BaseClass


def parse_datetime_fields(obj, DATETIME_FIELDS: list[str]) -> None:
    for dt_field in DATETIME_FIELDS:
        if (
            isinstance(getattr(obj, dt_field), str)
            and getattr(obj, dt_field) is not None
        ):
            setattr(obj, dt_field, datetime.fromisoformat(getattr(obj, dt_field)))


def parse_html_fields(obj, HTML_FIELDS: list[str]) -> None:
    with catch_warnings():
        simplefilter("ignore")  # ignore the warning about the html.parser
        for field in HTML_FIELDS:
            if getattr(obj, field, None):
                setattr(
                    obj,
                    field,
                    BeautifulSoup(getattr(obj, field), "html.parser").get_text(),
                )


def parse_int_fields(obj, INT_FIELDS: List[str]) -> None:
    for field in INT_FIELDS:
        if not isinstance(getattr(obj, field), int) and getattr(obj, field) is not None:
            setattr(obj, field, int(getattr(obj, field)))


def parse_bool_fields(obj, BOOL_FIELDS: list[str]) -> None:
    for field in BOOL_FIELDS:
        if (
            not isinstance(getattr(obj, field), bool)
            and getattr(obj, field) is not None
        ):
            setattr(obj, field, bool(getattr(obj, field)))


@dataclass
class BaseDetection(BaseClass):
    """
    Parent dataclass for Detection and CVEDetection
    for shared attributes.
    """

    UNIQUE_VULN_ID: int = field(
        metadata={"description": "The unique ID of the detection."}
    )
    TYPE: Literal["Confirmed", "Potential"] = field(
        metadata={"description": "The type of the detection."},
        default=None,
    )
    SSL: Optional[bool] = field(
        metadata={"description": "The SSL status of the detection."},
        default=False,
        compare=False,
    )
    RESULTS: Optional[str] = field(
        metadata={"description": "The results of the detection."},
        default=None,
    )
    STATUS: Literal["New", "Active", "Fixed", "Re-Opened"] = field(
        metadata={"description": "The status of the detection."},
        default=None,
    )
    PROTOCOL: Optional[str] = field(
        metadata={"description": "The protocol of the detection."},
        default=None,
        compare=False,
    )
    FIRST_FOUND_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was first found."},
        default=None,
        compare=False,
    )
    LAST_FOUND_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last found."},
        default=None,
        compare=False,
    )
    TIMES_FOUND: int = field(
        metadata={"description": "The number of times the detection was found."},
        default=None,
        compare=False,
    )
    LAST_TEST_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last tested."},
        default=None,
        compare=False,
    )
    LAST_UPDATE_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last updated."},
        default=None,
        compare=False,
    )
    PORT: Optional[int] = field(
        metadata={"description": "The port of the detection."},
        default=None,
        compare=False,
    )
    FQDN: Optional[str] = field(
        metadata={"description": "The fully qualified domain name of the detection."},
        default=None,
        compare=False,
    )
    IS_IGNORED: bool = field(
        metadata={"description": "The ignored status of the detection."},
        default=False,
        compare=False,
    )
    IS_DISABLED: bool = field(
        metadata={"description": "The disabled status of the detection."},
        default=False,
        compare=False,
    )
    LAST_PROCESSED_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last processed."},
        default=None,
        compare=False,
    )
    LAST_FIXED_DATETIME: Optional[Union[str, datetime]] = field(
        metadata={"description": "The date and time the detection was last fixed."},
        default=None,
        compare=False,
    )
    ID: int = field(
        metadata={"description": "The host ID of host the detection is on."},
        default=None,
    )

    def __post_init__(self):
        INT_FIELDS = ["UNIQUE_VULN_ID", "TIMES_FOUND", "ID", "PORT"]
        BOOL_FIELDS = ["SSL", "IS_IGNORED", "IS_DISABLED"]
        DATETIME_FIELDS = [
            "FIRST_FOUND_DATETIME",
            "LAST_FOUND_DATETIME",
            "LAST_TEST_DATETIME",
            "LAST_UPDATE_DATETIME",
            "LAST_PROCESSED_DATETIME",
            "LAST_FIXED_DATETIME",
        ]
        HTML_FIELDS = ["RESULTS"]

        # mapping each parser and its fields
        ALL = {
            parse_int_fields: INT_FIELDS,
            parse_bool_fields: BOOL_FIELDS,
            parse_datetime_fields: DATETIME_FIELDS,
            parse_html_fields: HTML_FIELDS,
        }
        # do the parsing
        [parser(self, fields) for parser, fields in ALL.items()]


@dataclass(order=True)
class Detection(BaseDetection):
    """
    Detection - represents a single QID detection on a host.
    """

    QID: int = field(
        metadata={"description": "The QID of the detection."}, default=None
    )
    SEVERITY: int = field(
        metadata={"description": "The severity of the detection."}, default=None
    )
    QDS: Optional[qds] = field(
        metadata={"description": "The Qualys Detection Score (QDS) of the detection."},
        default=None,
        compare=False,
    )

    QDS_FACTORS: Optional[List[QDSFactor]] = field(
        metadata={
            "description": "The Qualys Detection Score (QDS) factors of the detection."
        },
        default=None,
        compare=False,
    )

    def __post_init__(self):
        INT_FIELDS = ["QID"]
        parse_int_fields(self, INT_FIELDS)

        # convert the QDS to a QDS object
        if self.QDS:
            self.QDS = qds(SEVERITY=self.QDS["@severity"], SCORE=int(self.QDS["#text"]))

        # convert the QDS factors to QDSFactor objects
        if self.QDS_FACTORS:
            factors_bl = BaseList()
            data = self.QDS_FACTORS["QDS_FACTOR"]

            # Normalize QDS factors to a list for easier processing
            if isinstance(data, dict):
                data = [data]

            for factor in data:
                factors_bl.append(
                    QDSFactor(NAME=factor["@name"], VALUE=factor["#text"])
                )

            self.QDS_FACTORS = factors_bl

        super().__post_init__()

    def __str__(self):
        # return str(self.UNIQUE_VULN_ID)
        return str(self.QID)

    def __int__(self):
        return self.QID

    # TODO: See where this is used and remove.
    # there are better ways to do this using
    # the base class.
    def copy(self):
        return Detection(
            UNIQUE_VULN_ID=self.UNIQUE_VULN_ID,
            QID=self.QID,
            TYPE=self.TYPE,
            SEVERITY=self.SEVERITY,
            SSL=self.SSL,
            RESULTS=self.RESULTS,
            STATUS=self.STATUS,
            FIRST_FOUND_DATETIME=self.FIRST_FOUND_DATETIME,
            LAST_FOUND_DATETIME=self.LAST_FOUND_DATETIME,
            TIMES_FOUND=self.TIMES_FOUND,
            LAST_TEST_DATETIME=self.LAST_TEST_DATETIME,
            LAST_UPDATE_DATETIME=self.LAST_UPDATE_DATETIME,
            LAST_FIXED_DATETIME=self.LAST_FIXED_DATETIME,
            IS_IGNORED=self.IS_IGNORED,
            IS_DISABLED=self.IS_DISABLED,
            LAST_PROCESSED_DATETIME=self.LAST_PROCESSED_DATETIME,
            QDS=self.QDS,
            QDS_FACTORS=self.QDS_FACTORS,
            PORT=self.PORT,
            PROTOCOL=self.PROTOCOL,
        )

    # See above #TODO
    def valid_values(self):
        # return a list of attribute names that have non-None values
        return {k: v for k, v in self.items() if v is not None and v != "" and v != []}


@dataclass
class CVEDetection(BaseDetection):
    """
    In 2025, Qualys enabled the ability to pull CVEs from the
    HLD API. This class models the data returned from the new
    endpoint.
    """

    VULN_CVE: str = field(
        metadata={"description": "The CVE ID of the detection."},
        default=None,
    )
    ASSOCIATED_QID: int = field(
        metadata={"description": "The QID of the detection."},
        default=None,
    )  # needs converted from string to int
    QID_TITLE: str = field(
        metadata={"description": "The title of the detection."},
        default=None,
    )
    CVSS: float = field(
        metadata={"description": "The CVSS score of the detection."},
        default=None,
    )  # needs converted from string to float
    CVSS_BASE: str = field(
        metadata={"description": "The CVSS base score of the detection."},
        default=None,
    )
    CVSS_TEMPORAL: str = field(
        metadata={"description": "The CVSS temporal score of the detection."},
        default=None,
    )
    CVSS_31: float = field(
        metadata={"description": "The CVSS 3.1 score of the detection."},
        default=None,
    )  # needs converted from string to float
    CVSS_31_BASE: str = field(
        metadata={"description": "The CVSS 3.1 base score of the detection."},
        default=None,
    )
    CVSS_31_TEMPORAL: str = field(
        metadata={"description": "The CVSS 3.1 temporal score of the detection."},
        default=None,
    )
    QVS: int = field(
        metadata={
            "description": "The Qualys Vulnerability Score (QVS) of the detection."
        },
        default=None,
    )

    def __post_init__(self):
        # define extra attrs not in the base class
        INT_FIELDS = ["ASSOCIATED_QID", "QVS"]
        FLOAT_FIELDS = ["CVSS", "CVSS_31"]

        parse_int_fields(self, INT_FIELDS)

        # Could move this to a helper function,
        # but CVE detections are the only thing
        # that have float attributes.
        for field in FLOAT_FIELDS:
            if (
                not isinstance(getattr(self, field), float)
                and getattr(self, field) is not None
            ):
                setattr(self, field, float(getattr(self, field)))

        super().__post_init__()

    def __str__(self):
        return self.VULN_CVE
