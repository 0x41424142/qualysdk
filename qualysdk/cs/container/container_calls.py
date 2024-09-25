"""
Contains the code to interact with Docker hosts.
"""

from typing import Union
from urllib.parse import parse_qs

from ..data_classes.container import Container
from ...auth.token import TokenAuth
from ...base.call_api import call_api
from ...base.base_list import BaseList
from ...exceptions.Exceptions import *


def list_containers(
    auth: TokenAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> BaseList[Container]:
    """
    Get a list of all containers according to kwargs.

    Args:
        auth (TokenAuth): The authentication token.
        page_count (Union[int, 'all'] = 'all'): How many pages of results to retrieve.
        **kwargs: Any additional arguments to pass to the API.

    ## Kwargs:

    - filter (str): A filter to apply to the list using Qualys Container Security QQL.
    - paginationQuery (str): The pagination query to use. NOTE: The SDK handles this for you.
    - limit (int): The maximum number of results to return per page.

    Returns:
        BaseList[Container]: A list of Container objects.
    """

    # Check if page_count is valid:
    if page_count != "all" and not isinstance(page_count, int):
        raise ValueError("page_count must be an integer or 'all'.")

    results = BaseList()
    pages_pulled = 0

    while True:
        # Pull the data:
        response = call_api(auth, "containersecurity", "list_containers", params=kwargs)

        if response.status_code != 200 and response.text:
            raise QualysAPIError(response.json())
        elif response.status_code != 200 and not response.text:
            raise QualysAPIError(
                f"An error occurred with status code {response.status_code}. Qualys did not return any additional information."
            )

        data = response.json()

        # Check if the data is empty:
        if not data.get("data"):
            break

        if isinstance(data.get("data"), dict):
            # If the data is a dict, convert it to a list of dicts:
            data["data"] = [data["data"]]

        # Add the data to the results:
        for container in data["data"]:
            results.append(Container(**container))

        pages_pulled += 1

        # Check if we need to pull more pages:
        if page_count != "all" and pages_pulled >= page_count:
            print(f"Page count reached. Returning {pages_pulled} pages of containers.")
            break

        # Check the response headers for the next page:
        headers = dict(response.headers)
        if not headers.get("Link"):
            break
        else:
            # Use parse_qs to get the pagination query:
            pagination_query = parse_qs(headers["Link"].split(";")[0].strip("<>"))[
                "paginationQuery"
            ][0]
            kwargs["paginationQuery"] = pagination_query

    return results


def get_container_details(auth: TokenAuth, containerSha: str) -> Container:
    """
    Get details of a single container instance.

    Args:
        auth (TokenAuth): The authentication token.
        containerSha (str): The SHA hash of the container.

    Returns:
        Container: Container object with all attributes populated.
    """

    response = call_api(
        auth,
        module="containersecurity",
        endpoint="get_container_details",
        params={"placeholder": containerSha},
    )

    # Check for valid response:
    if response.status_code != 200:
        raise QualysAPIError(response.json())

    return Container.from_dict(response.json())
