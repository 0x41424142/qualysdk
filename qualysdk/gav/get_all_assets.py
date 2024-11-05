"""
get_all_assets.py - contains the get_all_assets function for the Global AssetView API (GAV) module.
"""

from typing import Union

from ..base.base_list import BaseList
from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *
from .hosts import Host


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

    while True:
        # make the request:
        response = call_api(
            auth=auth, module="gav", endpoint="get_all_assets", params=kwargs
        )
        j = response.json()

        if "responseCode" not in j.keys() or j["responseCode"] == "FAILED":
            raise QualysAPIError(j["responseMessage"])

        for record in j["assetListData"]["asset"]:
            responses.append(Host(**record))
        (
            print(f"Page {pulled+1} of {page_count} complete.")
            if page_count != "all"
            else print(f"Page {pulled+1} complete.")
        )
        pulled += 1

        if not j["hasMore"]:
            print("No more records.")
            break

        if page_count != "all" and pulled >= page_count:
            print("Page count reached.")
            break

        else:
            kwargs["lastSeenAssetId"] = j["lastSeenAssetId"]

    print("All pages complete.")
    return responses
