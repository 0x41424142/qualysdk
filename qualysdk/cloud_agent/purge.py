"""
purge.py - Contains the user-facing functions for purging Cloud Agents singularly or in bulk.
"""

from ..base.call_api import call_api
from ..base.xml_parser import xml_parser
from ..auth.basic import BasicAuth
from .prepare_criteria import prepare_criteria


def purge_agent(auth: BasicAuth, asset_id: str) -> str:
    """
    Purge a single Cloud Agent from your subscription.

    Args:
        auth (BasicAuth): The authentication object containing the user's credentials.
        asset_id (str): The **Asset ID** of the Cloud Agent to purge.

    Returns:
        str: The response from the API call.
    """

    xml_data = (
        '<?xml version="1.0" encoding="UTF-8" ?> <ServiceRequest></ServiceRequest>'
    )

    payload = {
        "placeholder": asset_id,  # For formatting the URL
        "_xml_data": xml_data,  # call_api will override body with this
    }

    response = call_api(
        auth=auth,
        module="cloud_agent",
        endpoint="purge_agent",
        payload=payload,
    )

    data = xml_parser(response.text)

    return data.get("ServiceResponse").get("responseCode")


def bulk_purge_agent(auth: BasicAuth, **kwargs) -> str:
    """
    Delete hosts in bulk based on asset ID, asset name,
    creation date, updated date, tagName, or agentUuid.

    NOTE: IT IS **HIGHLY** RECOMMENDED TO USE THE **asset_id** PARAMETER AS THE ONLY FILTER.

    Args:
        auth (BasicAuth): The authentication object containing the user's credentials.
        **kwargs: The filters to apply to the bulk purge.

    ## Kwargs:

        asset_id (list[str]): A list of asset IDs to purge. HIGHLY RECOMMENDED.
        name (list[str]): A list of asset names to purge.
        created (Union[str, datetime.datetime]): The creation date of the asset. Formatted like ```YYYY-MM-DD[THH:MM:SSZ] as a str.
        updated (Union[str, datetime.datetime]): The updated date of the asset. Formatted like ```YYYY-MM-DD[THH:MM:SSZ] as a str.
        created_operator (Literal['GREATER', 'LESSER']): The operator to apply to the created date.
        updated_operator (Literal['GREATER', 'LESSER']): The operator to apply to the updated date.
        tagName (list[str]): A list of tag names to purge assets under.
        agentUuid (list[str]): A list of agent UUIDs to purge.

    Returns:
        str: The response from the API call.
    """

    payload = {"_xml_data": prepare_criteria(**kwargs)}

    response = call_api(
        auth=auth,
        module="cloud_agent",
        endpoint="bulk_purge_agent",
        payload=payload,
    )

    data = xml_parser(response.text)

    return (
        data.get("ServiceResponse").get("responseCode")
        if response.status_code == 200
        else "ERROR: "
        + xml_parser(response.text)
        .get("ServiceResponse")
        .get("responseErrorDetails")
        .get("errorMessage")
    )
