"""
Contains user-facing functions for interacting with the /pm/v*/patchcatalog* endpoints
"""

from typing import Union, Literal, overload

from .data_classes.CatalogPatch import CatalogPatch
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

        if not result.status_code in range(200, 299):
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
