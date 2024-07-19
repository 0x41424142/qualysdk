"""
assetgroups.py - AG manipulation functions for the Qualys VMDR module.
"""

from typing import *
from urllib.parse import parse_qs, urlparse

from ..auth import BasicAuth
from .data_classes import AssetGroup, BaseList
from ..base import *


def get_ag_list(
    auth: BasicAuth, page_count: Union["all", int] = "all", **kwargs
) -> list[AssetGroup]:
    """
    Gets a list of asset groups from the Qualys subscription.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.
        page_count (Union["all", int]): The number of pages to retrieve. Defaults to "all". If an integer is passed, that number of pages will be retrieved.

    Keyword Args:
        ```
        action (str): Action to perform on the asset groups. Defaults to "list". WARNING: SDK automatically sets this value to list. It is just included for completeness.
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: SDK automatically sets this value to 0. It is just included for completeness.
        output_format (Literal["csv", "xml"]): The output format of the response. Defaults to "xml". WARNING: SDK automatically sets this value to xml. It is just included for completeness.
        ids (str): The ID of the asset group to get. Defaults to None (all), but can be a single ID or a comma-separated string of IDs.
        id_min (int): The minimum ID of the asset group to get. Defaults to None.
        id_max (int): The maximum ID of the asset group to get. Defaults to None.
        truncation_limit (int): The truncation limit of the asset groups. Defaults to all records. 0 indicates all records. If non-0, the response will be truncated to the specified number of records. Pagination is handled automatically.
        network_ids (str): The network IDs of the asset groups to get. Defaults to None. Can be a single ID or a comma-separated string of IDs. WARNING: This has to be enabled in the Qualys subscription!
        unit_id (str): The unit ID of the asset groups to get. Defaults to None. Must be a single ID.
        user_id (str): The user ID of the asset groups to get. Defaults to None. Must be a single ID.
        title (str): The title of the asset groups to get. Defaults to None. Must be an exact match.
        show_attributes (Union[None, str]): Choose what attributes are returned. Defaults to None (show basic attrs), can be "ALL", "ID", "TITLE", .. For full list, see Qualys documentation: https://cdn2.qualys.com/docs/qualys-api-vmpc-user-guide.pdf
        ```
    Returns:
        BaseList[AssetGroup]: BaseList object containing the AssetGroup objects.
    """

    if type(page_count) in [int, float] and page_count <= 0:
        raise ValueError("page_count must be 'all' or an integer greater than 0.")

    results = BaseList()
    pulled = 0

    while True:
        kwargs["action"] = "list"
        kwargs["echo_request"] = False
        kwargs["output_format"] = "xml"

        # Enforce uppercase for show_attributes:
        if kwargs.get("show_attributes"):
            kwargs["show_attributes"] = kwargs["show_attributes"].upper()

        response = call_api(
            auth=auth,
            module="vmdr",
            endpoint="get_ag_list",
            params=kwargs,
            headers={"X-Requested-With": "qualyspy SDK"},
        )

        if response.status_code == 200:
            data = xml_parser(response.text)["ASSET_GROUP_LIST_OUTPUT"]

            if "ASSET_GROUP" not in data["RESPONSE"]["ASSET_GROUP_LIST"]:
                print("No asset groups found. Returning empty BaseList.")
                break

            # Check if type(data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"]) is dict.
            # If so, put it inside a list to normalize the class instantiation.
            if isinstance(data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"], dict):
                data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"] = [
                    data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"]
                ]

            for ag in data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"]:
                results.append(AssetGroup(**ag))

            pulled += 1
            # Check page count:
            if page_count != "all" and pulled >= page_count:
                print(f"Page count reached. Returning {pulled} pages.")
                break

            # Check for pagination:
            if data["RESPONSE"].get("WARNING"):
                # Get the id_min param:
                url = data["RESPONSE"]["WARNING"]["URL"]
                parsed_url = urlparse(url)
                id_min = parse_qs(parsed_url.query)["id_min"][0]
                kwargs["id_min"] = id_min
                print(f"Pagination detected. new id_min param: {id_min}")
            else:
                break

    return results
