"""
Interact with connectors for a given cloud provider.
"""

from typing import Union, Literal

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.Connectors import AWSConnector, AzureConnector


def get_connectors(
    auth: BasicAuth,
    provider: Literal["aws", "azure"],
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList[Union[AWSConnector, AzureConnector]]:
    """
    Get all Connector definitions from the Qualys CloudView API

    Params:
        auth (BasicAuth): The authentication object.
        provider (Literal['aws', 'azure']): The cloud provider to get connectors for.
        page_count (int): The number of pages to return. If 'all', return all pages. Default is 'all'.

    ## Kwargs:

        pageNo (int): The ordered page to start retrieving connectors from, or if page_count is 1, the page to retrieve.
        pageSize (int): The number of connectors to get per page.
        filter (str): Filter connectors by providing a query. Queryable fields are: name, description, state (SUCCESS, PENDING, REGIONS_DISCOVERED, ERROR), connector.uuid, lastSyncedOn (in UTC). Example: filter="name:MyConnector"
        sort (Literal['lastSyncedOn:asc', 'lastSyncedOn:desc']): Sort the connectors by lastSyncedOn in ascending or descending order.

    Returns:
        BaseList[Connector]: The response from the API as a BaseList of <provider>Connector objects.
    """

    # Check cloud provider is valid
    provider = provider.lower()
    if provider not in ["aws", "azure"]:
        raise QualysAPIError(
            f"Invalid provider {provider}. Valid providers: 'aws' or 'azure'"
        )

    responses = BaseList()
    currentPage = 0

    if kwargs.get("filter"):
        # Make sure the query key is valid
        if kwargs["filter"].split(":")[0] not in [
            "name",
            "description",
            "state",
            "connector.uuid",
            "lastSyncedOn",
        ]:
            raise QualysAPIError(
                "Invalid filter key. Valid keys: name, description, state, connector.uuid, lastSyncedOn"
            )
        # If using state, make sure value is UPPERCASE:
        if kwargs["filter"].split(":")[0] == "state":
            vals = kwargs["filter"].split(":")
            kwargs["filter"] = f"{vals[0]}:{vals[1].upper()}"

    while True:
        # Set the current page number and page size in kwargs
        kwargs["pageNo"] = currentPage
        # Set the cloudprovider in kwargs so it is appended to the URL path
        kwargs["cloudprovider"] = provider

        # Make the API request to retrieve the connectors
        response = call_api(
            auth=auth, module="cloudview", endpoint="get_connectors", params=kwargs
        )

        if response.status_code != 200:
            raise QualysAPIError(
                f"Error retrieving {provider} connectors. Status code: {response.status_code}. Requests reporting {response.reason}"
            )

        j = response.json()

        if len(j["content"]) == 0:
            print("No connectors found.")
            break

        # Iterate through the records in the response and create Connector objects
        for record in j["content"]:
            match provider:
                case "aws":
                    responses.append(AWSConnector(**record))
                case "azure":
                    responses.append(AzureConnector(**record))

        # Print a message indicating the current page was retrieved successfully
        print(f"Page {currentPage+1} of {provider} connectors retrieved successfully.")
        currentPage += 1

        # Break the loop if all pages are retrieved or the requested number of pages are retrieved
        if (page_count != "all" and currentPage + 1 > page_count) or j["last"]:
            break

    # Print a message indicating all pages have been retrieved
    print(
        f"All pages complete. {str(len(responses))} {provider} connector records retrieved."
    )

    return responses


def get_connector_details(
    auth: BasicAuth, provider: Literal["aws", "azure"], connectorId: str
) -> Union[AWSConnector, AzureConnector]:
    """
    Get details for a single connector by connectorId

    Params:
        auth (BasicAuth): The authentication object.
        provider (Literal['aws', 'azure']): The cloud provider to get connectors for.
        connectorId (str): The connectorId of the connector to get details for.

    Returns:
        Connector: The response from the API as a <provider>Connector object.
    """

    # Check cloud provider is valid
    provider = provider.lower()
    if provider not in ["aws", "azure"]:
        raise QualysAPIError(
            f"Invalid provider {provider}. Valid providers: 'aws' or 'azure'"
        )

    response = call_api(
        auth=auth,
        module="cloudview",
        endpoint="get_connector_details",
        params={
            "placeholder": connectorId,
            "cloudprovider": provider,
        },  # placeholders let us append the connectorId/cloud provider to the URL path
    )

    if response.status_code != 200:
        raise QualysAPIError(
            f"Error retrieving {provider} connector details. Status code: {response.status_code}"
        )

    j = response.json()

    match provider:
        case "aws":
            return AWSConnector(**j)
        case "azure":
            return AzureConnector(**j)
        case _:
            raise QualysAPIError(
                f"Invalid provider {provider}. Valid providers: 'aws' or 'azure'"
            )


# BEGIN PLATFORM SPECIFIC FUNCTIONS:

"""AWS FUNCTIONS"""


def get_aws_base_account(auth: BasicAuth) -> dict:
    """
    Get the AWS Base Account details

    Params:
        auth (BasicAuth): The authentication object.

    Returns:
        dict: The response from the API as a dictionary.
    """

    response = call_api(
        auth=auth,
        module="cloudview",
        endpoint="get_aws_base_account",
    )

    if response.status_code != 200:
        raise QualysAPIError(
            f"Error retrieving AWS base account details. Status code: {response.status_code}"
        )

    return response.json()
