"""
Contains function to pull details on all cloud controls Qualys checks for.
"""

from typing import Union

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.Controls import Control


def get_control_metadata(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
):
    """
    Get controls Qualys checks a cloud provider for.

    Args:
        auth (BasicAuth): The authentication object.
        page_count (int): The number of pages to return. If 'all', return all pages. Default is 'all'.

    ## Kwargs:

        filter (str): Filter controls by providing a query. Queryable fields are:
        - control.name
        - resource.type
        - service.type
        - cid (supports control for IaC evaluations)
        - provider
        - control.criticality
        - control.type
        - policy.name
        - createdDate
        - modifiedDate
        - isCustomizable
        - qflow.name
        - qflow.id

        Example: filter="provider:AWS"

        pageNo (int): The ordered page to start retrieving controls from, or if page_count is 1, the page to retrieve.
        pageSize (int): The number of controls to get per page.

    Returns:
        BaseList[Control]: The response from the API as a BaseList of Control objects.
    """

    responses = BaseList()
    currentPage = 0

    if kwargs.get("filter"):
        # Make sure the query key is valid
        valid_controls = [
            "control.name",
            "resource.type",
            "service.type",
            "cid",
            "provider",
            "control.criticality",
            "control.type",
            "policy.name",
            "createdDate",
            "modifiedDate",
            "isCustomizable",
            "qflow.name",
            "qflow.id",
        ]

        if kwargs["filter"].split(":")[0] not in valid_controls:
            raise QualysAPIError(
                f"Invalid filter key. Valid keys: {', '.join(valid_controls)}"
            )

        # If provider, resource.type, control.criticality,
        # service.type, control.type is used in the filter, uppercase the value.
        if (
            "provider" in kwargs["filter"]
            or "resource.type" in kwargs["filter"]
            or "control.criticality" in kwargs["filter"]
            or "service.type" in kwargs["filter"]
            or "control.type" in kwargs["filter"]
        ):
            vals = kwargs["filter"].split(":")
            kwargs["filter"] = f"{vals[0]}:{vals[1].upper()}"

    while True:
        # Set the current page number and page size in kwargs
        kwargs["pageNo"] = currentPage

        # Make the API request to retrieve the connectors
        response = call_api(
            auth=auth,
            module="cloudview",
            endpoint="get_control_metadata",
            params=kwargs,
            headers={"accept": "application/json"},
        )

        if response.status_code != 200:
            raise QualysAPIError(
                f"Error retrieving controls. Status code: {response.status_code}. Requests reporting: {response.text}"
            )

        j = response.json()

        if len(j["control"]) == 0:
            print("No controls found.")
            break

        # Iterate through the records in the response and create Connector objects
        for record in j["control"]:
            responses.append(Control.from_dict(record))

        # Print a message indicating the current page was retrieved successfully
        print(f"Page {currentPage+1} of controls retrieved successfully.")
        currentPage += 1

        # Break the loop if all pages are retrieved or the requested number of pages are retrieved
        if (
            page_count != "all" and (currentPage + 1 > page_count)
        ) or "warning" not in j.keys():
            break

    # Print a message indicating all pages have been retrieved
    print(f"All pages complete. {str(len(responses))} control records retrieved.")

    return responses
