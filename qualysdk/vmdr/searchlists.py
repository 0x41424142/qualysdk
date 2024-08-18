"""
static_searchlists.py - Contains functions to interact with Static Searchlists in VMDR.
"""

from typing import *

from ..exceptions import *
from ..auth import BasicAuth
from ..base import call_api, xml_parser
from ..base.base_list import BaseList
from .data_classes import StaticSearchList


def get_static_searchlists(
    auth: BasicAuth, ids: str = None
) -> BaseList[StaticSearchList]:
    """
    Get a list of Static Searchlists in VMDR.

    Parameters:
        auth (BasicAuth): The authentication to use.
        ids (str): A comma-separated list of Static Searchlist IDs to retrieve.

    Returns:
        BaseList[StaticSearchlist]: A list of Static Searchlists.
    """
    responses = BaseList()
    params = {}
    params["action"] = "list"
    if ids:
        params["ids"] = ids

    resp = call_api(
        auth=auth,
        module="vmdr",
        endpoint="get_static_searchlists",
        params=params,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    searchlists = xml_parser(resp.text)

    if "STATIC_LISTS" not in searchlists["STATIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]:
        print("No Static Searchlists found.")
        return responses

    # If there is only one searchlist, it will not be in a list.
    if isinstance(
        searchlists["STATIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]["STATIC_LISTS"][
            "STATIC_LIST"
        ],
        dict,
    ):
        searchlists["STATIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]["STATIC_LISTS"][
            "STATIC_LIST"
        ] = [
            searchlists["STATIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]["STATIC_LISTS"][
                "STATIC_LIST"
            ]
        ]

    for searchlist in searchlists["STATIC_SEARCH_LIST_OUTPUT"]["RESPONSE"][
        "STATIC_LISTS"
    ]["STATIC_LIST"]:
        responses.append(StaticSearchList(**searchlist))

    return responses
