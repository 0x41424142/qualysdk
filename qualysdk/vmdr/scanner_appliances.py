"""
scanner_appliances.py - Contains functions to interact with Scanner Appliances in VMDR.
"""

from ..exceptions import *
from ..base import call_api, xml_parser
from .data_classes import ScannerAppliance
from ..base.base_list import BaseList
from ..auth import BasicAuth


def get_scanner_list(auth: BasicAuth, **kwargs) -> BaseList[ScannerAppliance]:
    """
    Get a list of Scanner Appliances in VMDR, filtered by kwargs.

    Parameters:
        auth (BasicAuth): The BasicAuth context to use.
        **kwargs: Additional keyword arguments to filter the Scanner Appliances by.

    :Kwargs:
        action (str): The action to filter by. NOTE: the SDK force-sets this to "list". It is just included for completeness.
        echo_request (bool): Whether to echo the request. NOTE: the SDK force-sets this to False. It is just included for completeness.
        output_mode (Literal['brief', 'full']): The output mode. Defaults to 'brief'.
        scan_detail (bool): Whether to include details on currently running scans. Defaults to False. Details include ID, title, scan_ref, type, and date.
        show_tags (bool): Whether to include tags. Defaults to False.
        include_cloud_info (bool): Whether to include cloud information. Defaults to False. Requires output_mode='full'. If set, output includes cloud data for appliances in a cloud platform.
        busy (bool): Whether to include busy appliances. Defaults to True.
        scan_ref (str): The scan reference to filter by. Output will only show scanners that are running this scan.
        name (str): The name to filter by.
        ids (Union[str, int]): The IDs to filter by. Can be a single ID or a comma-separated string of IDs.
        include_license_info (bool): Whether to include license usage info. Output is under ['LICENSE_INFO']. NOTE: the SDK force-sets this to False. It is just included for completeness.
        type (Literal['physical', 'virtual', 'containerized', 'offline']): The type of scanner to filter by. Appears when output_mode='full'.
        platform_provider (Literal['ec2', 'ec2_compat', 'gce', 'azure', 'vCenter']): The cloud platform provider to filter by.

    Returns:
        BaseList[ScannerAppliance]: A list of Scanner Appliances.
    """

    result = BaseList()

    # set the action and echo_request:
    kwargs["action"] = "list"
    kwargs["echo_request"] = False
    kwargs["include_license_info"] = False

    # call the API:
    resp = call_api(
        auth=auth,
        module="vmdr",
        endpoint="get_scanner_list",
        params=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    data = xml_parser(resp.text)["APPLIANCE_LIST_OUTPUT"]["RESPONSE"]

    if "APPLIANCE_LIST" not in data.keys():
        print("No data in response")
        return result

    # If there is just one dict, convert it to a list of one dict
    if isinstance(data["APPLIANCE_LIST"]["APPLIANCE"], dict):
        data = [data]

    for item in data["APPLIANCE_LIST"]["APPLIANCE"]:
        result.append(ScannerAppliance(**item))

    return result
