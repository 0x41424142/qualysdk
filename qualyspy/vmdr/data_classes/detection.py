"""
detection.py - contains the Detection dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *
from warnings import filterwarnings
from datetime import datetime

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

from .qds_factor import QDSFactor
from .qds import QDS
from .lists import BaseList

filterwarnings(
    "ignore", category=MarkupResemblesLocatorWarning, module="bs4"
)  # supress bs4 warnings

filterwarnings(
    "ignore", category=UserWarning, module="bs4"
)


@dataclass
class Detection:
    """
    Detection - represents a single QID detection on a host.
    """

    UNIQUE_VULN_ID: int = field(
        metadata={"description": "The unique ID of the detection."}
    )
    QID: int = field(metadata={"description": "The QID of the detection."})
    TYPE: Literal["Confirmed", "Potential"] = field(
        metadata={"description": "The type of the detection."}
    )
    SEVERITY: int = field(metadata={"description": "The severity of the detection."})
    SSL: bool = field(metadata={"description": "The SSL status of the detection."})
    RESULTS: str = field(metadata={"description": "The results of the detection."})
    STATUS: Literal["New", "Active", "Fixed", "Re-Opened"] = field(
        metadata={"description": "The status of the detection."}
    )
    FIRST_FOUND_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was first found."},
        default=None,
    )
    LAST_FOUND_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last found."},
        default=None,
    )

    QDS: Optional[QDS] = field(
        metadata={"description": "The Qualys Detection Score (QDS) of the detection."},
        default=None,
    )

    QDS_FACTORS: Optional[List[QDSFactor]] = field(
        metadata={
            "description": "The Qualys Detection Score (QDS) factors of the detection."
        },
        default=None,
    )

    TIMES_FOUND: int = field(
        metadata={"description": "The number of times the detection was found."},
        default=0,
    )
    LAST_TEST_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last tested."},
        default=None,
    )
    LAST_UPDATE_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last updated."},
        default=None,
    )
    IS_IGNORED: bool = field(
        metadata={"description": "The ignored status of the detection."},
        default=False,
    )
    IS_DISABLED: bool = field(
        metadata={"description": "The disabled status of the detection."},
        default=False,
    )
    LAST_PROCESSED_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last processed."},
        default=None,
    )
    LAST_FIXED_DATETIME: Optional[Union[str, datetime]] = field(
        metadata={"description": "The date and time the detection was last fixed."},
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

        INT_FIELDS = ["UNIQUE_VULN_ID", "QID", "SEVERITY", "TIMES_FOUND"]

        for field in DATETIME_FIELDS:
            if isinstance(getattr(self, field), str):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        # clean up fields that have html tags
        for field in HTML_FIELDS:
            setattr(
                self,
                field,
                BeautifulSoup(getattr(self, field), "html.parser").get_text(),
            )

        # convert the BOOL_FIELDS to bool
        for field in BOOL_FIELDS:
            if not isinstance(getattr(self, field), bool):
                setattr(self, field, bool(getattr(self, field)))

        # convert the INT_FIELDS to int
        for field in INT_FIELDS:
            if not isinstance(getattr(self, field), int):
                setattr(self, field, int(getattr(self, field)))

        # convert the QDS to a QDS object
        if self.QDS:
            self.QDS = QDS(SEVERITY=self.QDS["@severity"], SCORE=int(self.QDS["#text"]))

        # convert the QDS factors to QDSFactor objects
        if self.QDS_FACTORS:
            # if [QDS_FACTORS][QDS_FACTOR] is a list of dictionaries, itereate through each dictionary and convert it to a QDSFactor object
            # if it is just one dictionary, convert it to a QDSFactor object
            if isinstance(self.QDS_FACTORS["QDS_FACTOR"], list):
                self.QDS_FACTORS = [
                    QDSFactor(NAME=factor["@name"], VALUE=factor["#text"])
                    for factor in self.QDS_FACTORS["QDS_FACTOR"]
                ]
            else:
                self.QDS_FACTORS = [
                    QDSFactor(
                        NAME=self.QDS_FACTORS["QDS_FACTOR"]["@name"],
                        VALUE=self.QDS_FACTORS["QDS_FACTOR"]["#text"],
                    )
                ]

    def __str__(self):
        # return str(self.UNIQUE_VULN_ID)
        return str(self.QID)

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
        )

    def valid_values(self):
        # return a list of attribute names that have non-None values
        return [key for key, value in self.to_dict().items() if value is not None]

    def to_dict(self):
        """
        to_dict - convert the Detection object to a dictionary.

        This function is used to convert the Detection object to a dictionary.
        """
        return {
            "UNIQUE_VULN_ID": self.UNIQUE_VULN_ID,
            "QID": self.QID,
            "TYPE": self.TYPE,
            "SEVERITY": self.SEVERITY,
            "SSL": self.SSL,
            "RESULTS": self.RESULTS,
            "STATUS": self.STATUS,
            "FIRST_FOUND_DATETIME": self.FIRST_FOUND_DATETIME,
            "LAST_FOUND_DATETIME": self.LAST_FOUND_DATETIME,
            "TIMES_FOUND": self.TIMES_FOUND,
            "LAST_TEST_DATETIME": self.LAST_TEST_DATETIME,
            "LAST_UPDATE_DATETIME": self.LAST_UPDATE_DATETIME,
            "IS_IGNORED": self.IS_IGNORED,
            "IS_DISABLED": self.IS_DISABLED,
            "LAST_PROCESSED_DATETIME": self.LAST_PROCESSED_DATETIME,
            "LAST_FIXED_DATETIME": self.LAST_FIXED_DATETIME,
            "QDS": self.QDS,
            "QDS_FACTORS": self.QDS_FACTORS,
        }

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
