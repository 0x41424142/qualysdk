"""
Contains the get_remediation_activities function for Totalcloud
"""

from typing import Union, Literal

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.RemediationActivity import RemediationActivity


def get_remediation_activities(
    auth: BasicAuth,
    provider: Literal["aws", "azure"],
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList[dict]:
    """
    Pull remediation activity by cloud provider

    Args:
        auth (BasicAuth): The authentication object.
        provider (Literal['aws', 'azure']): The cloud provider of the resource.
        page_count (Union[int, 'all']): The number of pages to retrieve. If 'all', all pages are retrieved.

    ## Kwargs:
        - filter (str): Filter resources by providing a QQL [query](https://docs.qualys.com/en/cloudview/latest/search_tips/search_remediation_activity.htm?rhhlterm=search%20remediation%20activity%20activities&rhsearch=Search%20for%20Remediation%20Activity)
        - pageNo (int): The ordered page to start retrieving resources from, or if page_count is 1, the page to retrieve.
        - pageSize (int): The number of resources to get per page.

    Returns:
        BaseList[dict]: A list of dictionaries containing the remediation activities. WARNING: I have not seen the response from this API, so I am not sure what the response will look like.
    """

    if (page_count != "all" and (not isinstance(page_count, int))) or (
        isinstance(page_count, int) and page_count < 1
    ):
        raise ValueError("page_count must be an integer >=1 or 'all'.")

    if provider.lower() not in ["aws", "azure"]:
        raise ValueError("Invalid provider. Must be 'aws' or 'azure'.")

    params = {
        "cloudType": provider.upper(),
    }

    # Add in kwargs to the params
    if kwargs:
        params.update(kwargs)

    pulled_pages = 0
    bl = BaseList()

    while True:
        # Call the API
        response = call_api(
            auth=auth,
            module="cloudview",
            endpoint="get_remediation_activities",
            params=params,
        )

        # Check the response
        if response.status_code != 200:
            raise QualysAPIError(f"{response.status_code}: {response.text}")

        j = response.json()

        if "errorCode" in j:
            raise QualysAPIError(f"{j['errorCode']}, {j['message']}")

        if "content" not in j.keys() or not j["pageable"].get("empty"):
            print("No content in response")
            break

        data = j["content"]
        if isinstance(data, dict):
            data = [data]
        for item in data:
            bl.append(RemediationActivity.from_dict(item))

        # Check if we need to pull more pages
        if page_count != "all":
            pulled_pages += 1
            if pulled_pages >= page_count:
                print("Reached page limit of", page_count)
                break

    return bl
