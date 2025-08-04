"""
Administration RBAC (Role-Based Access Control) APIs

These APIs allow for the management of user roles, tags and permissions within the Qualys platform.
"""

from typing import Union, overload

from .data_classes.User import User
from ..auth import BasicAuth
from ..base.base_list import BaseList
from ..base.call_api import call_api

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
            endpoint="get_user_id",
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
