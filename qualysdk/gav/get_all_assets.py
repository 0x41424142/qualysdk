"""
get_all_assets.py - contains the get_all_assets function for the Global AssetView API (GAV) module.
"""

from typing import Union

from ..base.base_list import BaseList
from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *
from .hosts import Host
from qualysdk.base.logging import ProgressTracker, get_logger

logger = get_logger(__name__)


def get_all_assets(
    auth: TokenAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> BaseList[Host]:
    """
    Get all assets in the Global AssetView API.

    Params:
        auth (TokenAuth): The authentication object.
        page_count (Union[int, "all"]): The number of pages to get. If "all", get all pages. Defaults to "all".

    :Kwargs:
        excludeFields (str): The fields to exclude.
        includeFields (str): The fields to include.
        lastSeenAssetId (int): The last seen asset ID. Used for automatic pagination.
        lastModifiedDate (str): The last modified date.
        pageSize (int): The number of assets to get per page. Max of 300.

    Returns:
        BaseList[Hosts]: The response from the API as a BaseList of Hosts objects.
    """

    responses = BaseList()
    pulled = 0
    completion_reason = "all pages complete"
    progress = ProgressTracker(
        logger=logger,
        operation="get_all_assets",
        item_label="assets collected",
        page_interval=10,
        time_interval=20.0,
    )

    while True:
        # make the request:
        response = call_api(auth=auth, module="gav", endpoint="get_all_assets", params=kwargs)
        j = response.json()

        if "responseCode" not in j.keys() or j["responseCode"] == "FAILED":
            raise QualysAPIError(j["responseMessage"])

        records = j["assetListData"]["asset"]
        for record in records:
            responses.append(Host(**record))
        pulled += 1
        progress.record(items=len(records), pages=1)

        if not j["hasMore"]:
            completion_reason = "no more records"
            break

        if page_count != "all" and pulled >= page_count:
            completion_reason = "page count reached"
            break

        else:
            kwargs["lastSeenAssetId"] = j["lastSeenAssetId"]

    progress.complete(extra=completion_reason)
    return responses
