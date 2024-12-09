"""
Contains the user-facing functions for interacting with
the /pm/v*/patches* endpoints
"""

from typing import Union, Literal

from .base.threading_backend import _get_patches_or_assets as get_assets_backend
from .data_classes.PMAsset import Asset
from ..auth.token import TokenAuth
from ..base.call_api import call_api
from ..base.base_list import BaseList
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
