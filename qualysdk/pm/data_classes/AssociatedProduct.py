"""
Contains AssociatedProduct data class for products under a Qualys
Windows patch.
"""

from dataclasses import dataclass

from ...base.base_class import BaseClass

@dataclass
class AssociatedProduct(BaseClass):
    """
    A data class representing a product associated with a Windows patch.
    
    name: str
        The name of the product.
    patchId: str
        The UUID of the associated patch.
    """

    name: str = None
    patchId: str = None
    
    def __str__(self):
        return f"{self.name}"