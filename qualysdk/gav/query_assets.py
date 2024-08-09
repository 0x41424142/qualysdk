"""
query_assets.py - contains the query_assets function for the Global AssetView API (GAV) module.

Gets all assets that satisfy a Qualys Query Language (QQL) filter.
"""

from typing import Union

from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *
from .hosts import Host


def query_assets(
    auth: TokenAuth, page_count: Union["all", int] = "all", **kwargs
) -> list[Host]:
    """
    Queries GAV inventory for assets that satisfy a Qualys Query Language (QQL) filter.

    Params:
        auth (TokenAuth): The authentication object.
        page_count (int): The number of pages to get. Defaults to 'all'.

    :Kwargs:
        filter (str): The Qualys QQL filter to use.
        excludeFields (str): The fields to exclude.
        includeFields (str): The fields to include.
        lastSeenAssetId (int): The last seen asset ID. Used for automatic pagination.
        lastModifiedDate (str): The last modified date.
        pageSize (int): The number of assets to get per page.

    Returns:
        List[Host]: List of Host objects.
    """

    responses = []  # list to hold all the responses
    pulled = 0

    while True:
        # make the request:
        response = call_api(
            auth=auth, module="gav", endpoint="query_assets", params=kwargs
        )
        # if there is no response, break the loop
        if response.text == "":
            print("No Results returned.")
            break

        j = response.json()
        for record in j["assetListData"]["asset"]:
            responses.append(Host(**record))
        (
            print(f"Page {pulled+1} of {page_count}complete.")
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
