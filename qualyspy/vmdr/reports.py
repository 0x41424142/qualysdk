"""
reports.py - contains functions to work with reports in VMDR.
"""

from typing import *

from requests.models import Response

from .data_classes import VMDRReport
from ..auth import BasicAuth
from ..base import call_api
from ..base import xml_parser
from .data_classes.lists import BaseList
from ..exceptions.Exceptions import *


def manage_reports(
    auth: BasicAuth,
    action: Literal["list", "launch", "cancel", "fetch", "delete"],
    **kwargs,
) -> Response:
    """
    Backend function to manage reports in Qualys VMDR.

    Parameters:
        ```auth```: ```Required[BasicAuth]``` - The BasicAuth object.
        ```action```: ```Literal["list", "launch", "cancel", "fetch", "delete"]``` - The action to take.

    Returns:
        ```Response``` - The response from the API.

    Kwargs:

    WHEN ```action=="list"```:
        ```id```: ```Optional[Union[int,str]]``` - A specific report ID to get.
        ```state```: ```Optional[str]``` - Filter output to reports in a specific state.
        ```user_login```: ```Optional[str]``` - Filter output to reports launched by a specific user.
        ```expires_before_datetime```: ```Optional[str]``` - Filter output to reports that will expire before this datetime. Formatted like: YYYY-MM-DD[THH:MM:SSZ]
        ```client_id```: ```Optional[Union[int,str]]``` - Filter output to reports for a specific client ID. ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!
        ```client_name```: ```Optional[str]``` - Filter output to reports for a specific client name. ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!
    """

    # Set specific kwargs
    kwargs["action"] = action
    kwargs["echo_request"] = False

    headers = {"X-Requested-With": "qualyspy SDK"}

    match action:
        case "list":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="get_report_list",
                params=kwargs,
                headers=headers,
            )
        case _:
            raise NotImplementedError(f"Action {action} is not implemented yet.")


def get_report_list(auth: BasicAuth, **kwargs) -> BaseList[VMDRReport]:
    """
    Get a list of reports in VMDR, according to kwargs.

    Parameters:
        ```auth```: ```Required[BasicAuth]``` - The BasicAuth object.

    Kwargs:
        ```id```: ```Optional[Union[int,str]]``` - A specific report ID to get.
        ```state```: ```Optional[str]``` - Filter output to reports in a specific state.
        ```user_login```: ```Optional[str]``` - Filter output to reports launched by a specific user.
        ```expires_before_datetime```: ```Optional[str]``` - Filter output to reports that will expire before this datetime. Formatted like: YYYY-MM-DD[THH:MM:SSZ]
        ```client_id```: ```Optional[Union[int,str]]``` - Filter output to reports for a specific client ID. ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!
        ```client_name```: ```Optional[str]``` - Filter output to reports for a specific client name. ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!

    Returns:
        ```BaseList[VMDRReport]``` - A list of VMDRReport objects.
    """

    response = manage_reports(auth, action="list", **kwargs)

    data = xml_parser(response.text)

    reports = data["REPORT_LIST_OUTPUT"]["RESPONSE"]["REPORT_LIST"]["REPORT"]

    bl = BaseList()

    # Check if there are multiple reports or just one
    if isinstance(reports, dict):
        reports = [reports]

    for report in reports:
        bl.append(VMDRReport.from_dict(report))

    return bl
