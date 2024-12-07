"""
Certificate data class
"""

from dataclasses import dataclass, asdict
from typing import Union, Literal
from datetime import datetime

from ...base.base_class import BaseClass
from .Asset import Asset
from ...base.base_list import BaseList


@dataclass
class Certificate(BaseClass):
    """
    Represents a certificate in CERT.
    """

    id: int = None
    certhash: str = None
    keySize: int = None
    serialNumber: str = None
    validToDate: Union[str, datetime] = None
    validTo: Union[int, datetime] = None
    validFromDate: Union[str, datetime] = None
    validFrom: Union[int, datetime] = None
    signatureAlgorithm: str = None
    extendedValidation: bool = None
    createdDate: Union[str, datetime] = None
    dn: str = None
    subject: dict = None
    # subject is parsed into below fields:
    subject_organization: str = None
    subject_locality: str = None
    subject_name: str = None
    subject_country: str = None
    subject_organizationUnit: BaseList[str] = None
    # end of subject fields
    updateDate: Union[str, datetime] = None
    lastFound: Union[int, datetime] = None
    imported: bool = None
    selfSigned: bool = None
    issuer: dict = None
    # issuer is parsed into below fields:
    issuer_organization: str = None
    issuer_organizationUnit: BaseList[str] = None
    issuer_name: str = None
    issuer_country: str = None
    issuer_state: str = None
    issuer_certhash: str = None
    issuer_locality: str = None
    # end of issuer fields
    issuerCategory: str = None
    instanceCount: int = None
    assetCount: int = None
    sources: Union[list[str], BaseList[str]] = None
    assets: Union[list[dict], BaseList[object]] = None
    type: Literal["Leaf", "Intermediate", "Root"] = None
    rootissuer: dict = None
    # rootissuer is parsed into below fields:
    rootissuer_organization: str = None
    rootissuer_organizationUnit: BaseList[str] = None
    rootissuer_name: str = None
    rootissuer_country: str = None
    rootissuer_state: str = None
    rootissuer_certhash: str = None
    rootissuer_locality: str = None
    # end of rootissuer fields

    def __post_init__(self):
        INT_TO_DT_FIELDS = ["validTo", "validFrom", "lastFound"]
        STR_TO_DT_FIELDS = ["validToDate", "validFromDate", "createdDate", "updateDate"]
        DT_FIELDS = INT_TO_DT_FIELDS + STR_TO_DT_FIELDS

        for field in DT_FIELDS:
            if getattr(self, field):
                if field in INT_TO_DT_FIELDS and not isinstance(
                    getattr(self, field), datetime
                ):
                    setattr(
                        self, field, datetime.fromtimestamp(getattr(self, field) / 1000)
                    )
                elif field in STR_TO_DT_FIELDS and not isinstance(
                    getattr(self, field), datetime
                ):
                    setattr(self, field, datetime.fromisoformat(getattr(self, field)))
                else:
                    raise ValueError(f"Field {field} is not a valid datetime field.")

        if self.subject:
            setattr(self, "subject_organization", self.subject.get("organization"))
            setattr(self, "subject_locality", self.subject.get("locality"))
            setattr(self, "subject_name", self.subject.get("name"))
            setattr(self, "subject_country", self.subject.get("country"))
            setattr(
                self,
                "subject_organizationUnit",
                BaseList(self.subject.get("organizationUnit", [])),
            )
            setattr(self, "subject", None)

        if self.issuer:
            setattr(self, "issuer_organization", self.issuer.get("organization"))
            setattr(
                self,
                "issuer_organizationUnit",
                BaseList(self.issuer.get("organizationUnit", [])),
            )
            setattr(self, "issuer_name", self.issuer.get("name"))
            setattr(self, "issuer_country", self.issuer.get("country"))
            setattr(self, "issuer_state", self.issuer.get("state"))
            setattr(self, "issuer_certhash", self.issuer.get("certhash"))
            setattr(self, "issuer_locality", self.issuer.get("locality"))
            setattr(self, "issuer", None)

        if self.rootissuer:
            setattr(
                self, "rootissuer_organization", self.rootissuer.get("organization")
            )
            setattr(
                self,
                "rootissuer_organizationUnit",
                BaseList(self.rootissuer.get("organizationUnit", [])),
            )
            setattr(self, "rootissuer_name", self.rootissuer.get("name"))
            setattr(self, "rootissuer_country", self.rootissuer.get("country"))
            setattr(self, "rootissuer_state", self.rootissuer.get("state"))
            setattr(self, "rootissuer_certhash", self.rootissuer.get("certhash"))
            setattr(self, "rootissuer_locality", self.rootissuer.get("locality"))
            setattr(self, "rootissuer", None)

        if self.sources:
            setattr(self, "sources", BaseList(self.sources))

        if self.assets:
            setattr(self, "assets", BaseList([Asset(**x) for x in self.assets]))
