from dataclasses import dataclass
from typing import Literal

from ...base.base_class import BaseClass


@dataclass
class ProductVulnCount(BaseClass):
    """
    Represents a product and its associated QID count/details.
    """

    name: str
    totalQIDCount: int = 0
    patchableQIDCount: int = None
    type: str = None
    patchableQIDs: str = None
    totalQIDs: int = None
    severity: Literal["Critical", "Important", "Moderate", "Low", "None"] = "Undefined"
