"""
Contains AssociatedProduct data class for products under a Qualys
Windows patch.
"""

from dataclasses import dataclass

from ...base.base_class import BaseClass
from ...base.base_list import BaseList


@dataclass
class AssociatedProduct(BaseClass):
    """
    A data class representing a product associated with a Windows patch.

    product: BaseList[str]
        The product name(s) associated with the patch.
    patchId: str
        The UUID of the associated patch.
    """

    product: BaseList[str] = None
    patchId: str = None

    def __str__(self):
        return f"{str(self.product)}"

    def __post_init__(self):
        if self.product:
            setattr(self, "product", BaseList(self.product))
