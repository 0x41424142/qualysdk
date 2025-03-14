"""
Code to generate XML service requests to Qualys WAS API
"""

from typing import Literal, Union, Dict, Any, List
from html import unescape
from re import compile

import xmltodict
from requests import Response

from ...base.xml_parser import xml_parser
from ...exceptions.Exceptions import QualysAPIError


def is_valid_regex(s: str) -> bool:
    """
    Attempts to use re.compile to test
    if a string is a valid regex.

    Args:
        s (str): The string to test.

    Returns:
        bool: Whether the string is a valid regex.
    """
    try:
        # Attempt to compile the string as a regex.
        compile(s)

        # If it contains common URL elements or non-regex patterns, return False
        # Examples: '://', '=', '&', 'www.', '.com', etc.
        if any(
            substring in s for substring in ["://", "=", "&", "www.", ".com", ".org"]
        ):
            return False

        return True
    except Exception as e:
        return False


def ensure_data_structure(request_dict: Dict[str, Any]) -> None:
    """
    Ensures that the 'data' and 'WebApp' keys exist in the request_dict.

    Args:
        request_dict (Dict[str, Any]): The dictionary where the 'data' and 'WebApp' keys need to be present.

    Returns:
        None
    """
    if "data" not in request_dict["ServiceRequest"]:
        request_dict["ServiceRequest"]["data"] = {}
    if "WebApp" not in request_dict["ServiceRequest"]["data"]:
        request_dict["ServiceRequest"]["data"]["WebApp"] = {}


def validate_list(
    input_data: Union[str, List[Any]], data_type: type, name: str
) -> List[Any]:
    """
    Validates that the input_data is a list of the specified data_type.
    Converts a comma-separated string into a list if needed.

    Args:
        input_data (Union[str, List[Any]]): The data to be validated, either as a list or a comma-separated string.
        data_type (type): The expected type of elements in the list (e.g., str, int).
        name (str): The name of the input (used for error messaging).

    Returns:
        List[Any]: The validated list of elements.

    Raises:
        ValueError: If input_data is not a list or a string that can be converted to a list of the expected type.
    """
    if isinstance(input_data, str):
        input_data = input_data.split(",")
    if not isinstance(input_data, list) or not all(
        isinstance(item, data_type) for item in input_data
    ):
        raise ValueError(
            f"{name} must be passed as a list of {data_type.__name__}s or a comma-separated string, not {input_data}"
        )
    return input_data


def update_request_dict(
    request_dict: Dict[str, Any],
    key: str,
    value: Any,
    action: Literal["add", "remove", "set"] = "set",
) -> None:
    """
    Updates the request_dict with a given key and value under the 'WebApp' section.

    Args:
        request_dict (Dict[str, Any]): The dictionary to be updated.
        key (str): The key under which the value will be stored.
        value (Any): The value to be stored in the request_dict.
        action (Literal["add", "remove", "set"], optional): The action to be taken on the value. Defaults to "set".

    Returns:
        None
    """
    ensure_data_structure(request_dict)
    request_dict["ServiceRequest"]["data"]["WebApp"][key] = {action: value}


def format_xml_list(items: List[Any], tag: str) -> str:
    """
    Formats a list of items into an XML string with the specified tag.

    Args:
        items (List[Any]): The list of items to be formatted as XML.
        tag (str): The XML tag to wrap around each item.

    Returns:
        str: A string containing the items formatted as XML elements.
    """
    if tag == "Tag":
        # Special case for tags, which have a different format
        return "".join(f"\n<Tag><id>{item}</id></Tag>" for item in items)
    else:
        return "".join(f"\n<{tag}>{item}</{tag}>" for item in items)


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
            f"WAS API Error. Status code: {response.status_code}. Endpoint reporting: {responseCode}. Error message: {errorMessage}"
        )

    # early exit if the request is for downloading scan results:
    if len(parsed) == 1 and "WasScan" in parsed.keys():
        return parsed

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
        if "Scan is not in a running state. Scan status: CANCELED" != errorMessage:
            raise QualysAPIError(
                f"WAS API Error. Status code: {response.status_code}. Endpoint reporting: {responseCode}. Error message: {errorMessage}"
            )

    return parsed


def build_service_request(
    _webapp_creation_or_edit: bool = False,
    authRecord_id: int = None,
    _uris: Union[str, list[str]] = None,
    tag_ids: Union[int, list[int]] = None,
    _domains: Union[str, list[str]] = None,
    _scannerTag_ids: Union[int, list[int]] = None,
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
        tag_ids (Union[int, list[int]], optional): The tag IDs to be added to the WebApp. Can be a single integer or a list of integers.
        domains (Union[str, list[str]], optional): The domains to be added to the WebApp. Can be a single string or a list of strings.
        _scannerTag_ids (Union[int, list[int]], optional): A tag ID associated with 1+ scanners to assign to the WebApp.

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
        update_request_dict(
            request_dict, "authRecords", {"WebAppAuthRecord": {"id": authRecord_id}}
        )

    # Integrate URIs into the main XML structure if provided
    if _uris:
        uris = validate_list(_uris, str, "URIs")
        uriList = format_xml_list(uris, "Url")
        update_request_dict(request_dict, "uris", uriList)

    # Integrate tag_ids into the main XML structure if provided
    if tag_ids:
        tag_ids = validate_list(tag_ids, int, "Tag IDs")
        tagList = format_xml_list(tag_ids, "Tag")
        update_request_dict(request_dict, "tags", tagList)

    # Integrate domains into the main XML structure if provided
    if _domains:
        domains = validate_list(_domains, str, "Domains")
        domainList = format_xml_list(domains, "Domain")
        update_request_dict(request_dict, "domains", domainList)

    if _scannerTag_ids:
        scannerTag_ids = validate_list(_scannerTag_ids, int, "Scanner Tag IDs")
        scannerTagList = format_xml_list(scannerTag_ids, "Tag")
        update_request_dict(request_dict, "defaultScannerTags", scannerTagList)

    # Build the Criteria tags for the filters:
    filters = []
    for kwarg, value in kwargs.items():
        if kwarg.endswith(".operator"):
            continue
        # fields that go under WebApp:
        if kwarg in [
            "authRecord.id",
            "uris",
            "tag.ids",
            "domains",
            "scannerTag.ids",
            "removeFromSubscription",
        ]:
            continue
        criteria = {
            "@field": kwarg,
            "@operator": kwargs.get(f"{kwarg}.operator", "EQUALS"),
            "#text": str(value).lower() if isinstance(value, bool) else str(value),
        }
        filters.append(criteria)

    if filters:
        request_dict["ServiceRequest"]["filters"]["Criteria"] = filters
        # If any filters snuck in that have a None #text value, remove them
        for criteria in request_dict["ServiceRequest"]["filters"]["Criteria"]:
            if criteria["#text"] is None:
                request_dict["ServiceRequest"]["filters"]["Criteria"].remove(criteria)
    else:
        del request_dict["ServiceRequest"]["filters"]

    # Unescape any HTML. Necessary due to xmltodict's behavior.
    try:
        xml = unescape(xmltodict.unparse(request_dict, pretty=True))
        payload = {"_xml_data": xml}
    except Exception as e:
        raise ValueError(f"Error unescaping XML: {e}")

    return payload


def build_update_request(
    name: str = None,
    url: str = None,
    attributes: Dict[
        Literal["add"] : [{"key", "value"}], Literal["remove"] : [str]
    ] = None,
    defaultProfile_id: int = None,
    _urlExcludelist: List[str] = None,
    _urlAllowlist: List[str] = None,
    _postDataExcludelist: List[str] = None,
    _useSitemap: bool = None,
    _headers: List[str] = None,
    _authRecord_id: Dict[Literal["add"] : [], Literal["remove"] : []] = None,
    **kwargs,
) -> dict[str, str]:
    """
    Build the XML update request. Users pass in the filters as kwargs.
    there is the filter itself as well as a filter_operator kwarg.
    If the filter_operator is not provided, default to "EQUALS".

    Args:
        name (str, optional): The name of the web application.
        url (str, optional): The URL of the web application.
        attributes (Dict[Literal['add']: List[Dict[str, str]], Literal['remove']: List[str]], optional): The attributes to add or remove from the web application.
        defaultProfile_id (int, optional): The ID of the default profile to assign to the web application.
        _urlExcludelist (List[str], optional): The list of URLs to exclude from the web application.
        _urlAllowlist (List[str], optional): The list of URLs to allow in the web application.
        _postDataExcludelist (List[str], optional): The list of post data to exclude from the web application.
        _useSitemap (bool, optional): Whether to use the sitemap for the web application.
        _headers (List[str], optional): The headers to add to the web application.
        _authRecord_id (Dict[Literal['add']: List[int], Literal['remove']: List[int]], optional): The authentication record IDs to add or remove from the web application.
        kwargs (dict): Additional filters to be passed to the Qualys API.

    Returns:
        dict: The XML payload to be sent to the Qualys API.
    """

    request_dict = {"ServiceRequest": {"data": {"WebApp": {}}}}

    if name:
        request_dict["ServiceRequest"]["data"]["WebApp"]["name"] = name

    if url:
        request_dict["ServiceRequest"]["data"]["WebApp"]["url"] = url

    if defaultProfile_id:
        request_dict["ServiceRequest"]["data"]["WebApp"]["defaultProfile"] = {
            "id": defaultProfile_id
        }

    if attributes:
        add_data = attributes.get("add")
        remove_data = attributes.get("remove")
        if add_data and not isinstance(add_data, list):
            add_data = [add_data]
        # Ensure that everything in the list is a dictionary
        for item in add_data:
            if not isinstance(item, dict):
                raise ValueError(
                    f"Attributes must be passed as a list of dictionaries. Key-value pairs are expected to add attributes. Received: {add_data}"
                )
        if remove_data and not isinstance(remove_data, list):
            remove_data = [remove_data]
        if add_data:
            for itm in add_data:
                for k, v in itm.items():
                    request_dict["ServiceRequest"]["data"]["WebApp"]["attributes"] = {
                        "update": {"Attribute": {"name": k, "value": v}}
                    }
        if remove_data:
            request_dict["ServiceRequest"]["data"]["WebApp"]["attributes"] = {
                "remove": {"Attribute": {"name": remove_data}}
            }

    if _authRecord_id:
        add_data = _authRecord_id.get("add")
        remove_data = _authRecord_id.get("remove")
        if add_data and not isinstance(add_data, list):
            add_data = [add_data]
        if remove_data and not isinstance(remove_data, list):
            remove_data = [remove_data]
        if add_data:
            request_dict["ServiceRequest"]["data"]["WebApp"]["authRecords"] = {
                "add": {"WebAppAuthRecord": {"id": add_data}}
            }
        if remove_data:
            request_dict["ServiceRequest"]["data"]["WebApp"]["authRecords"] = {
                "remove": {"WebAppAuthRecord": {"id": remove_data}}
            }

    if _urlExcludelist:
        urlExcludelist = _urlExcludelist
        if not isinstance(urlExcludelist, list):
            raise ValueError(
                f"urlExcludelist must be passed as a list of strings. Received: {urlExcludelist}"
            )

        entry_list = []
        for entry in urlExcludelist:
            # Check for any regex characters in the entry.
            # If found, set the regex attribute to true.
            if is_valid_regex(entry):
                entry_list.append(
                    xmltodict.unparse(
                        {"UrlEntry": {"@regex": "true", "#text": str(entry)}},
                        full_document=False,
                    )
                )
            else:
                entry_list.append(
                    xmltodict.unparse(
                        {"UrlEntry": {"@regex": "false", "#text": str(entry)}},
                        full_document=False,
                    )
                )

        request_dict["ServiceRequest"]["data"]["WebApp"]["urlExcludelist"] = {
            "set": "\n".join(entry_list)
        }

    if _urlAllowlist:
        if not isinstance(_urlAllowlist, list):
            raise ValueError(
                f"urlAllowlist must be passed as a list of strings. Received: {_urlAllowlist}"
            )
        url_list = []
        for entry in _urlAllowlist:
            # Check for any regex characters in the entry.
            # If found, set the regex attribute to true.
            if is_valid_regex(entry):
                url_list.append(
                    xmltodict.unparse(
                        {"UrlEntry": {"@regex": "true", "#text": str(entry)}},
                        full_document=False,
                    )
                )
            else:
                url_list.append(
                    xmltodict.unparse(
                        {"UrlEntry": {"@regex": "false", "#text": str(entry)}},
                        full_document=False,
                    )
                )

        request_dict["ServiceRequest"]["data"]["WebApp"]["urlAllowlist"] = {
            "set": "\n".join(url_list)
        }

    if _postDataExcludelist:
        if not isinstance(_postDataExcludelist, list):
            raise ValueError(
                f"postDataExcludelist must be passed as a list of strings. Received: {_postDataExcludelist}"
            )

        post_list = []
        for entry in _postDataExcludelist:
            # Check for any regex characters in the entry.
            # If found, set the regex attribute to true.
            if is_valid_regex(entry):
                post_list.append(
                    xmltodict.unparse(
                        {"UrlEntry": {"@regex": "true", "#text": str(entry)}},
                        full_document=False,
                    )
                )
            else:
                post_list.append(
                    xmltodict.unparse(
                        {"UrlEntry": {"@regex": "false", "#text": str(entry)}},
                        full_document=False,
                    )
                )

        request_dict["ServiceRequest"]["data"]["WebApp"]["postDataExcludelist"] = {
            "set": "\n".join(post_list)
        }

    if _useSitemap is not None:
        request_dict["ServiceRequest"]["data"]["WebApp"]["useSitemap"] = str(
            _useSitemap
        ).lower()

    if _headers:
        if not isinstance(_headers, list):
            raise ValueError(
                f"headers must be passed as a list of strings. Received: {_headers}"
            )
        header_list = []
        for header in _headers:
            header_list.append(
                xmltodict.unparse({"WebAppHeader": header}, full_document=False)
            )
        request_dict["ServiceRequest"]["data"]["WebApp"]["headers"] = {
            "set": "\n".join(header_list)
        }

    # Unescape any HTML. Necessary due to xmltodict's behavior.
    try:
        xml = unescape(xmltodict.unparse(request_dict, pretty=True))
        payload = {"_xml_data": xml}
    except Exception as e:
        raise ValueError(f"Error unescaping XML: {e}")

    return payload
