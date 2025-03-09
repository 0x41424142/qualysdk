"""
Contains the user-facing functions for interacting with
the /pm/v*/patches* endpoints
"""

from typing import Union, Literal, overload

from .base.assets_patches_threading_backend import (
    _get_patches_or_assets as get_assets_backend,
)
from .data_classes.PMAsset import Asset
from ..auth.token import TokenAuth
from ..base.base_list import BaseList
from ..base.call_api import call_api
from ..exceptions.Exceptions import QualysAPIError


def get_assets(
    auth: TokenAuth,
    platform: Literal["all", "windows", "linux"] = "all",
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList[Asset]:
    """
    Get a list of assets according to the specified kwarg filters.

    By default, returns all assets across both Windows and Linux platforms.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['all', 'windows', 'linux']): The platform to filter by. Default is 'windows'.
        page_count (Union[int, 'all']): The number of pages to retrieve. Default is 'all'.
        **kwargs: Any additional valid parameters.

    ## Kwargs:

        - pageSize (int): The number of patches to return per page. Default (and max) is 400.
        - query (str): A PM asset QQL query.
        - havingQuery (str): A patch QQL query.
        - attributes (list[str]): A list of attributes to return.

    Returns:
        BaseList[Asset]: A BaseList of Asset objects.
    """

    return get_assets_backend(auth, platform, "ASSET", page_count, **kwargs)


@overload
def lookup_host_uuids(
    auth: TokenAuth,
    assetIds: list[str | int],
) -> BaseList[tuple[str, str]]:
    ...


@overload
def lookup_host_uuids(
    auth: TokenAuth,
    assetIds: BaseList[str | int],
) -> BaseList[tuple[str, str]]:
    ...


@overload
def lookup_host_uuids(
    auth: TokenAuth,
    assetIds: str | int,
) -> tuple[str, str]:
    ...


def lookup_host_uuids(
    auth: TokenAuth, assetIds: Union[str, int, list[str | int], BaseList[str | int]]
) -> BaseList[tuple[str, str]]:
    """
    Look up the Patch Management UUIDs for a given assetId(s)

    Args:
        auth (TokenAuth): The authentication object.
        assetIds (Union[str, int, list[str|int], BaseList[str|int]]): The assetId(s) to look up.

    Returns:
        BaseList[tuple[str, str]]: A BaseList of tuples containing the assetId and the corresponding UUID.
    """

    # If the user passed in a comma-separated string, split it into a list:
    if isinstance(assetIds, str) and "," in assetIds:
        assetIds = assetIds.replace(" ", "").split(",")

    if not isinstance(assetIds, (list, BaseList)):
        assetIds = [assetIds]

    mapped_results = BaseList()

    while True:
        # Base case
        if not assetIds:
            break

        # Call the API with a slice of 1K:
        result = call_api(auth, "pm", "lookup_host_uuids", jsonbody=assetIds[0:1_000])

        if result.status_code != 200:
            raise QualysAPIError(result.text)

        # Remove those 1K assetIds from the list:
        assetIds = assetIds[1_000:]

        j = result.json()

        if j.get("mappedAssets"):
            for asset in j["mappedAssets"]:
                mapped_results.append((asset["assetId"], asset["assetUuid"]))

        if len(j["mappedAssets"]) == 0:
            break

    return mapped_results
