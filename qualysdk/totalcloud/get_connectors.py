"""
get_connectors.py - returns a list of Connector objects
"""

from typing import Union

# Import necessary modules and functions
from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.connector import Connector


def get_connectors(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> BaseList[Connector]:
    """
    Get all Connector definitions from the Qualys CloudView API

    Params:
        auth (BasicAuth): The authentication object.
        page_count (int): The number of pages to return. If 'all', return all pages. Default is 'all'.

    ## Kwargs:

        pageNo (int): The ordered page to start retrieving connectors from, or if page_count is 1, the page to retrieve.
        pageSize (int): The number of connectors to get per page.
        filter (str): Filter connectors by providing a query. Queryable fields are: name, description, state (SUCCESS, PENDING, REGIONS_DISCOVERED, ERROR), connector.uuid, lastSyncedOn (in UTC). Example: filter="name:MyConnector"
        sort (Literal['lastSyncedOn:asc', 'lastSyncedOn:desc']): Sort the connectors by lastSyncedOn in ascending or descending order.

    Returns:
        BaseList[Connector]: The response from the API as a BaseList of Connector objects.
    """
    responses = BaseList()
    currentPage = 0

    while True:
        # Set the current page number and page size in kwargs
        kwargs["pageNo"] = currentPage

        # Make the API request to retrieve the connectors
        response = call_api(
            auth=auth, module="cloudview", endpoint="get_connectors", params=kwargs
        )

        if response.status_code != 200:
            raise QualysAPIError(
                f"Error retrieving connectors. Status code: {response.status_code}"
            )

        j = response.json()

        if len(j["content"]) == 0:
            print("No connectors found.")
            break

        # Iterate through the records in the response and create Connector objects
        for record in j["content"]:
            responses.append(Connector(**record))

        # Print a message indicating the current page was retrieved successfully
        print(f"Page {currentPage+1} retrieved successfully.")
        currentPage += 1

        # Break the loop if all pages are retrieved or the requested number of pages are retrieved
        if (page_count != "all" and currentPage + 1 > page_count) or j["last"]:
            break

    # Print a message indicating all pages have been retrieved
    print(f"All pages complete. {str(len(responses))} Connector records retrieved.")

    return responses
