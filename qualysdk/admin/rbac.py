"""
Administration RBAC (Role-Based Access Control) APIs

These APIs allow for the management of user roles, tags and permissions within the Qualys platform.
"""

from typing import Union, overload, Literal

from xmltodict import unparse

from .data_classes.User import User
from ..auth import BasicAuth
from ..base.base_list import BaseList
from ..base.call_api import call_api

_UserIdOperator = ["EQUALS", "GREATER", "LESSER"]


@overload
def get_user_details(auth: BasicAuth, user_id: Union[int, str]) -> User:
    ...


@overload
def get_user_details(auth: BasicAuth, user_id: Union[list[int], list[str]]) -> BaseList[User]:
    ...


def get_user_details(
    auth: BasicAuth, user_id: Union[int, str, list[int], list[str]]
) -> Union[User, BaseList[User]]:
    """
    Get the administration details of user(s) by their admin user ID.

    :param auth: Authentication object
    :param user_id: Admin user ID or list of Admin user IDs to query
    :return: User object or BaseList of User objects
    """

    users = []
    responses = BaseList()

    if isinstance(user_id, (int, str)):
        # single user ID
        users.append(user_id)
    elif isinstance(user_id, (BaseList, list)) and all(
        isinstance(uid, (int, str)) for uid in user_id
    ):
        # list of user IDs
        users.extend(user_id)
    else:
        raise TypeError("user_id must be an int, str, or list of ints/strs")

    for uid in users:
        print(f"Querying user ID: {uid}")
        response = call_api(
            auth=auth,
            module="admin",
            endpoint="get_user_details",
            params={"placeholder": uid},
            headers={"Accept": "application/json"},
        )

        response.raise_for_status()
        data = response.json()
        if "responseErrorDetails" in data.get("ServiceResponse", {}):
            print(f"{data['ServiceResponse']['responseErrorDetails']['errorMessage']}")
            continue

        else:
            responses.append(User(**data["ServiceResponse"]["data"][0]["User"]))

    if len(responses) == 1:
        return responses[0]
    else:
        return responses


def search_users(
    auth: BasicAuth,
    user_id: Union[int, str] = None,
    user_id_operator: Literal["EQUALS", "GREATER", "LESSER"] = "EQUALS",
    username: str = None,
    role_name: Union[str, list[str]] = None,
) -> BaseList[User]:
    """
    Search for users based on various criteria.

    NOTE: To get all users, set `user_id` to 1 and `user_id_operator` to 'GREATER'.

    :param auth: Authentication object
    :param user_id: The ID of the user to search for.
    :param user_id_operator: The operator to use when searching by user ID. Defaults to 'EQUALS'. Must be one of 'EQUALS', 'GREATER', or 'LESSER'.
    :param username: The username of the user to search for.
    :param role_name: The name of the role to search for. Can be a single string, comma-separated string or a list of strings.
    :return: BaseList of User objects that match the search criteria.
    :raises ValueError: If no search criteria are provided.
    :raises TypeError: If the types of the provided parameters are incorrect.
    """

    # First, check search criteria
    if not any([user_id, username, role_name]):
        raise ValueError(
            "At least one search criterion must be provided: user_id, username, or role_name."
        )

    jsonpayload = {"ServiceRequest": {"filters": {"Criteria": []}}}

    if user_id is not None:
        # user_id can be only be a single int or str
        if not isinstance(user_id, (int, str)):
            raise TypeError("user_id must be an int or str")
        if user_id_operator not in _UserIdOperator:
            raise ValueError(f"user_id_operator must be one of {_UserIdOperator}")
        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append(
            {"field": "id", "operator": user_id_operator, "value": user_id}
        )

    if username is not None:
        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append(
            {
                "field": "username",
                "operator": "EQUALS",
                "value": username,
            }
        )

    if role_name is not None:
        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append(
            {"field": "roleName", "operator": "EQUALS", "value": role_name}
        )

    # start pagination
    users_list = BaseList()
    while True:
        response = call_api(
            auth=auth,
            module="admin",
            endpoint="search_users",
            jsonbody=jsonpayload,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

        data = response.json()
        if data.get("ServiceResponse", {}).get("responseErrorDetails"):
            print(f"{data['ServiceResponse']['responseErrorDetails']['errorMessage']}")
            break

        if data["ServiceResponse"].get("count", 0) == 0 and "data" not in data["ServiceResponse"]:
            print("No users found matching the search criteria.")
            break

        users = data["ServiceResponse"]["data"]

        if data["ServiceResponse"].get("count", 0) == 1:
            users_list.append(User(**users[0]["User"]))
            break
        else:
            users_list.extend([User(**user["User"]) for user in users])
            if not data["ServiceResponse"].get("hasMoreRecords", False) in [True, "true"]:
                print(f"Found {len(users)} users on final page, no more records to fetch.")
                break
            jsonpayload["ServiceRequest"]["filters"]["Criteria"].append(
                {"field": "id", "operator": "GREATER", "value": data["ServiceResponse"]["lastId"]}
            )
            print(f"Found {len(users)} users on current page, continuing to next page...")
    return users_list


def _validate_list(param, expected_type, param_name):
    if param is not None and not all(isinstance(i, expected_type) for i in param):
        raise TypeError(f"{param_name} must be a list of {expected_type.__name__}s")


def update_user(
    auth: BasicAuth,
    user_id: Union[int, str],
    add_tag_ids: list[int] = None,
    add_tag_names: list[str] = None,
    add_role_ids: list[int] = None,
    add_role_names: list[str] = None,
    remove_tag_ids: list[int] = None,
    remove_tag_names: list[str] = None,
    remove_role_ids: list[int] = None,
    remove_role_names: list[str] = None,
) -> str:
    """
    Update a user by adding or removing tags and roles.

    :param auth: Authentication object
    :param user_id: The ID of the user to update
    :param add_tag_ids: List of tag IDs to add to the user
    :param add_tag_names: List of tag names to add to the user
    :param add_role_ids: List of role IDs to add to the user
    :param add_role_names: List of role names to add to the user
    :param remove_tag_ids: List of tag IDs to remove from the user
    :param remove_tag_names: List of tag names to remove from the user
    :param remove_role_ids: List of role IDs to remove from the user
    :param remove_role_names: List of role names to remove from the user
    :return: Response message indicating success or failure
    """

    # Check which parameters are provided
    if not any(
        [
            add_tag_ids,
            add_tag_names,
            add_role_ids,
            add_role_names,
            remove_tag_ids,
            remove_tag_names,
            remove_role_ids,
            remove_role_names,
        ]
    ):
        raise ValueError("At least one parameter must be provided to update the user.")

    # check that provided parameters are lists with the correct types inside:
    param_validations = [
        (add_tag_ids, int, "add_tag_ids"),
        (add_tag_names, str, "add_tag_names"),
        (add_role_ids, int, "add_role_ids"),
        (add_role_names, str, "add_role_names"),
        (remove_tag_ids, int, "remove_tag_ids"),
        (remove_tag_names, str, "remove_tag_names"),
        (remove_role_ids, int, "remove_role_ids"),
        (remove_role_names, str, "remove_role_names"),
    ]

    for param, expected_type, param_name in param_validations:
        _validate_list(param, expected_type, param_name)

    # Template the JSON payload
    jsonpayload = {
        "ServiceRequest": {
            "data": {
                "User": {
                    "scopeTags": {"add": {"TagData": []}, "remove": {"TagData": []}},
                    "roleList": {"add": {"RoleData": []}, "remove": {"RoleData": []}},
                }
            }
        }
    }

    # Add tags to the payload
    if add_tag_ids:
        jsonpayload["ServiceRequest"]["data"]["User"]["scopeTags"]["add"]["TagData"].extend(
            [{"id": tag_id} for tag_id in add_tag_ids]
        )
    if add_tag_names:
        jsonpayload["ServiceRequest"]["data"]["User"]["scopeTags"]["add"]["TagData"].extend(
            [{"name": tag_name} for tag_name in add_tag_names]
        )
    if remove_tag_ids:
        jsonpayload["ServiceRequest"]["data"]["User"]["scopeTags"]["remove"]["TagData"].extend(
            [{"id": tag_id} for tag_id in remove_tag_ids]
        )
    if remove_tag_names:
        jsonpayload["ServiceRequest"]["data"]["User"]["scopeTags"]["remove"]["TagData"].extend(
            [{"name": tag_name} for tag_name in remove_tag_names]
        )

    # Add roles to the payload
    if add_role_ids:
        jsonpayload["ServiceRequest"]["data"]["User"]["roleList"]["add"]["RoleData"].extend(
            [{"id": role_id} for role_id in add_role_ids]
        )
    if add_role_names:
        jsonpayload["ServiceRequest"]["data"]["User"]["roleList"]["add"]["RoleData"].extend(
            [{"name": role_name} for role_name in add_role_names]
        )
    if remove_role_ids:
        jsonpayload["ServiceRequest"]["data"]["User"]["roleList"]["remove"]["RoleData"].extend(
            [{"id": role_id} for role_id in remove_role_ids]
        )
    if remove_role_names:
        jsonpayload["ServiceRequest"]["data"]["User"]["roleList"]["remove"]["RoleData"].extend(
            [{"name": role_name} for role_name in remove_role_names]
        )

    # Make the API call
    response = call_api(
        auth=auth,
        module="admin",
        endpoint="update_user",
        jsonbody=jsonpayload,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        params={"placeholder": user_id},
    )

    data = response.json()
    if data.get("ServiceResponse", {}).get("responseErrorDetails"):
        error_message = data["ServiceResponse"]["responseErrorDetails"]["errorMessage"]
        raise Exception(f"Error updating user: {error_message}")
    if not "count" in data.get("ServiceResponse", {}):
        print("No count key in response. Assume failure.")
        return "Failure: No count key in response)."
    return data["ServiceResponse"]["responseCode"]
