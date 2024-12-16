"""
Contains the user-facing functions for interacting with
the /pm/v*/patches* endpoints
"""

from typing import Union, Literal

from .data_classes.Patch import Patch
from .base.assets_patches_threading_backend import (
    _get_patches_or_assets as get_assets_backend,
)
from ..auth.token import TokenAuth
from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..exceptions.Exceptions import QualysAPIError


def get_patches(
    auth: TokenAuth,
    platform: Literal["all", "windows", "linux"] = "all",
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList[Patch]:
    """
    Get a list of patches according to the specified kwarg filters.

    By default, returns all patches across both Windows and Linux platforms.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['all', 'windows', 'linux']): The platform to filter by. Default is 'windows'.
        page_count (Union[int, 'all']): The number of pages to retrieve. Default is 'all'.
        **kwargs: Any additional valid parameters.

    ## Kwargs:

        - pageSize (int): The number of patches to return per page. Default is 1000.
        - query (str): A patch QQL query. Default is patchStatus:[Missing,Installed] and isSuperseded:false when platform == 'windows'.
        - havingQuery (str): A PM asset QQL query.
        - attributes (list[str]): A list of attributes to return.

    Returns:
        BaseList[Patch]: A BaseList of Patch objects.
    """

    return get_assets_backend(auth, platform, "PATCH", page_count, **kwargs)


def get_patch_count(
    auth: TokenAuth,
    platform: Literal["windows", "linux"] = "Windows",
    query: str = None,
    havingQuery: str = None,
) -> int:
    """
    Get the number of patches available for the specified platform.


    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal["windows", "linux"]): The platform to filter by. Default is "Windows".
        query (str): A patch QQL query. Default is None.
        havingQuery (str): A PM asset QQL query. Default is None.

    Returns:
        int: The number of patches available for the specified platform.
    """

    platform = platform.title()

    if platform not in ["Windows", "Linux"]:
        raise ValueError("Invalid platform. Must be 'windows' or 'linux'.")

    params = {
        "platform": platform,
    }

    if query:
        params["query"] = query
    if havingQuery:
        params["havingQuery"] = havingQuery

    response = call_api(
        auth=auth,
        module="pm",
        endpoint="get_patch_count",
        params=params,
    )

    if response.status_code not in range(200, 299):
        raise QualysAPIError(response.text)

    patches_value = response.json().get("patches", {})

    return patches_value.get("count", 0) if patches_value else 0
