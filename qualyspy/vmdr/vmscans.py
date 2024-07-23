"""
vmscans.py - Contains functions to interact with the /api/2.0/fo/scan/ API endpoint,
with the 'action' parameter controlling what is done with the scan(s).
"""

from datetime import datetime

from qualyspy.base import call_api, xml_parser
from .data_classes.lists.base_list import BaseList
from .data_classes.vmscan import VMScan
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *


def get_scan_list(auth: BasicAuth, **kwargs) -> BaseList[VMScan]:
    """
    Pull a list of scans in the Qualys subscription.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.

    Keyword Args:
        ```
        SCAN LIST FILTERS:
        scan_ref (str): Scan reference ID. Formatted like scan/1234567890123456, compliance/1234567890123456, or qscap/1234567890123456.
        state (Union[Literal["Running", "Paused", "Canceled", "Finished", "Error", "Queued", "Loading"], BaseList[str]): State of the scan. Multiple states can be specified as a comma-separated string. Can also pass a BaseList of strings.
        processed (bool): Whether the scan has been processed. Defaults to None.
        type (Literal["On-Demand", "API", "Scheduled"]): Type of scan. Defaults to None.
        target (Union[str, BaseList[str], IPv4Address, IPv4Network, BaseList[IPv4Address], BaseList[IPv4Network]]) Target IP(s) of the scan. Can be a single IP string, an IP network, or a BaseList of IPs/networks. Calls API with the correct format - a comma separated string. If an IP range/network obj is passed, it is formatted as 1.2.3.4-5.6.7.8.
        user_login (str): Filter on owner of the scan. Defaults to None.
        launched_after_datetime (Union[strm datetime]): Filter on scans launched after a certain datetime. Can be a string or a datetime object. If a datetime object is passed, it is converted to a string.
        launched_before_datetime (Union[str, datetime]): Filter on scans launched before a certain datetime. Can be a string or a datetime object. If a datetime object is passed, it is converted to a string.
        scan_type (Literal["certview", "ec2certview"]): Filter on scan type. Defaults to None.
        client_id (Union[str, int]): Filter on client ID. Defaults to None.
        client_name (str): Filter on client name. Defaults to None.

        SHOW/HIDE FIELDS:
        show_ags (bool): Whether to show AGs. Defaults to None.
        show_op (bool): Whether to show OP. Defaults to None.
        show_status (bool): Whether to show status. Defaults to None.
        show_last (bool): Whether to show last scan. Defaults to None.
        ignore_target (bool): Whether to ignore the target. Defaults to None.
        ```

    Returns:
        BaseList: BaseList object containing the scan(s) in the Qualys subscription.
    """

    DT_FIELDS = ["launched_after_datetime", "launched_before_datetime"]

    # If user passes a datetime object, convert it to a string:
    for field in DT_FIELDS:
        if field in kwargs and isinstance(kwargs[field], datetime):
            kwargs[field] = kwargs[field].strftime("%Y-%m-%dT%H:%M:%S")

    # For all other kwargs, check if they are BaseList/list objects and convert them to a comma-separated string:
    for key in kwargs:
        if type(kwargs[key]) in [BaseList, list]:
            kwargs[key] = ",".join(kwargs[key])

    kwargs["action"] = "list"

    # Make the request:
    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="list_scans",
        params=kwargs,
        headers={"X-Requested-With": "qualyspy SDK"},
    )

    # Parse the response:
    result = xml_parser(response.text)

    # Check for empty results:
    if not result:
        print("No scans found.")
        return None

    data = result["SCAN_LIST_OUTPUT"]["RESPONSE"]

    if "SCAN_LIST" not in data or "SCAN" not in data["SCAN_LIST"]:
        print("No scans found.")
        return None

    # If data["SCAN_LIST"]["SCAN"] is a dict, convert it to a list of dicts:
    if isinstance(data["SCAN_LIST"]["SCAN"], dict):
        data["SCAN_LIST"]["SCAN"] = [data["SCAN_LIST"]["SCAN"]]

    # Convert the data to a BaseList of VMScan objects:
    scans = BaseList()

    for scan in data["SCAN_LIST"]["SCAN"]:
        scans.append(VMScan.from_dict(scan))

    return scans
