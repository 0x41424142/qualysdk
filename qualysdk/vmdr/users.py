"""
users.py - contains functions to interact with VMDR user management APIs.
"""

from typing import List, Union, Literal

from ..auth import BasicAuth
from ..base import xml_parser, call_api
from ..base.base_list import BaseList
from .data_classes.user import User
from ..exceptions import *


def get_user_list(auth: BasicAuth, **kwargs) -> BaseList[User]:
    """
    Get a list of users in the subscription.

    Args:
        auth (BasicAuth): The authentication object.

    :Kwargs:
        external_id__contains (str): Filter by external ID containing this string.
        external_id_assigned (bool): Filter by external ID assigned.

    Returns:
        BaseList[User]: BaseList of User objects.
    """

    response = call_api(
        auth=auth,
        endpoint="get_user_list",
        module="vmdr",
        params=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    bl = BaseList()

    if response.status_code != 200:
        raise QualysAPIError(response.text)

    user_list = xml_parser(response.text)

    if "ERROR" in user_list["USER_LIST_OUTPUT"].keys():
        raise QualysAPIError(user_list["USER_LIST_OUTPUT"]["ERROR"]["#text"])

    if "USER" not in user_list["USER_LIST_OUTPUT"]["USER_LIST"].keys():
        print("No users found.")
        return bl

    # Check for single user
    if isinstance(user_list["USER_LIST_OUTPUT"]["USER_LIST"]["USER"], dict):
        user_list["USER_LIST_OUTPUT"]["USER_LIST"]["USER"] = [
            user_list["USER_LIST_OUTPUT"]["USER_LIST"]["USER"]
        ]

    for user in user_list["USER_LIST_OUTPUT"]["USER_LIST"]["USER"]:
        bl.append(User(**user))

    return bl


def add_user(
    auth: BasicAuth,
    user_role: Literal[
        "manager", "unit_manager", "scanner", "reader", "contact", "administrator"
    ],
    business_unit: Union[Literal["Unassigned"], str],
    first_name: str,
    last_name: str,
    title: str,
    phone: str,
    email: str,
    address1: str,
    city: str,
    country: str,
    state: str,
    **kwargs,
) -> str:
    """
    Adds a user to the subscription.

    Args:
        auth (BasicAuth): The authentication object.
        user_role (Literal["manager", "unit_manager", "scanner", "reader", "contact", "administrator"]): The role of the user.
        business_unit (Union[Literal["Unassigned"], str]): The business unit of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        title (str): The title of the user.
        phone (str): The phone number of the user.

        email (str): The email of the user.
        address1 (str): The address of the user.
        city (str): The city of the user.
        country (str): The country of the user.
        state (str): The state of the user.

    :Kwargs:
        send_email (bool): Send an email to the user about their activation. True by default. If False, output will contain the username and password.
        asset_groups (str): Comma-separated string of asset group IDs.
        fax (str): The fax number of the user. Because 21st century...
        address2 (str): The second line of the address.
        zip_code (str): The zip code.
        external_id (str): The external ID of the user.

    Returns:
        str: The message from Qualys. If send_email is False, the output will contain the username and password.
    """

    params = {
        "action": "add",
        "user_role": user_role,
        "business_unit": business_unit,
        "first_name": first_name,
        "last_name": last_name,
        "title": title,
        "phone": phone,
        "email": email,
        "address1": address1,
        "city": city,
        "country": country,
        "state": state,
    }

    params.update(kwargs)

    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="add_user",
        params=params,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    if response.status_code != 200:
        raise QualysAPIError(response.text)

    result = xml_parser(response.text)

    if result["USER_OUTPUT"]["RETURN"]["@status"] == "FAILED":
        raise QualysAPIError(result["USER_OUTPUT"]["RETURN"]["MESSAGE"])

    if kwargs.get("send_email") == False:
        return f"User created. User:Pass is: {result['USER_OUTPUT']['USER']['USER_LOGIN']}:{result['USER_OUTPUT']['USER']['PASSWORD']}"

    else:
        return result["USER_OUTPUT"]["RETURN"]["MESSAGE"]


def edit_user(auth: BasicAuth, login: str, **kwargs) -> str:
    """
    Change details of a pre-existing user in Qualys.
    NOTE: To clear a field, specify it with an empty string in the kwargs.

    Args:
        auth (BasicAuth): The authentication object.
        login (str): The login of the user to edit.

    :Kwargs:
        asset_groups (str): Comma-separated string of asset group IDs.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        title (str): The title of the user.
        phone (str): The phone number of the user.
        fax (str): The fax number of the user. Because 21st century...
        email (str): The email of the user.
        address1 (str): The address of the user.
        address2 (str): The second line of the address.
        city (str): The city of the user.
        country (str): The country of the user.
        state (str): The state of the user.
        zip_code (str): The zip code.
        external_id (str): The external ID of the user.

    Returns:
        str: The message from Qualys.
    """

    params = {"action": "edit", "login": login}
    params.update(kwargs)

    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="edit_user",
        params=params,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    if response.status_code != 200:
        raise QualysAPIError(response.text)

    result = xml_parser(response.text)

    if result["USER_OUTPUT"]["RETURN"]["@status"] == "FAILED":
        raise QualysAPIError(result["USER_OUTPUT"]["RETURN"]["MESSAGE"])

    return result["USER_OUTPUT"]["RETURN"]["MESSAGE"]
