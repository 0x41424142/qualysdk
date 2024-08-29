"""
static_searchlists.py - Contains functions to interact with Static Searchlists in VMDR.
"""

from typing import *

from ..exceptions import *
from ..auth import BasicAuth
from ..base import call_api, xml_parser
from ..base.base_list import BaseList
from .data_classes import StaticSearchList, DynamicSearchList


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
    params["echo_request"] = False
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


def get_dynamic_searchlists(
    auth: BasicAuth, ids: str = None, **kwargs
) -> BaseList[DynamicSearchList]:
    """
    Get a BaseList of dynamic searchlists.

    Parameters:
        auth (BasicAuth): The authentication to use.
        ids (str): A comma-separated list of dynamic searchlist IDs to retrieve.

    ## Kwargs:

        show_qids (bool): Whether to show QIDs in the response.
        show_option_profiles (bool): Whether to show option profiles in the response.
        show_distribution_groups (bool): Whether to show distribution groups in the response.
        show_report_templates (bool): Whether to show report templates in the response.
        show_remediation_policies (bool): Whether to show remediation policies in the response.

    Returns:
        BaseList[DynamicSearchList]: A list of dynamic searchlists.
    """

    kwargs["action"] = "list"
    kwargs["echo_request"] = False

    if ids:
        kwargs["ids"] = ids

    responses = BaseList()

    resp = call_api(
        auth=auth,
        module="vmdr",
        endpoint="get_dynamic_searchlists",
        params=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    searchlists = xml_parser(resp.text)

    if "DYNAMIC_LISTS" not in searchlists["DYNAMIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]:
        print("No Dynamic Searchlists found.")
        return responses

    if isinstance(
        searchlists["DYNAMIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]["DYNAMIC_LISTS"][
            "DYNAMIC_LIST"
        ],
        dict,
    ):
        searchlists["DYNAMIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]["DYNAMIC_LISTS"][
            "DYNAMIC_LIST"
        ] = [
            searchlists["DYNAMIC_SEARCH_LIST_OUTPUT"]["RESPONSE"]["DYNAMIC_LISTS"][
                "DYNAMIC_LIST"
            ]
        ]

    for searchlist in searchlists["DYNAMIC_SEARCH_LIST_OUTPUT"]["RESPONSE"][
        "DYNAMIC_LISTS"
    ]["DYNAMIC_LIST"]:
        responses.append(DynamicSearchList(**searchlist))

    return responses
