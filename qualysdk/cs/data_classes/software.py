"""Contains the csSoftware dataclass"""

from dataclasses import dataclass

from ...base.base_class import BaseClass
from ...exceptions.Exceptions import *


@dataclass
class csSoftware(BaseClass):
    """
    Represents a software object in Qualys Container Security.
    """

    name: str = None
    version: str = None
    scanType: str = None
    packagePath: str = None
    fixVersion: str = None
    vulnerabilities: dict = None
    # vulnerabilities is parsed into below fields:
    vulnerabilities_severity5Count: int = None
    vulnerabilities_severity4Count: int = None
    vulnerabilities_severity3Count: int = None
    vulnerabilities_severity2Count: int = None
    vulnerabilities_severity1Count: int = None
    containerSha: str = None
    # End vulnerabilities fields

    def __post_init__(self):
        # Parse the vulnerabilities field into its components:
        if self.vulnerabilities:
            for key in [
                "vulnerabilities_severity5Count",
                "vulnerabilities_severity4Count",
                "vulnerabilities_severity3Count",
                "vulnerabilities_severity2Count",
                "vulnerabilities_severity1Count",
            ]:
                if key in self.vulnerabilities:
                    setattr(self, key, self.vulnerabilities[key])

            del self.vulnerabilities

    def __str__(self):
        return self.name
