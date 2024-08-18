"""
detection.py - contains the Detection dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field, asdict
from typing import *
from datetime import datetime
from warnings import catch_warnings, simplefilter

from bs4 import BeautifulSoup

from .qds_factor import QDSFactor
from .qds import QDS as qds
from ...base.base_list import BaseList


@dataclass(order=True)
class Detection:
    """
    Detection - represents a single QID detection on a host.
    """

    UNIQUE_VULN_ID: int = field(
        metadata={"description": "The unique ID of the detection."}, compare=False
    )
    QID: int = field(metadata={"description": "The QID of the detection."})
    TYPE: Literal["Confirmed", "Potential"] = field(
        metadata={"description": "The type of the detection."}
    )
    SEVERITY: int = field(metadata={"description": "The severity of the detection."})
    STATUS: Literal["New", "Active", "Fixed", "Re-Opened"] = field(
        metadata={"description": "The status of the detection."}, compare=False
    )
    SSL: Optional[bool] = field(
        metadata={"description": "The SSL status of the detection."},
        default=False,
        compare=False,
    )
    RESULTS: Optional[str] = field(
        metadata={"description": "The results of the detection."},
        default="",
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

    TIMES_FOUND: int = field(
        metadata={"description": "The number of times the detection was found."},
        default=0,
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
    PORT: Optional[int] = field(
        metadata={"description": "The port of the detection."},
        default=None,
        compare=False,
    )
    PROTOCOL: Optional[str] = field(
        metadata={"description": "The protocol of the detection."},
        default=None,
        compare=False,
    )
    FQDN: Optional[str] = field(
        metadata={"description": "The fully qualified domain name of the detection."},
        default=None,
        compare=False,
    )

    ID: int = field(
        metadata={"description": "The host ID of host the detection is on."},
        default=None,
    )

    def __post_init__(self):
        # convert the datetimes to datetime objects
        DATETIME_FIELDS = [
            "FIRST_FOUND_DATETIME",
            "LAST_FOUND_DATETIME",
            "LAST_TEST_DATETIME",
            "LAST_UPDATE_DATETIME",
            "LAST_PROCESSED_DATETIME",
            "LAST_FIXED_DATETIME",
        ]

        HTML_FIELDS = ["RESULTS"]

        BOOL_FIELDS = ["IS_IGNORED", "IS_DISABLED", "SSL"]

        INT_FIELDS = ["UNIQUE_VULN_ID", "QID", "SEVERITY", "TIMES_FOUND", "PORT", "ID"]

        for field in DATETIME_FIELDS:
            if (
                isinstance(getattr(self, field), str)
                and getattr(self, field) is not None
            ):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        # clean up fields that have html tags
        with catch_warnings():
            simplefilter("ignore")  # ignore the warning about the html.parser
            for field in HTML_FIELDS:
                setattr(
                    self,
                    field,
                    BeautifulSoup(getattr(self, field), "html.parser").get_text(),
                )

        # convert the BOOL_FIELDS to bool
        for field in BOOL_FIELDS:
            if (
                not isinstance(getattr(self, field), bool)
                and getattr(self, field) is not None
            ):
                setattr(self, field, bool(getattr(self, field)))

        # convert the INT_FIELDS to int
        for field in INT_FIELDS:
            if (
                not isinstance(getattr(self, field), int)
                and getattr(self, field) is not None
            ):
                setattr(self, field, int(getattr(self, field)))

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

    def __str__(self):
        # return str(self.UNIQUE_VULN_ID)
        return str(self.QID)

    def __int__(self):
        return self.QID

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

    def valid_values(self):
        # return a list of attribute names that have non-None values
        return {k: v for k, v in self.items() if v is not None and v != "" and v != []}

    def to_dict(self):
        """
        to_dict - convert the Detection object to a dictionary.

        This function is used to convert the Detection object to a dictionary.
        """
        return asdict(self)

    def __dict__(self):
        return asdict(self)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: Union[dict, list]):
        """
        from_dict - create a Software object from a dictionary.

        This function is used to create a Software object from a dictionary.
        """
        # make sure that the dictionary has the required keys and nothing else:
        required_keys = {"QID", "SEVERITY", "STATUS", "TYPE"}

        if not required_keys.issubset(data.keys()):
            raise ValueError(
                f"Dictionary must contain the following keys: {required_keys}"
            )

        return cls(**data)
