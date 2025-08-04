"""
Administration RBAC (Role-Based Access Control) APIs

These APIs allow for the management of user roles, tags and permissions within the Qualys platform.
"""

from typing import Union, overload, Literal

from .data_classes.User import User
from ..auth import BasicAuth
from ..base.base_list import BaseList
from ..base.call_api import call_api

_UserIdOperator = [
    "EQUALS",
    "GREATER",
    "LESSER"
]

@overload
def get_user_details(auth: BasicAuth, user_id: Union[int, str]) -> User: ...

@overload
def get_user_details(auth: BasicAuth, user_id: Union[list[int], list[str]]) -> BaseList[User]: ...

def get_user_details(auth: BasicAuth, user_id: Union[int, str, list[int], list[str]]) -> Union[User, BaseList[User]]:
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
    elif isinstance(user_id, (BaseList, list)) and all(isinstance(uid, (int, str)) for uid in user_id):
        # list of user IDs
        users.extend(user_id)
    else:
        raise TypeError("user_id must be an int, str, or list of ints/strs")

    for uid in user_id:
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
        raise ValueError("At least one search criterion must be provided: user_id, username, or role_name.")
    
    jsonpayload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": []
            }

        }
    }

    if user_id is not None:
        #user_id can be only be a single int or str
        if not isinstance(user_id, (int, str)):
            raise TypeError("user_id must be an int or str")
        if user_id_operator not in _UserIdOperator:
            raise ValueError(f"user_id_operator must be one of {_UserIdOperator}")
        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append({
            "field": "id",
            "operator": user_id_operator,
            "value": user_id
        })

    if username is not None:
        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append({
            "field": "username",
            "operator": "EQUALS",
            "value": username,
        })

    if role_name is not None:
        jsonpayload["ServiceRequest"]["filters"]["Criteria"].append({
            "field": "roleName",
            "operator": "EQUALS",
            "value": role_name
        })

    #start pagination
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
            jsonpayload["ServiceRequest"]["filters"]["Criteria"].append({
                "field": "id",
                "operator": "GREATER",
                "value": data["ServiceResponse"]["lastId"]
            })
            print(f"Found {len(users)} users on current page, continuing to next page...")
    return users_list
