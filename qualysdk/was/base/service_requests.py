"""
Code to generate XML service requests to Qualys WAS API
"""

from typing import Literal, Union
from html import unescape

import xmltodict
from requests import Response

from ...base.xml_parser import xml_parser
from ...exceptions.Exceptions import QualysAPIError


def guaranteed_list(x):
    if not x:
        return []
    elif isinstance(x, list):
        return x
    else:
        return [x]


def validate_response(response: Response) -> dict:
    """
    Parse the XML response from the Qualys API
    and check for errors.

    Args:
        response (Response): The response object from the API call.

    Returns:
        dict: The parsed XML response.
    """
    parsed = xml_parser(response.text)

    if response.status_code != 200:
        errorMessage = parsed.get("ServiceResponse").get("responseErrorDetails")

        if errorMessage:
            errorMessage = errorMessage.get("errorMessage")

        responseCode = parsed.get("ServiceResponse").get("responseCode")
        raise QualysAPIError(
            f"Error retrieving web applications. Status code: {response.status_code}. Endpoint reporting: {responseCode}. Error message: {errorMessage}"
        )

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        errorMessage = (
            parsed.get("ServiceResponse")
            .get("responseErrorDetails")
            .get("errorMessage")
        )
        responseCode = parsed.get("ServiceResponse").get("responseCode")
        raise QualysAPIError(
            f"Error retrieving web applications. Status code: {response.status_code}. Endpoint reporting: {responseCode}. Error message: {errorMessage}"
        )

    return parsed


def build_service_request(
    _webapp_creation_or_edit: bool = False,
    action: Literal["set", "add", "remove"] = "set",
    authRecord_id: int = None,
    _uris: Union[str, list[str]] = None,
    tag_ids: Union[int, list[int]] = None,
    **kwargs,
) -> dict[str, str]:
    """
    Build the XML request. Users pass in the filters as kwargs.
    there is the filter itself as well as a filter_operator kwarg.
    If the filter_operator is not provided, default to "EQUALS".
    Do not create a Criteria tag for any _operator kwargs.

    Args:
        _webapp_creation_or_edit (bool, optional): If True, allows some tags to go into the DATA section instead of filters.
        action (Literal['set','add','remove'], optional): Whether to set, add, or remove various details.
        authRecord_id (int, optional): The ID of an authentication record
        _uris (Union[str, list[str]], optional): The URIs to be added to the WebApp. Can be a comma-separated string or a list of strings.

    Returns:
        dict: The XML payload to be sent to the Qualys API.
    """

    request_dict = {"ServiceRequest": {"filters": {}}}

    # Check for any tags that need to be under preferences instead of filters:
    PREFERENCE_TAGS = ["verbose"]

    # If this is a webapp creation or edit, move some tags to the DATA section:
    DATA_TAGS = ["name", "url"]

    preferences = {}
    for tag in PREFERENCE_TAGS:
        if tag in kwargs:
            preferences[tag] = (
                str(kwargs.pop(tag)).lower()
                if isinstance(kwargs[tag], bool)
                else kwargs.pop(tag)
            )

    if preferences:
        request_dict["ServiceRequest"]["preferences"] = preferences

    if _webapp_creation_or_edit:
        data = {"WebApp": {}}
        for tag in DATA_TAGS:
            if tag in kwargs:
                data["WebApp"][tag] = (
                    str(kwargs.pop(tag)).lower()
                    if isinstance(kwargs[tag], bool)
                    else kwargs.pop(tag)
                )
        request_dict["ServiceRequest"]["data"] = data

    # Integrate authRecord_id into the main XML structure if provided
    if authRecord_id:
        if "data" not in request_dict["ServiceRequest"]:
            request_dict["ServiceRequest"]["data"] = {}

        if "WebApp" not in request_dict["ServiceRequest"]["data"]:
            request_dict["ServiceRequest"]["data"]["WebApp"] = {}

        request_dict["ServiceRequest"]["data"]["WebApp"]["authRecords"] = {
            action: {"WebAppAuthRecord": {"id": authRecord_id}}
        }

    # Integrate URIs into the main XML structure if provided.
    # Uris is a list of strings.
    if _uris:
        if isinstance(_uris, str):
            _uris = _uris.split(",")
        # Check that all URIs are strings:
        if not isinstance(_uris, list) or not all(
            isinstance(uri, str) for uri in _uris
        ):
            raise ValueError(
                f"URIs must be passed as a list of strings or a comma-separated string, not {_uris}"
            )

        if "data" not in request_dict["ServiceRequest"]:
            request_dict["ServiceRequest"]["data"] = {}

        if "WebApp" not in request_dict["ServiceRequest"]["data"]:
            request_dict["ServiceRequest"]["data"]["WebApp"] = {}

        # Generate XML formatted URIs and join them into a single string.
        # Necessary due to how xmltodict handles lists and the format
        # Qualys expects.
        uriList = "".join(f"\n<Url>{uri}</Url>" for uri in _uris)

        # Update the request dictionary with the formatted URIs
        request_dict["ServiceRequest"]["data"]["WebApp"]["uris"] = {action: uriList}

    if tag_ids:
        if not isinstance(tag_ids, list):
            tag_ids = [tag_ids]

        # Make sure all tag_ids are integers:
        if not all(isinstance(tag_id, int) for tag_id in tag_ids):
            raise ValueError(
                f"Tag IDs must be integers, not {tag_ids}. Please provide a list of integers."
            )

        if "data" not in request_dict["ServiceRequest"]:
            request_dict["ServiceRequest"]["data"] = {}

        if "WebApp" not in request_dict["ServiceRequest"]["data"]:
            request_dict["ServiceRequest"]["data"]["WebApp"] = {}

        # Generate XML formatted tag IDs and join them into a single string.
        # Necessary due to how xmltodict handles lists and the format
        # Qualys expects.
        tagList = "".join(f"\n<Tag><id>{_id}</id></Tag>" for _id in tag_ids)

        # Update the request dictionary with the formatted tags:
        request_dict["ServiceRequest"]["data"]["WebApp"]["tags"] = {action: tagList}

    # Build the Criteria tags for the filters:
    filters = []
    for kwarg, value in kwargs.items():
        if kwarg.endswith(".operator"):
            continue
        # fields that go under WebApp:
        if kwarg in ["authRecord.id", "uris", "tag.ids"]:
            continue
        criteria = {
            "@field": kwarg,
            "@operator": kwargs.get(f"{kwarg}.operator", "EQUALS"),
            "#text": str(value).lower() if isinstance(value, bool) else value,
        }
        filters.append(criteria)

    if filters:
        request_dict["ServiceRequest"]["filters"]["Criteria"] = filters
    else:
        del request_dict["ServiceRequest"]["filters"]

    # Unescape any HTML. Necessary due to xmltodict's behavior.
    # This is especially relevant for URIs.
    xml = unescape(xmltodict.unparse(request_dict, pretty=True))
    payload = {"_xml_data": xml}

    return payload
