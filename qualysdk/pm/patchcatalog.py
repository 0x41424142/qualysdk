"""
Contains user-facing functions for interacting with the /pm/v*/patchcatalog* endpoints
"""

from typing import Union, Literal, overload

from .data_classes.CatalogPatch import CatalogPatch, PackageDetail
from .data_classes.AssociatedProduct import AssociatedProduct
from ..base.base_list import BaseList
from ..auth.token import TokenAuth
from ..base.call_api import call_api
from ..exceptions.Exceptions import QualysAPIError


@overload
def get_patch_catalog(
    auth: TokenAuth,
    patchId: Union[int, str],
    platform: Literal["windows", "linux"] = "windows",
    **kwargs,
) -> BaseList[CatalogPatch]:
    ...


@overload
def get_patch_catalog(
    auth: TokenAuth,
    patchId: Union[BaseList[str, int], list[str, int]],
    platform: Literal["windows", "linux"] = "windows",
    **kwargs,
) -> BaseList[CatalogPatch]:
    ...


def get_patch_catalog(
    auth: TokenAuth,
    patchId: str,
    platform: Literal["windows", "linux"] = "windows",
    **kwargs,
) -> BaseList[CatalogPatch]:
    """
    Retrieve details on patches available for a given platform by patch UUID.

    NOTE: You must call this API with EITHER windows OR linux patch UUID(s), not both.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['windows', 'linux']): The platform to filter by. Default is 'windows'.

    ## Kwargs:

        - attributes (str): A comma-separated string of attributes to return.

    Returns:
        BaseList[CatalogPatch]: A BaseList of CatalogPatch objects.
    """

    platform = platform.title()

    if platform not in ["Windows", "Linux"]:
        raise ValueError("platform must be 'windows' or 'linux'")

    if isinstance(patchId, str) and "," in patchId:
        patchId = patchId.replace(" ", "").split(",")

    if not isinstance(patchId, (list, BaseList)):
        patchId = [patchId]

    params = {
        "platform": platform,
    }

    if "attributes" in kwargs:
        params["attributes"] = kwargs["attributes"]

    results = BaseList()
    pulled = 0

    # Set up chunking
    while True:
        if not patchId:
            # After loop has run its course,
            # list will be empty and we can break
            break

        # call api with a chunk of 1K
        result = call_api(
            auth,
            "pm",
            "get_patch_catalog",
            jsonbody={"patchUuid": patchId[:1000]},
            params=params,
        )

        if result.status_code not in range(200, 299):
            raise QualysAPIError(result.json())

        # Remove processed patchIds from the list:
        patchId = patchId[1000:]

        j = result.json()

        for catalog_entry in j:
            results.append(CatalogPatch(**catalog_entry))

        pulled += 1
        if pulled % 5 == 0:
            print(f"Pulled {pulled} chunks of 1K patch catalog entries")

    return results


def _get_products_or_packages_in_patch():
    """
    Backend function for user-facing get_packages_in_linux_patch 
    and get_products_in_windows_patch functions.
    """
    pass

@overload
def get_packages_in_linux_patch(auth: TokenAuth, patchId: str, page_count: Union[int, 'all'] = 'all', **kwargs) -> BaseList[PackageDetail]:
    ...
    
@overload
def get_packages_in_linux_patch(auth: TokenAuth, patchId: Union[BaseList[str], list[str]], page_count: Union[int, 'all'] = 'all', **kwargs) -> BaseList[PackageDetail]:
    ...

def get_packages_in_linux_patch(auth: TokenAuth, patchId: Union[str, BaseList[str], list[str]], page_count: Union[int, 'all'] = 'all', **kwargs) -> BaseList[PackageDetail]:
    """
    Get a list of packages associated with a Linux patch.
    
    Args:
        auth (TokenAuth): The authentication object.
        patchId (Union[str, BaseList[str], list[str]]): The patch ID(s) to retrieve packages for. If a BaseList/list of patch IDs is provided, the SDK will use threading to speed up the process.
        page_count (int, 'all'): The number of pages to retrieve. Default is 'all'.
        
    ## Kwargs:
        
            - filter (str): A filter to apply to the results. Patch QQL is supported.
            - PageNumber (int): The page number to retrieve. The SDK will automatically handle pagination unless page_count = 1, in which case it will return the page you specify.
            - PageSize (int): The number of results to return per page. Used for pagination (the SDK will automatically handle pagination). Default is 10.
            
    Returns:
        BaseList[PackageDetail]: A list of PackageDetail objects.
    """
    pass
    
@overload
def get_products_in_windows_patch(auth: TokenAuth, patchId: str) -> BaseList[AssociatedProduct]:
    ...
    
@overload
def get_products_in_windows_patch(auth: TokenAuth, patchId: Union[BaseList[str], list[str]]) -> BaseList[AssociatedProduct]:
    ...
    
def get_products_in_windows_patch(auth: TokenAuth, patchId: Union[str, BaseList[str], list[str]]) -> BaseList[AssociatedProduct]:
    """
    Get a list of products associated with a Windows patch.
    
    Args:
        auth (TokenAuth): The authentication object.
        patchId (Union[str, BaseList[str], list[str]]): The patch ID(s) to retrieve products for. If a BaseList/list of patch IDs is provided, the SDK will use threading to speed up the process.
        
    Returns:
        BaseList[PackageDetail]: A list of PackageDetail objects.
    """
    pass