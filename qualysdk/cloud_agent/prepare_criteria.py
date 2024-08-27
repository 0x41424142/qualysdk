"""
prepare_criteria.py - backend function to prepare XML string (Criteria tag) for Qualys Cloud Agent API calls
"""

import datetime


def prepare_criteria(**kwargs):
    """
    Prepare the XML string for the filters to apply to the API call.

    Args:
        **kwargs: The filters to apply to the API call.

    ## Kwargs:

        asset_id (list[str]): A list of asset IDs to filter.
        name (list[str]): A list of asset names to filter.
        created (Union[str, datetime.datetime]): The creation date of the asset.
        updated (Union[str, datetime.datetime]): The updated date of the asset.
        created_operator (Literal['GREATER', 'LESSER']): The operator to apply to the created date.
        updated_operator (Literal['GREATER', 'LESSER']): The operator to apply to the updated date.
        tagName (list[str]): A list of tag names to filter assets under.
        agentUuid (list[str]): A list of agent UUIDs to filter.
        pagination_id (int): The pagination ID to use for the API call.

    Returns:
        str: The XML string to pass to the API call.
    """
    # Prepare the base XML format
    xml = '<?xml version="1.0" encoding="UTF-8" ?><ServiceRequest><filters>{REPLACE}</filters></ServiceRequest>'

    DATE_FIELDS = [
        "created",
        "updated",
        "lastVulnScan",
        "lastComplianceScan",
        "informationGatheredUpdated",
        "lastComplianceScan",
        "lastSystemBoot",
        "lastLoggedOnUser",
        "vulnsUpdated",
        "lastCheckedIn",
        "update",
    ]

    # Add the filters to the XML

    # First, check if created and updated are datetime objects
    for field in DATE_FIELDS:
        if field in kwargs and isinstance(kwargs[field], datetime.datetime):
            kwargs[field] = kwargs[field].strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # For each kwarg filter, add it to the list value under the Criteria tag,
    # with field=kwarg and value=kwarg value
    # as well as a operator attribute with value="EQUALS" (unless
    # the kwarg is created or updated, in which case the created/updated_operator parameter):
    user_xml = ""

    # Map the kwargs to the tag name Qualys expects
    tag_lookup = {
        "asset_id": "id",
        "pagination_id": "id",
    }

    for kwarg, value in (
        (kwarg, value)
        for kwarg, value in kwargs.items()
        if "operator" not in kwarg and "pagination_id" not in kwarg
    ):
        if not isinstance(value, list) and kwarg not in DATE_FIELDS:
            criteria = f'<Criteria field="{tag_lookup.get(kwarg, kwarg)}" operator="EQUALS">{str(value)}</Criteria>'

        elif kwarg in DATE_FIELDS:
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

    if kwargs.get("pagination_id"):
        user_xml += f'<Criteria field="id" operator="GREATER">{kwargs["pagination_id"]}</Criteria>'

    # Replace the {REPLACE} placeholder in the base XML with the user XML:
    return xml.format(REPLACE=user_xml)
