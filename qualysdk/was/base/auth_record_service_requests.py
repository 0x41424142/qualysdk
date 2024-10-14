from typing import Any, Dict, List, Literal, Optional, Union
from html import unescape

from xmltodict import unparse


def unparse_to_xml_str(data: Dict[str, Any]) -> str:
    """
    Convert a dictionary to an XML string.

    Args:
         data (Dict[str, Any]): The dictionary to be converted.

    Returns:
         str: The XML string.
    """
    return (
        unescape(unparse(data, full_document=False, pretty=True))
        .replace("True", "true")
        .replace("False", "false")
    )


def remove_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return data

    # Create a new dictionary to avoid modifying the original while iterating
    new_dict = {}

    for key, value in data.items():
        if isinstance(value, dict):
            # Recursively clean the dictionary
            cleaned_dict = remove_none_values(value)
            if cleaned_dict:  # Only add non-empty dictionaries
                new_dict[key] = cleaned_dict
        elif isinstance(value, list):
            # Recursively clean each item in the list
            cleaned_list = [
                remove_none_values(item) for item in value if item or item == 0
            ]
            if cleaned_list:  # Only add non-empty lists
                new_dict[key] = cleaned_list
        elif (
            value or value == 0 or value is False
        ):  # Consider False and 0 as valid non-null values
            new_dict[key] = value

    return new_dict


def create_service_request(
    filters: Optional[
        List[
            Dict[
                str,
                Union[
                    str,
                    Literal[
                        "CONTAINS",
                        "IN",
                        "EQUALS",
                        "NOT EQUALS",
                        "GREATER",
                        "LESSER",
                        "NONE",
                    ],
                ],
            ]
        ]
    ] = None,
    preferences: Optional[Dict[str, Union[int, float]]] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Creates a dictionary representing a ServiceRequest.

    Args:
        filters (Optional[List[Dict[str, Union[str, Literal["CONTAINS", "IN", "EQUALS", "NOT EQUALS", "GREATER", "LESSER", "NONE"]]]]]): List of filter criteria.
        preferences (Optional[Dict[str, Union[int, float]]]): Preferences for the service request.
        data (Optional[Dict[str, Any]]): Data for the service request.

    Returns:
        Dict[str, Any]: A dictionary matching the ServiceRequest schema.
    """
    xml = {
        "ServiceRequest": {
            "filters": format_filters(filters) if filters else None,
            "preferences": format_preferences(preferences) if preferences else None,
            "data": {
                "WebAppAuthRecord": (
                    format_data(data).pop("WebAppAuthRecord") if data else None
                )
            },
        }
    }

    return remove_none_values(xml)


def format_filters(
    filters: List[
        Dict[
            str,
            Union[
                str,
                Literal[
                    "CONTAINS",
                    "IN",
                    "EQUALS",
                    "NOT EQUALS",
                    "GREATER",
                    "LESSER",
                    "NONE",
                ],
            ],
        ]
    ]
) -> Dict[str, Any]:
    """
    Formats the filters for the ServiceRequest.

    Args:
        filters (List[Dict[str, Union[str, Literal["CONTAINS", "IN", "EQUALS", "NOT EQUALS", "GREATER", "LESSER", "NONE"]]]]): List of filter criteria.

    Returns:
        Dict[str, Any]: A dictionary representing the filters.
    """
    for filter_ in filters:
        if not isinstance(filter_.get("field"), str):
            raise ValueError("Field must be a string.")
        if filter_.get("operator") not in [
            "CONTAINS",
            "IN",
            "EQUALS",
            "NOT EQUALS",
            "GREATER",
            "LESSER",
            "NONE",
        ]:
            raise ValueError("Invalid operator.")
        if not isinstance(filter_.get("value"), str):
            raise ValueError("Value must be a string.")
    return {
        "Criteria": [
            {"field": f["field"], "operator": f["operator"], "value": f["value"]}
            for f in filters
        ]
    }


def format_preferences(
    preferences: Dict[str, Union[int, float]]
) -> Dict[str, Union[int, float]]:
    """
    Formats the preferences for the ServiceRequest.

    Args:
        preferences (Dict[str, Union[int, float]]): Preferences for the service request.

    Returns:
        Dict[str, Union[int, float]]: A dictionary representing the preferences.
    """
    if "startFromId" in preferences and not isinstance(preferences["startFromId"], int):
        raise ValueError("startFromId must be an integer.")
    if "startFromOffset" in preferences and not isinstance(
        preferences["startFromOffset"], int
    ):
        raise ValueError("startFromOffset must be an integer.")
    if "limitResults" in preferences and not isinstance(
        preferences["limitResults"], int
    ):
        raise ValueError("limitResults must be an integer.")
    return preferences


def format_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the data for the ServiceRequest.

    Args:
        data (Dict[str, Any]): Data for the service request.

    Returns:
        Dict[str, Any]: A dictionary representing the data.
    """
    if "WebAppAuthRecord" in data:
        data["WebAppAuthRecord"] = format_web_app_auth_record(data["WebAppAuthRecord"])
    return data


def format_web_app_auth_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the WebAppAuthRecord.

    Args:
        record (Dict[str, Any]): WebAppAuthRecord data.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthRecord.
    """
    VALID = ["formRecord", "serverRecord", "oauth2Record", "tags", "comments", "name"]
    for key in record.keys():
        if key not in VALID:
            raise ValueError(f"Invalid key: {key}. Must be one of: {VALID}")

    if "formRecord" in record:
        record["formRecord"] = format_web_app_auth_form_record(record["formRecord"])
    if "serverRecord" in record:
        record["serverRecord"] = format_web_app_auth_server_record(
            record["serverRecord"]
        )
    if "oauth2Record" in record:
        record["oauth2Record"] = format_web_app_auth_oauth2_record(
            record["oauth2Record"]
        )
    if "tags" in record:
        record["tags"] = format_tag_list(record["tags"])
    if "comments" in record:
        record["comments"] = format_comment_list(record["comments"])
    return record


def format_web_app_auth_form_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the WebAppAuthFormRecord.

    Args:
        record (Dict[str, Any]): WebAppAuthFormRecord data.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthFormRecord.
    """
    if "type" in record and record["type"] not in [
        "NONE",
        "STANDARD",
        "CUSTOM",
        "SELENIUM",
    ]:
        raise ValueError(
            f"Invalid type {record['type']} for WebAppAuthFormRecord. Must be one of: {['NONE', 'STANDARD', 'CUSTOM', 'SELENIUM']}"
        )
    if "fields" in record:
        record["fields"] = format_web_app_auth_form_record_field_list(record["fields"])
    return record


def format_web_app_auth_form_record_field_list(
    fields: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, Any]:
    """
    Formats the WebAppAuthFormRecordFieldList.

    Args:
        fields (Dict[str, List[Dict[str, Any]]]): WebAppAuthFormRecordFieldList data.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthFormRecordFieldList.
    """
    return {
        "set": "".join(
            [
                f'\n<WebAppAuthFormRecordField><name>{field.get("name")}</name>\n<value>{field.get("value")}</value></WebAppAuthFormRecordField>\n'
                for field in fields.get("set", [])
            ]
        ),
        "add": "".join(
            [
                f'\n<WebAppAuthFormRecordField><name>{field.get("name")}</name>\n<secured>{field.get("secured")}</secured>\n<value>{field.get("value")}</value></WebAppAuthFormRecordField>\n'
                for field in fields.get("add", [])
            ]
        ),
        "remove": "".join(
            [
                f'\n<WebAppAuthFormRecordField><name>{field.get("name")}</name>\n<secured>{field.get("secured")}</secured>\n<value>{field.get("value")}</value></WebAppAuthFormRecordField>\n'
                for field in fields.get("remove", [])
            ]
        ),
        "update": "".join(
            [
                f'\n<WebAppAuthFormRecordField><name>{field.get("name")}</name>\n<secured>{field.get("secured")}</secured>\n<value>{field.get("value")}</value></WebAppAuthFormRecordField>\n'
                for field in fields.get("update", [])
            ]
        ),
    }


def format_web_app_auth_form_record_field(field: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats a WebAppAuthFormRecordField.

    Args:
        field (Dict[str, Any]): WebAppAuthFormRecordField data.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthFormRecordField.
    """
    if "name" in field and not isinstance(field["name"], str):
        raise ValueError("Field name must be a string.")
    if "secured" in field and not isinstance(field["secured"], bool):
        raise ValueError("Field secured must be a boolean.")
    if "value" in field and not isinstance(field["value"], str):
        raise ValueError("Field value must be a string.")
    # If <SeleniumScript>, we need to validate the data element:
    if "data" in field and not isinstance(field["data"], str):
        try:
            field["data"] = unparse(field["data"])
        except Exception as e:
            raise ValueError(f"Field data must be a string or an XNL-like dictionary.")
    return field


def format_web_app_auth_server_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the WebAppAuthServerRecord.

    Args:
        record (Dict[str, Any]): WebAppAuthServerRecord data.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthServerRecord.
    """
    if "fields" in record and (
        record["fields"].get("set")
        or record["fields"].get("add")
        or record["fields"].get("remove")
        or record["fields"].get("update")
    ):
        record["fields"] = format_web_app_auth_server_record_field_list(
            record["fields"]
        )
    return record


def format_web_app_auth_server_record_field_list(
    fields: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, Any]:
    """
    Formats the WebAppAuthServerRecordFieldList.

    Args:
        fields (Dict[str, List[Dict[str, Any]]]): WebAppAuthServerRecordFieldList data.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthServerRecordFieldList.
    """
    return {
        "set": [
            format_web_app_auth_server_record_field(field, "set")
            for field in fields.get("set", [])
        ],
        "add": [
            format_web_app_auth_server_record_field(field, "add")
            for field in fields.get("add", [])
        ],
        "remove": [
            format_web_app_auth_server_record_field(field, "remove")
            for field in fields.get("remove", [])
        ],
        "update": [
            format_web_app_auth_server_record_field(field, "update")
            for field in fields.get("update", [])
        ],
    }


def format_web_app_auth_server_record_field(
    field: Dict[str, Any], command: Literal["set", "remove", "add", "update"]
) -> Dict[str, Any]:
    """
    Formats a WebAppAuthServerRecordField.

    Args:
        field (Dict[str, Any]): WebAppAuthServerRecordField data.
        command (Literal["set", "remove", "add", "update"]): The command to use as an element.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthServerRecordField.
    """
    if "type" in field and field["type"] not in ["BASIC", "DIGEST", "NTLM"]:
        raise ValueError("Invalid type for WebAppAuthServerRecordField.")
    if "domain" in field and not isinstance(field["domain"], str):
        raise ValueError("Field domain must be a string.")
    if "username" in field and not isinstance(field["username"], str):
        raise ValueError("Field username must be a string.")
    if "password" in field and not isinstance(field["password"], str):
        raise ValueError("Field password must be a string.")

    match command:
        case "set":
            return "".join(
                [
                    f'\n<WebAppAuthServerRecordField>\n<domain>{field.get("domain")}</domain>\n<username>{field.get("username")}</username>\n<password>{field.get("password")}</password></WebAppAuthServerRecordField>\n'
                ]
            )
        case "add":
            return "".join(
                [
                    f'\n<WebAppAuthServerRecordField>\n<domain>{field.get("domain")}</domain>\n<username>{field.get("username")}</username>\n<password>{field.get("password")}</password></WebAppAuthServerRecordField>\n'
                ]
            )
        case "remove":
            return "".join(
                [
                    f'\n<WebAppAuthServerRecordField>\n<domain>{field.get("domain")}</domain>\n<username>{field.get("username")}</username>\n<password>{field.get("password")}</password></WebAppAuthServerRecordField>\n'
                ]
            )
        case "update":
            return "".join(
                [
                    f'\n<WebAppAuthServerRecordField>\n<domain>{field.get("domain")}</domain>\n<username>{field.get("username")}</username>\n<password>{field.get("password")}</password></WebAppAuthServerRecordField>\n'
                ]
            )
        case _:
            raise ValueError("Invalid command for WebAppAuthServerRecordField.")


def format_web_app_auth_oauth2_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the WebAppAuthOAuth2Record.

    Args:
        record (Dict[str, Any]): WebAppAuthOAuth2Record data.

    Returns:
        Dict[str, Any]: A dictionary representing the WebAppAuthOAuth2Record.
    """
    if "grantType" in record and record["grantType"] not in [
        "NONE",
        "AUTH_CODE",
        "IMPLICIT",
        "PASSWORD",
        "CLIENT_CREDS",
    ]:
        raise ValueError("Invalid grantType for WebAppAuthOAuth2Record.")
    if (
        record.get("seleniumScript")
        and record["seleniumScript"].get("data")
        and not isinstance(record["seleniumScript"]["data"], str)
    ):
        try:
            record["seleniumScript"]["data"] = unparse(record["seleniumScript"]["data"])
        except Exception as e:
            raise ValueError(
                f"SeleniumScript data must be a string or an XML-like dictionary."
            )
    return record


def format_tag_list(tags: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Formats the TagList.

    Args:
        tags (Dict[str, List[Dict[str, Any]]]): TagList data.

    Returns:
        Dict[str, Any]: A dictionary representing the TagList.
    """
    """return {
        "set": tags.get("set", []),
        "add": tags.get("add", []),
        "remove": tags.get("remove", []),
    }"""

    # BUG: Above needs to be refactored to build a "".join() string of the XML elements for the tags.
    # due to xmltodict's behavior.
    # CORRECTION:
    return {
        "set": "".join(
            [f'\n<Tag>\n<id>{tag["id"]}</id>\n</Tag>' for tag in tags.get("set", [])]
        ),
        "add": "".join(
            [f'\n<Tag>\n<id>{tag["id"]}</id>\n</Tag>' for tag in tags.get("add", [])]
        ),
        "remove": "".join(
            [f'\n<Tag>\n<id>{tag["id"]}</id>\n</Tag>' for tag in tags.get("remove", [])]
        ),
        "update": "".join(
            [f'\n<Tag>\n<id>{tag["id"]}</id>\n</Tag>' for tag in tags.get("update", [])]
        ),
    }


def format_comment_list(comments: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Formats the CommentList.

    Args:
        comments (Dict[str, List[str]]): CommentList data.

    Returns:
        Dict[str, Any]: A dictionary representing the CommentList.
    """
    # Strange xmltodict behavior forces us to build a string of the XML elements for the comments.
    return {
        "set": "".join(
            [
                f"\n<Comment>\n<contents>{comment}</contents>\n</Comment>"
                for comment in comments.get("set", [])
            ]
        ),
        "add": "".join(
            [
                f"\n<Comment>\n<contents>{comment}</contents>\n</Comment>"
                for comment in comments.get("add", [])
            ]
        ),
        "remove": "".join(
            [
                f"\n<Comment>\n<contents>{comment}</contents>\n</Comment>"
                for comment in comments.get("remove", [])
            ]
        ),
        "update": "".join(
            [
                f"\n<Comment>\n<contents>{comment}</contents>\n</Comment>"
                for comment in comments.get("update", [])
            ]
        ),
    }
