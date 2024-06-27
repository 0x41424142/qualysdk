"""
detection.py - contains the Detection dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *
from warnings import filterwarnings
from datetime import datetime

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

filterwarnings(
    "ignore", category=MarkupResemblesLocatorWarning, module="bs4"
)  # supress bs4 warnings


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
    SSL: int = field(metadata={"description": "The SSL status of the detection."})
    RESULTS: str = field(
        metadata={"description": "The results of the detection."}
    )
    STATUS: Literal["New", "Active", "Fixed", "Re-Opened"] = field(
        metadata={"description": "The status of the detection."}
    )
    FIRST_FOUND_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was first found."}
    )
    LAST_FOUND_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last found."}
    )
    TIMES_FOUND: int = field(
        metadata={"description": "The number of times the detection was found."}
    )
    LAST_TEST_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last tested."}
    )
    LAST_UPDATE_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last updated."}
    )
    IS_IGNORED: bool = field(
        metadata={"description": "The ignored status of the detection."}
    )
    IS_DISABLED: bool = field(
        metadata={"description": "The disabled status of the detection."}
    )
    LAST_PROCESSED_DATETIME: Union[str, datetime] = field(
        metadata={"description": "The date and time the detection was last processed."}
    )

    def __post_init__(self):
        # convert the datetimes to datetime objects
        DATETIME_FIELDS = [
            "FIRST_FOUND_DATETIME",
            "LAST_FOUND_DATETIME",
            "LAST_TEST_DATETIME",
            "LAST_UPDATE_DATETIME",
            "LAST_PROCESSED_DATETIME",
        ]

        HTML_FIELDS = ["RESULTS"]

        for field in DATETIME_FIELDS:
            if isinstance(getattr(self, field), str):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        # clean up fields that have html tags
        for field in HTML_FIELDS:
            setattr(self, field, BeautifulSoup(getattr(self, field), "html.parser").get_text())


    def __str__(self):
        #return str(self.UNIQUE_VULN_ID)
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
            IS_IGNORED=self.IS_IGNORED,
            IS_DISABLED=self.IS_DISABLED,
            LAST_PROCESSED_DATETIME=self.LAST_PROCESSED_DATETIME,
        )
    
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
