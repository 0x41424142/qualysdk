"""
Pull details on a single resource by its ID
"""

from typing import Union, Literal

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.AWSResources import *
from .data_classes.resource_mappings import *


def get_resource_details(
    auth: BasicAuth,
    provider: Literal["aws", "azure"],
    resourceType: str,
    resourceId: str,
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> object:
    """
    Get details of a single resource by its ID

    Params:
        auth (BasicAuth): The authentication object.
        provider (Literal['aws', 'azure']): The cloud provider of the resource.
        resourceType (str): The type of resource to get details for.
        resourceId (str): The ID of the resource to get details for.
        page_count (int): The number of pages to return. If 'all', return all pages. Default is 'all'.

    ## Kwargs:

        pageNo (int): The ordered page to start retrieving resources from, or if page_count is 1, the page to retrieve.
        pageSize (int): The number of resources to get per page.
        filter (str): Filter resources by providing a QQL query.
        sort (Literal['lastSyncedOn:asc', 'lastSyncedOn:desc']): Sort the resources by lastSyncedOn in ascending or descending order.
        updated (str): Filter resources by the last updated date. Format is Qualys QQL, like [2024-01-01 ... 2024-12-31], [2024-01-01 ... now-1m]

    Returns:
        object: The response from the API as an object.
    """

    # Check cloud provider is valid
    provider = provider.lower()
    if provider not in ["aws", "azure"]:
        raise QualysAPIError(
            f"Invalid provider {provider}. Valid providers: 'aws' or 'azure'"
        )

    resourceType = resourceType.upper()

    # Handle common names
    resourceType = resourceType.replace(" ", "_")
    for key, value in COMMON_NAMES[provider].items():
        if resourceType in value:
            resourceType = key
            break

    if resourceType not in VALID_RESOURCETYPES[provider]:
        raise ValueError(
            f"Invalid resource type for provider {provider}. Valid resource types are: {VALID_RESOURCETYPES[provider]}"
        )

    kwargs["placeholder"] = resourceType
    kwargs["resourceid"] = resourceId
    kwargs["cloudprovider"] = provider.upper()

    response = call_api(
        auth=auth,
        module="cloudview",
        endpoint="get_resource_details",
        params=kwargs,
    )

    if response.status_code not in [200, 400, 404]:
        if not response.text:
            raise QualysAPIError(
                "An error occurred while retrieving the resource details. Most likely, a parameter you set is incorrect."
            )
        else:
            raise QualysAPIError(response.json())

    j = response.json()

    if response.status_code == 200:
        resource_class = resource_map.get(resourceType, None)
        if resource_class:
            if "type" in j.keys():
                j["_type"] = j.pop("type")
            obj = resource_class(**j)
        else:
            raise ValueError(
                f"Invalid resource type {resourceType} for provider {provider}. Valid resource types are:\n{VALID_RESOURCETYPES[provider]}"
            )
        return obj

    else:
        j["resourceType"] = resourceType
        raise QualysAPIError(j)
