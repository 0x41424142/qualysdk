"""
query_assets.py - contains the query_assets function for the Global AssetView API (GAV) module.

Gets all assets that satisfy a Qualys Query Language (QQL) filter.
"""

from typing import Union

from ..base.base_list import BaseList
from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *
from .hosts import Host
from qualysdk.base.logging import ProgressTracker, get_logger

logger = get_logger(__name__)


def query_assets(
    auth: TokenAuth, page_count: Union["all", int] = "all", **kwargs
) -> BaseList[Host]:
    """
    Queries GAV inventory for assets that satisfy a Qualys Query Language (QQL) filter.

    Params:
        auth (TokenAuth): The authentication object.
        page_count (int): The number of pages to get. Defaults to 'all'.

    ## Kwargs:

        filter (str): The Qualys QQL filter to use.
        excludeFields (str): The fields to exclude.
        includeFields (str): The fields to include.
        lastSeenAssetId (int): The last seen asset ID. Used for automatic pagination.
        lastModifiedDate (str): The last modified date.
        pageSize (int): The number of assets to get per page.

    Returns:
        BaseList[Host]: BaseList of Host objects.
    """

    responses = BaseList()
    pulled = 0
    completion_reason = "all pages complete"
    progress = ProgressTracker(
        logger=logger,
        operation="query_assets",
        item_label="assets collected",
        page_interval=10,
        time_interval=20.0,
    )

    while True:
        # make the request:
        response = call_api(auth=auth, module="gav", endpoint="query_assets", params=kwargs)
        # if there is no response, break the loop
        if not response.text:
            completion_reason = "no results returned"
            logger.info("No Results returned.")
            break

        j = response.json()

        if "responseCode" not in j.keys() or j["responseCode"] == "FAILED":
            raise QualysAPIError(j)

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
