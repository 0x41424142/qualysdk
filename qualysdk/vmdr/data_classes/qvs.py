"""
qvs.py - Contains the KBQVS class for ```get_kb_qvs``` function in the VMDR module.
"""

from typing import Union, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass(order=True)
class KBQVS(BaseClass):
    """
    Knowledgebase Qualys Vulnerability Severity (QVS) entry dataclass
    """

    base: Union[dict, None] = field(default=None, compare=False)  # The base entry
    # The following fields are nested under base:
    id: str = field(default=None, compare=False)
    idType: str = field(default=None, compare=False)
    qvs: Union[str, int] = field(default=None)
    qvsLastChangedDate: Union[str, datetime] = field(default=None, compare=False)
    nvdPublishedDate: Union[str, datetime] = field(default=None, compare=False)
    contributingFactors: Union[dict, None] = field(default=None, compare=False)
    # The following fields are nested under contributingFactors:
    cvss: Union[str, float] = field(default=None, init=False, compare=False)
    cvssVersion: str = field(default=None, init=False, compare=False)
    cvssString: str = field(default=None, init=False, compare=False)
    epss: Union[list, float] = field(default=None, init=False, compare=False)
    threatActors: Optional[Union[list[str], BaseList[str]]] = field(
        default=None, compare=False
    )  # List of one long string
    exploitMaturity: Optional[Union[list[str], BaseList[str]]] = field(
        default=None, compare=False
    )  # List of one long string
    trending: Optional[Union[list[str], BaseList[str]]] = field(
        default=None, compare=False
    )  # List of one long string
    mitigationControls: Optional[Union[list[str], BaseList[str]]] = field(
        default=None, compare=False
    )
    malwareName: Optional[Union[list[str], BaseList[str]]] = field(
        default=None, compare=False
    )  # List of one long string
    malwareHash: Optional[Union[list[str], BaseList[str]]] = field(
        default=None, compare=False
    )
    rti: Optional[Union[list[str], BaseList[str]]] = field(default=None, compare=False)

    def __post_init__(self):
        if not self.base:
            raise ValueError("The base attribute is required.")

        DT_FIELDS = ["qvsLastChangedDate", "nvdPublishedDate"]
        for dt_field in DT_FIELDS:
            if dt_field and not isinstance(getattr(self, dt_field), datetime):
                setattr(
                    self, dt_field, datetime.fromtimestamp(int(self.base.get(dt_field)))
                )

        if self.base.get("id"):
            setattr(self, "id", self.base.get("id"))

        if self.base.get("qvs") and not isinstance(self.base.get("qvs"), int):
            setattr(self, "qvs", int(self.base.get("qvs")))

        if self.base.get("idType"):
            setattr(self, "idType", self.base.get("idType"))

        if self.contributingFactors and isinstance(self.contributingFactors, dict):
            if "epss" in self.contributingFactors.keys():
                setattr(self, "epss", float(self.contributingFactors.get("epss")[0]))

            if "cvssVersion" in self.contributingFactors.keys():
                setattr(
                    self, "cvssVersion", self.contributingFactors.get("cvssVersion")
                )

            if "cvssString" in self.contributingFactors.keys():
                setattr(self, "cvssString", self.contributingFactors.get("cvssString"))

            if "cvss" in self.contributingFactors.keys():
                setattr(self, "cvss", float(self.contributingFactors.get("cvss")))

            ONE_LONG_STR_FIELDS = [
                "threatActors",
                "exploitMaturity",
                "trending",
                "malwareName",
            ]
            for str_field in ONE_LONG_STR_FIELDS:
                if str_field in self.contributingFactors.keys():
                    bl = BaseList()
                    for item in self.contributingFactors.get(str_field)[0].split(","):
                        if str_field == "trending":
                            item = int(item)
                        bl.append(item)
                    setattr(self, str_field, bl)

            if "mitigationControls" in self.contributingFactors.keys():
                bl = BaseList()
                for control in self.contributingFactors.get("mitigationControls")[0][
                    0
                ].split(","):
                    bl.append(control)
                setattr(self, "mitigationControls", bl)

            if "malwareHash" in self.contributingFactors.keys():
                bl = BaseList()
                for h in self.contributingFactors.get("malwareHash"):
                    bl.append(h)
                setattr(self, "malwareHash", bl)

            if "rti" in self.contributingFactors.keys():
                bl = BaseList()
                for r in self.contributingFactors.get("rti"):
                    bl.append(r)
                setattr(self, "rti", bl)

        # Set key fields to None
        setattr(self, "contributingFactors", None)
        setattr(self, "base", None)

    def __str__(self):
        return str(self.id)

    def __int__(self):
        return self.qvs

    def epss_category(self):
        """
        Returns a low/medium/high/critical category based on the EPSS value.

        Returns:
            str: The category of the EPSS value.
        """
        if self.epss < 0.15:
            return "Low"
        elif self.epss < 0.4:
            return "Medium"
        elif self.epss < 0.7:
            return "High"
        elif self.epss < 1:
            return "Critical"
        else:
            return "Unknown"
