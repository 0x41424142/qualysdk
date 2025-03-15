"""
Contains the middleware API call formatting for tagging APIs
"""

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
