"""
purge.py - Contains the user-facing functions for purging Cloud Agents singularly or in bulk.
"""

from datetime import datetime

from ..base.call_api import call_api
from ..base.xml_parser import xml_parser
from ..auth.basic import BasicAuth


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
        created (Union[str, datetime.datetime]): The creation date of the asset.
        updated (Union[str, datetime.datetime]): The updated date of the asset.
        created_operator (Literal['GREATER_THAN', 'LESS_THAN']): The operator to apply to the created date.
        updated_operator (Literal['GREATER_THAN', 'LESS_THAN']): The operator to apply to the updated date.
        tagName (list[str]): A list of tag names to purge assets under.
        agentUuid (list[str]): A list of agent UUIDs to purge.

    Returns:
        str: The response from the API call.
    """

    # Prepare the base XML format
    xml = '<?xml version="1.0" encoding="UTF-8" ?><ServiceRequest><filters>{REPLACE}</filters></ServiceRequest>'

    # Add the filters to the XML

    # First, check if created and updated are datetime objects
    if "created" in kwargs and isinstance(kwargs["created"], datetime.datetime):
        kwargs["created"] = kwargs["created"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if "updated" in kwargs and isinstance(kwargs["updated"], datetime.datetime):
        kwargs["updated"] = kwargs["updated"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # For each kwarg filter, add it to the list value under the Criteria tag,
    # with field=kwarg and value=kwarg value
    # as well as a operator attribute with value="EQUALS" (unless
    # the kwarg is created or updated, in which case the created/updated_operator parameter):
    user_xml = ""

    # Map the kwargs to the tag name Qualys expects
    tag_lookup = {
        "asset_id": "id",
        "name": "name",
    }

    for kwarg, value in kwargs.items():
        if not isinstance(value, list) and kwarg not in ["created", "updated"]:
            criteria = f'<Criteria field="{tag_lookup.get(kwarg, kwarg)}" operator="EQUALS">{str(value)}</Criteria>'

        elif kwarg in ["created", "updated"]:
            operator = kwargs.get(
                f"{kwarg}_operator", "EQUALS"
            )  # Fallback to EQUALS if not provided for date fields
            criteria = (
                f'<Criteria field="{kwarg}" operator="{operator}">{value}</Criteria>'
            )

        elif isinstance(value, list):
            # Otherwise, if the value is a list, use the IN operator
            # and comma-sep strings for the values:
            criteria = f'<Criteria field="{tag_lookup.get(kwarg, kwarg)}" operator="IN">{",".join([str(v) for v in value])}</Criteria>'

        else:
            raise ValueError(f"Invalid value for {kwarg}: {value}")

        user_xml += criteria

    # Replace the {REPLACE} placeholder in the base XML with the user XML:
    xml = xml.format(REPLACE=user_xml)

    payload = {"_xml_data": xml}

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
