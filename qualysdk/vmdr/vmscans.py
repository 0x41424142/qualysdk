"""
vmscans.py - Contains functions to interact with the /api/2.0/fo/scan/ API endpoint,
with the 'action' parameter controlling what is done with the scan(s).
"""

from datetime import datetime
from typing import Union, Literal
from io import StringIO

from pandas import read_json, DataFrame

from ..base import call_api, xml_parser
from ..base.base_list import BaseList
from .data_classes.vmscan import VMScan
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *


def get_scan_list(auth: BasicAuth, **kwargs) -> BaseList[VMScan]:
    """
    Pull a list of scans in the Qualys subscription.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.

    Keyword Args:
        SCAN LIST FILTERS:
        scan_ref (str): Scan reference ID. Formatted like scan/1234567890123456, compliance/1234567890123456, or qscap/1234567890123456.
        state (Union[Literal["Running", "Paused", "Canceled", "Finished", "Error", "Queued", "Loading"], BaseList[str]): State of the scan. Multiple states can be specified as a comma-separated string. Can also pass a BaseList of strings.
        processed (bool): Whether the scan has been processed. Defaults to None.
        type (Literal["On-Demand", "API", "Scheduled"]): Type of scan. Defaults to None.
        target (Union[str, BaseList[str]]) Target IP(s) of the scan. Can be a single IP string, or a BaseList of strings. Calls API with the correct format - a comma separated string. If an IP range/network obj is passed, it is formatted as 1.2.3.4-5.6.7.8.
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
        headers={"X-Requested-With": "qualysdk SDK"},
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


def launch_scan(auth: BasicAuth, **kwargs) -> VMScan:
    """
    Create a new VMDR scan and launch, or call
    a pre-existing VMDR scan on supplied target (IP, asset group IDs, etc.).

    Keyword args:
        action (Literal["launch"]): The action to perform. Defaults to "launch". WARNING: the SDK will force-set this to "launch".
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: the SDK will force-set this to False.
        runtime_http_header (str): The value the scanner will put in the Qualys-Scan header. Defaults to None. Used to "drop defenses".
        scan_title (str): The title of the scan. Defaults to None.
        option_id (int): The option profile ID. Required if option_title not specified.
        option_title (str): The option profile title. Required if option_id not specified.

        SCANNER APPLIANCE OPTIONS:
            iscanner_id (int): The internal scanner ID. Defaults to None.
            iscanner_name (str): The internal scanner name. Defaults to None.
            ec2_instance_ids (str): The EC2 instance IDs of external scanners. Defaults to None.

        priority (int, 0-10): The priority of the scan. Defaults to None.

        ASSET IPs/GROUP OPTIONS:
            ip (Union[str, BaseList[str]]): The IP(s) to scan. Defaults to None.
            asset_group_ids (Union[str, BaseList[str], int, BaseList[int]]): The asset group IDs to scan. Defaults to None.
            asset_groups (Union[str, BaseList[str]]): The asset group titles to scan. Defaults to None.
            exclude_ip_per_scan (Union[str, BaseList[str]]): The IPs to exclude from the scan. Defaults to None. Only valid when target_from=assets.
            fqdn (Union[str, BaseList[str]]): The FQDN(s) to scan. Defaults to None.
            default_scanner (bool): Whether to use the default scanner. Defaults to None.
            scanners_in_ag (bool): Whether to use scanners in the asset group. Defaults to None.
            target_from (Literal["assets", "tags"]): The target source. Defaults to "assets".
            use_ip_nt_range_tags_include (bool): Whether to use IP/NT range tags include. Defaults to None.
            use_ip_nt_range_tags_exclude (bool): Whether to use IP/NT range tags exclude. Defaults to None.
            use_ip_nt_range_tags (bool): Whether to use IP/NT range tags. Defaults to None.
            tag_include_selector (Literal["any", "all"]): The tag include selector. Defaults to any.
            tag_exclude_selector (Literal["any", "all"]): The tag exclude selector. Defaults to any.
            tag_set_by (Literal["id", "name"]) Whether to search for tags by ID or name. Defaults to id.
            tag_set_exclude (str): Comma-separated string of tag IDs or names, according to tag_set_by. Defaults to None.
            tag_set_include (str): Comma-separated string of tag IDs or names, according to tag_set_by. Defaults to None.

        ip_network_id (int): The IP network ID. Defaults to None. Must be enabled in the Qualys subscription.
        client_id (int): The client ID. Defaults to None. Only available for consultant subscriptions.
        client_name (str): The client name. Defaults to None. Only available for consultant subscriptions.
        connector_name (str): The connector name for EC2 scans. Defaults to None. Required for EC2 scans.
        ec2_endpoint (str): The EC2 region code or VPC ID zone. Defaults to None. Required for EC2 scans.

        EXAMPLE:
        ```
        # Launch a scan on a single IP:
        result = launch_scan(auth, ip="1.2.3.4", scan_title="My Scan", priority=5, option_id=123456)
        >>> "New vm scan launched with REF: scan/1234567890123456"
        result
        >>> ("New vm scan launched", "scan/1234567890123456")
        ```

    Returns:
        VMSan: VMScan dataclass object containing the scan details.
    """

    # Set the required kwargs:
    kwargs["action"] = "launch"
    kwargs["echo_request"] = False

    # Convert any BaseList objects to comma-separated strings:
    for key in kwargs:
        if isinstance(kwargs[key], BaseList):
            kwargs[key] = ",".join(kwargs[key])

    # Make the request:
    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="launch_scan",
        payload=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    # Parse the response:
    result = xml_parser(response.text)

    # Check for empty results:
    if not result:
        print("No scan launched.")
        return None

    # Check for scan details in simple_return:

    data = result["SIMPLE_RETURN"]["RESPONSE"]

    if "CODE" in data.keys():
        raise QualysAPIError(data["TEXT"])

    items_list = data["ITEM_LIST"]["ITEM"]
    # if items_list is a dict, put it into a list:
    if isinstance(items_list, dict):
        items_list = [items_list]

    scan_ref = ""
    for item in items_list:
        # Check if the KEY key's value is REFERENCE
        if item["KEY"] == "REFERENCE":
            scan_ref = item["VALUE"]

    print(f'{data["TEXT"]} with REF: {scan_ref}')

    # Return a VMScan object with the scan details:
    return get_scan_list(auth, scan_ref=scan_ref)[0]


def manage_scan(
    auth: BasicAuth,
    scan_ref: str,
    action: Literal["pause", "cancel", "resume", "fetch", "delete"],
    **kwargs,
) -> Union[str, DataFrame]:
    """
    Perform an action on a VMDR scan.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.
        scan_ref (str): The scan reference ID. Formatted like scan/1234567890123456.
        action (Literal["pause", "resume", "cancel", "fetch", "delete"]): The action to perform on the scan.

    :Keyword Args:
    NOTE: ALL KWARGS ARE FOR action="fetch" ONLY

        ips (str): The IPs to fetch. Defaults to None.
        mode (Literal["brief", "extended"]): The fetch mode. Defaults to "brief". If you specify nothing, or a non-existent mode, the SDK will default to "brief".
        client_id (int): The client ID. Defaults to None. Only available for consultant subscriptions.
        client_name (str): The client name. Defaults to None. Only available for consultant subscriptions.

    Returns:
        Union[str, pd.DataFrame]: Either a text response or a pandas DF.
    """

    # Check for valid action:
    if action not in ["pause", "resume", "cancel", "fetch", "delete"]:
        raise ValueError(
            f"Invalid action {action}. Must be one of 'pause', 'resume', 'cancel', or 'fetch'."
        )

    # Base payload for all actions:
    payload = {
        "scan_ref": scan_ref,
        "action": action,
        "echo_request": False,
    }

    # If action is "fetch", add the kwargs to the payload:
    if action == "fetch":
        match kwargs.get("mode"):
            case "brief":
                payload["output_format"] = "json"
            case "extended":
                payload["output_format"] = "json_extended"
            case _:
                payload["output_format"] = "json"

        payload.update(kwargs)

    # Make the request:
    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint=f"{action}_scan",  # Nifty way to dynamically get required params/payload for each action
        payload=payload,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    # Parse the response:

    # Special case for fetch.
    if action != "fetch":
        result = xml_parser(response.text)

        # Check for empty results:
        if not result:
            print("No scan paused.")
            return None

        data = result["SIMPLE_RETURN"]["RESPONSE"]

        if "CODE" in data.keys():
            raise QualysAPIError(data["TEXT"])

        return data["TEXT"]

    else:
        # Make sure that the response is JSON:
        if response.headers["Content-Type"] not in [
            "application/json",
            "application/json; charset=UTF-8",
            "text/html; charset=UTF-8",
        ]:
            raise QualysAPIError(
                xml_parser(response.text)["SIMPLE_RETURN"]["RESPONSE"]["TEXT"]
            )

        # Parse the JSON response:
        result = read_json(StringIO(response.text))

        if result.empty:
            print("No scan found.")
            return None

        return result


def pause_scan(auth: BasicAuth, scan_ref: str) -> str:
    """
    Pause a VMDR scan.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.
        scan_ref (str): The scan reference ID. Formatted like scan/1234567890123456.

    Returns:
        str: The text response from Qualys
    """

    # Call manage_scan with the action set to "pause":
    return manage_scan(auth=auth, scan_ref=scan_ref, action="pause")


def resume_scan(auth: BasicAuth, scan_ref: str) -> str:
    """
    Resume a VMDR scan.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.
        scan_ref (str): The scan reference ID. Formatted like scan/1234567890123456.

    Returns:
        str: The text response  from Qualys
    """

    # Call manage_scan with the action set to "resume":
    return manage_scan(auth=auth, scan_ref=scan_ref, action="resume")


def cancel_scan(auth: BasicAuth, scan_ref: str) -> str:
    """
    Cancel a VMDR scan.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.
        scan_ref (str): The scan reference ID. Formatted like scan/1234567890123456.

    Returns:
        str: The text response from Qualys
    """

    # Call manage_scan with the action set to "cancel":
    return manage_scan(auth=auth, scan_ref=scan_ref, action="cancel")


def delete_scan(auth: BasicAuth, scan_ref: str) -> str:
    """
    Delete a VMDR scan.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.
        scan_ref (str): The scan reference ID. Formatted like scan/1234567890123456.

    Returns:
        str: The text response from Qualys
    """

    # Call manage_scan with the action set to "delete":
    return manage_scan(auth=auth, scan_ref=scan_ref, action="delete")


def fetch_scan(auth: BasicAuth, scan_ref: str, **kwargs) -> DataFrame:
    """
    Fetch VMDR scan results.

    Args:
        auth (BasicAuth): Qualys BasicAuth object.
        scan_ref (str): The scan reference ID. Formatted like scan/1234567890123456.

    :kwargs:
        ips (str): The IPs to fetch. Defaults to None.
        mode (Literal["brief", "extended"]): The fetch mode. Defaults to "brief". If you specify nothing, or a non-existent mode, the SDK will default to "brief".
        client_id (int): The client ID. Defaults to None. Only available for consultant subscriptions.
        client_name (str): The client name. Defaults to None. Only available for consultant subscriptions.

    Returns:
        pd.DataFrame: The scan results in a pandas DataFrame.
    """

    # Call manage_scan with the action set to "fetch":
    return manage_scan(auth=auth, scan_ref=scan_ref, action="fetch", **kwargs)
