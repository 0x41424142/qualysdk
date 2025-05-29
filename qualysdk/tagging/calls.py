"""
Contains the middleware API call formatting for tagging APIs
"""

from typing import Union, overload

from .base.kwarg_validation import validate_kwargs
from .data_classes.Tag import Tag
from ..base.call_api import call_api
from ..auth.basic import BasicAuth
from ..base.base_list import BaseList


def call_tags_api(auth: BasicAuth, endpoint: str, payload: dict):
    """
    Call a Qualys Tagging API endpoint and return the parsed response. This is
    a backend function and should not be called directly.

    Args:
        auth (BasicAuth): The authentication object.
        endpoint (str): The API endpoint to call.
        payload (dict): The payload to send to the API.

    Returns:
        The parsed response from the API.
    """

    match endpoint:
        case "count_tags":
            params = {"placeholder": "count", "tagId": ""}
        case "get_tags":
            params = {"placeholder": "search", "tagId": ""}
        case "get_tag_info":
            params = {"placeholder": "get", "tagId": payload}
        case "create_tag":
            params = {"placeholder": "create", "tagId": ""}
        case "delete_tag":
            params = {"placeholder": "delete", "tagId": payload}
        case "update_tag":
            params = {"placeholder": "update", "tagId": ""}
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}")

    response = call_api(
        auth=auth,
        override_method="POST" if endpoint != "get_tag_info" else "GET",
        module="tagging",
        endpoint="call_tags_api",
        jsonbody=payload,
        params=params,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )

    data = response.json()

    if data.get("ServiceResponse", {}).get("responseCode") != "SUCCESS":
        errorDetails = data.get("ServiceResponse", {}).get("responseErrorDetails", {})
        raise ValueError(
            f"Failed to call {endpoint} API: {errorDetails.get('errorMessage')} - {errorDetails.get('errorResolution')}"
        )

    return data


def count_tags(auth: BasicAuth, **kwargs) -> int:
    """
    Get the number of tags that match the given kwarg filters

    Args:
        auth (BasicAuth): The authentication object
        **kwargs: The filters to apply to the tags

    ## Kwargs:

        - id (Union[str, int]): The tag id(s) to filter by
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): The operator to use for the id filter
        - name (str): The tag name to filter by
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): The operator to use for the name filter
        - parent (Union[str, int]): The parent tag id(s) to filter by
        - parent_operator (Literal["EQUALS", "NOT EQUALS","GREATER", "LESSER", "IN"]): The operator to use for the parent filter
        - ruleType (Literal["GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]): The rule type to filter by
        - ruleType_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): The operator to use for the ruleType filter
        - provider (Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]): The cloud provider to filter by
        - provider_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): The operator to use for the provider filter
        - color (str): The hex color code to filter by, such as #FFFFFF

    Returns:
        int: The number of tags that match the given filters
    """

    validate_kwargs("count_tags", **kwargs)

    # Build the service request:

    jsonpayload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": [],
            }
        }
    }

    for key, value in kwargs.items():
        if key.endswith("_operator"):
            continue

        operator = kwargs.get(f"{key}_operator", "EQUALS")

        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append(
            {
                "field": key,
                "operator": operator,
                "value": value,
            }
        )

    has_criteria = True if len(kwargs) > 0 else False

    response = call_tags_api(auth, "count_tags", jsonpayload if has_criteria else None)

    return response.get("ServiceResponse", {}).get("count", 0)


def get_tags(auth: BasicAuth, **kwargs) -> BaseList:
    """
    Get the tags that match the given kwarg filters

    Args:
        auth (BasicAuth): The authentication object
        **kwargs: The filters to apply to the tags

    ## Kwargs:

        - id (Union[str, int]): The tag id(s) to filter by
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): The operator to use for the id filter
        - name (str): The tag name to filter by
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): The operator to use for the name filter
        - parent (Union[str, int]): The parent tag id(s) to filter by
        - parent_operator (Literal["EQUALS", "NOT EQUALS","GREATER", "LESSER", "IN"]): The operator to use for the parent filter
        - ruleType (Literal["GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]): The rule type to filter by
        - ruleType_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): The operator to use for the ruleType filter
        - provider (Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]): The cloud provider to filter by
        - provider_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): The operator to use for the provider filter
        - color (str): The hex color code to filter by, such as #FFFFFF

    Returns:
        BaseList[Tag]: The tags that match the given filters
    """

    validate_kwargs("get_tags", **kwargs)

    has_more = True
    results = BaseList()
    # Build the service request:
    jsonpayload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": [],
            }
        }
    }
    for key, value in kwargs.items():
        if key.endswith("_operator"):
            continue

        operator = kwargs.get(f"{key}_operator", "EQUALS")

        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append(
            {
                "field": key,
                "operator": operator,
                "value": value,
            }
        )

    while has_more:
        response = call_tags_api(auth, "get_tags", jsonpayload)
        data = response.get("ServiceResponse", {}).get("data", {})
        if not data:
            print("No data found in response. Exiting...")
            return results
        if isinstance(data, dict):
            data = [data]
        for tag in data:
            results.append(Tag.from_dict(tag["Tag"]))

        has_more = response.get("ServiceResponse", {}).get("hasMoreRecords", False)
        if has_more not in [False, "false"]:
            jsonpayload["ServiceRequest"]["filters"]["Criteria"].append(
                {
                    "field": "id",
                    "operator": "GREATER",
                    "value": response.get("ServiceResponse", {}).get("lastId"),
                }
            )
            print("Pagination detected, fetching more results...")
        else:
            has_more = False

    print("No more results to fetch. Exiting...")
    return results


def get_tag_details(auth: BasicAuth, tag_id: Union[int, str]) -> Tag:
    """
    Get the details of a specific tag by its ID.

    Args:
        auth (BasicAuth): The authentication object.
        tag_id (str): The ID of the tag to retrieve.

    Returns:
        Tag: The details of the specified tag.
    """

    response = call_tags_api(auth, "get_tag_info", tag_id)
    data = response.get("ServiceResponse", {}).get("data", {})
    if not data:
        raise ValueError(f"No data found for tag ID {tag_id}")

    tag = data[0].get("Tag", {})
    if tag:
        return Tag.from_dict(tag)


def create_tag(auth: BasicAuth, name: str, **kwargs) -> Tag:
    """
    Create a new tag with the given name and optional parameters.

    If no ruleType is provided, the tag will be created as a static tag.

    Args:
        auth (BasicAuth): The authentication object.
        name (str): The name of the tag to create.
        **kwargs: Optional parameters for the tag.

    ## Kwargs:

        ruleType (Literal["STATIC", "GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]): The rule type for the tag.
        ruleText (str): The rule text for a new dynamic tag.
        children (list[str]): A list of child tag names to also create.
        parentTagId (int): The ID of the parent tag.
        criticalityScore (int): The criticality score for the tag.
        color (str): The hex color code for the tag, such as #FFFFFF.
        description (str): A description for the tag.
        provider (Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]): The cloud provider for the tag.

    Returns:
        Tag: The created tag object.
    """

    # Build the service request:
    payload_template = {
        "ServiceRequest": {
            "data": {
                "Tag": {
                    "name": name,
                    "ruleType": kwargs.get("ruleType"),
                    "ruleText": kwargs.get("ruleText"),
                    "parentTagId": kwargs.get("parentTagId"),
                    "criticalityScore": kwargs.get("criticalityScore"),
                    "color": kwargs.get("color"),
                    "description": kwargs.get("description"),
                    "provider": kwargs.get("provider"),
                }
            }
        }
    }

    # Remove any None values from the payload
    jsonpayload = {
        "ServiceRequest": {
            "data": {
                "Tag": {
                    k: v
                    for k, v in payload_template["ServiceRequest"]["data"]["Tag"].items()
                    if v is not None
                }
            }
        }
    }

    # Add children if provided
    if "children" in kwargs:
        jsonpayload["ServiceRequest"]["data"]["Tag"]["children"] = {
            "set": {"TagSimple": [{"name": child} for child in kwargs["children"]]}
        }

    response = call_tags_api(auth, "create_tag", jsonpayload)
    data = response.get("ServiceResponse", {}).get("data", {})
    if not data:
        raise ValueError(f"No data found for tag creation")

    tag = data[0].get("Tag", {})
    if tag:
        return Tag.from_dict(tag)


@overload
def delete_tag(auth: BasicAuth, tag_id: Union[int, str]) -> int:
    ...


@overload
def delete_tag(auth: BasicAuth, tag_id: list[Union[int, str]]) -> int:
    ...


def delete_tag(auth: BasicAuth, tag_id: Union[int, str, list[Union[int, str]]]) -> int:
    """
    Delete one or more tags by their IDs.

    This method supports overloading to handle both single and multiple tag IDs.
    To delete multiple tags, pass a list of IDs.
    To delete a single tag, pass a single ID.

    Args:
        auth (BasicAuth): The authentication object.
        tag_id (Union[int, str, list[Union[int, str]]]): The ID(s) of the tag(s) to delete.

    Returns:
        int: The number of tags deleted.
    """

    if not isinstance(tag_id, list):
        tag_id = [tag_id]
    deleted = 0
    for tag in tag_id:
        response = call_tags_api(auth, "delete_tag", tag)
        deleted += response.get("ServiceResponse", {}).get("count", 0)
    return deleted


def update_tag(auth: BasicAuth, tag_id: Union[int, str], **kwargs) -> Tag:
    """
    Update an existing tag with the given ID and optional parameters.

    NOTE: You should not try to add and remove children at the same time.

    Args:
        auth (BasicAuth): The authentication object.
        tag_id (Union[int, str]): The ID of the tag to update.
        **kwargs: Optional parameters for the tag.

    ## Kwargs:

        name (str): The new name of the tag.
        ruleType (Literal["STATIC", "GROOVY", "OS_REGEX", "NETWORK_RANGE", "NAME_CONTAINS", "INSTALLED_SOFTWARE", "OPEN_PORTS", "VULN_EXIST", "ASSET_SEARCH", "NETWORK_TAG", "NETWORK", "NETWORK_RANGE_ENHANCED", "CLOUD_ASSET", "GLOBAL_ASSET_VIEW", "TAGSET", "BUSINESS_INFORMATION", "VULN_DETECTION"]): The rule type for the tag.
        ruleText (str): The rule text for a new dynamic tag.
        add_children (list[str]): A list of child tag names to add/create.
        remove_children (list[str]): A list of child tag IDs to remove.
        parentTagId (int): The ID of the parent tag.
        criticalityScore (int): The criticality score for the tag.
        color (str): The hex color code for the tag, such as #FFFFFF.
        description (str): A description for the tag.
        provider (Literal["EC2", "AZURE", "GCP", "IBM", "OCI"]): The cloud provider for the tag.

    Returns:
        Tag: The updated tag object.
    """

    # if no kwargs are provided, raise an error
    if not kwargs:
        raise ValueError("No kwargs provided for tag update")

    # Build the service request:
    payload_template = {
        "ServiceRequest": {
            "data": {
                "Tag": {
                    "id": tag_id,
                    "name": kwargs.get("name"),
                    "ruleType": kwargs.get("ruleType"),
                    "ruleText": kwargs.get("ruleText"),
                    "parentTagId": kwargs.get("parentTagId"),
                    "criticalityScore": kwargs.get("criticalityScore"),
                    "color": kwargs.get("color"),
                    "description": kwargs.get("description"),
                    "provider": kwargs.get("provider"),
                }
            }
        }
    }

    # Remove any None values from the payload
    jsonpayload = {
        "ServiceRequest": {
            "data": {
                "Tag": {
                    k: v
                    for k, v in payload_template["ServiceRequest"]["data"]["Tag"].items()
                    if v is not None
                }
            }
        }
    }

    # Add children if provided
    if "add_children" in kwargs:
        jsonpayload["ServiceRequest"]["data"]["Tag"]["children"] = {
            "set": {"TagSimple": [{"name": child} for child in kwargs["add_children"]]}
        }
    # Remove children if provided
    if "remove_children" in kwargs:
        jsonpayload["ServiceRequest"]["data"]["Tag"]["children"] = {
            "remove": {"TagSimple": [{"id": child} for child in kwargs["remove_children"]]}
        }

    response = call_tags_api(auth, "update_tag", jsonpayload)
    data = response.get("ServiceResponse", {}).get("data", {})
    if not data:
        raise ValueError(f"No data found for tag update")
    tag = data[0].get("Tag", {})
    if tag:
        return Tag.from_dict(tag)
