"""
Contains the list_certs function
"""

from json import JSONDecodeError
from typing import Union

from .data_classes.Certificate import Certificate
from ..base.base_list import BaseList
from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import QualysAPIError


def list_certs(
    auth: TokenAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> dict:
    """
    Return a list of certificates that match the given kwargs.

    Args:
        auth (TokenAuth): The authentication object for the API
        page_count (Union[int, 'all']): The number of pages to retrieve. If 'all', retrieve all pages. Default is 'all'.
        **kwargs: The search parameters for the API call.

    **Kwargs:

        - certId (str): The certificate ID.
        - certId_operator (Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"]): The operator to use for the certId parameter. Default is "IS_NOT_EMPTY".
        - hash (str): The certificate hash.
        - hash_operator (Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"]): The operator to use for the hash parameter. Default is "IS_NOT_EMPTY".
        - validFromDate (str): The valid from date.
        - validFromDate_operator (Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"]): The operator to use for the validFromDate parameter. Default is "GREATER".
        - wasUrl (str): The WAS URL.
        - wasUrl_operator (Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"]): The operator to use for the wasUrl parameter. Default is "IS_NOT_EMPTY".
        - certificateType (Literal["Leaf", "Intermediate", "Root"]): The certificate type.
        - pageSize (int): The number of items to return per page. Default is 10.

    Returns:
        dict: The JSON response from the API.
    """

    # Check that page_count is either > 0 or 'all':
    if page_count != "all" and (not isinstance(page_count, int) or page_count <= 0):
        raise ValueError("page_count must be 'all' or > 0")

    pages_pulled = 0
    responses = BaseList()

    payload = {
        "filter": {
            "filters": [],
            "operator": "AND",
        },
        "pageNumber": 0,
        "pageSize": kwargs.pop("pageSize", 10),
        "includes": ["ASSET_INTERFACES", "ASSET_TAGS"],
        "assetType": "ALL",
    }

    """
    Filter structure:
    
    filters: [
        {
            "value": "string",
            "field": "string",
            "operator": "string"
        },
        ...
    ]
    """

    # Set up the filters from the kwargs.
    # Group by which _operator Literal is valid for each parameter.

    for key, value in kwargs.items():
        if key.endswith("_operator"):
            continue
        operator = (
            kwargs.get(f"{key}_operator", "IS_NOT_EMPTY")
            if key != "validFromDate"
            else "GREATER"
        )
        if operator not in [
            "IN",
            "LESSER",
            "IS_EMPTY",
            "GREATER",
            "GREATER_THAN_EQUAL",
            "IS_NOT_EMPTY",
            "EQUALS",
            "NOT_EQUALS",
            "LESS_THAN_EQUAL",
            "CONTAINS",
        ]:
            raise ValueError(f"Invalid operator: {operator}")

        if key == "certificateType":
            payload["filter"]["filters"].append(
                {"field": "certificate.type", "value": value, "operator": "EQUALS"}
            )
        else:
            payload["filter"]["filters"].append(
                {"field": key, "value": value, "operator": operator}
            )

    while True:
        response = call_api(
            auth=auth, module="cert", endpoint="list_certs", jsonbody=payload
        )

        response_json = response.json()
        if response.status_code != 200:
            raise QualysAPIError(response.text)

        for cert in response_json:
            responses.append(Certificate(**cert))
        pages_pulled += 1

        if page_count != "all" and pages_pulled >= page_count:
            print(f"Hit user-defined limit of {page_count} pages.")
            break

        if not response_json:
            break

        payload["pageNumber"] += 1

    return responses
