"""
get_host_list_detections.py - contains the get_host_list_detections function for the Qualyspy package.

This endpoint is used to get a list of hosts and their QID detections.
"""

from typing import List, Union

from xmltodict import parse

from .data_classes.detection import Detection
from .data_classes.lists import BaseList
from .data_classes.hosts import VMDRHost
from ..base.call_api import call_api
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *

def get_hld(auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs)->List:
    """
    get_hld - get a list of hosts and their QID detections.

    Args:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        page_count (Union[int, "all"]): The number of pages to retrieve. Defaults to "all".
        **kwargs: Additional keyword arguments to pass to the API. See below.

    Keyword Args:
        ```
        action (Optional[str]) #The action to perform. Default is 'list'. WARNING: any value you pass is overwritten with 'list'. It is just recognized as valid for the sake of completeness.
        echo_request (Optional[bool]) #Whether to echo the request. Default is False. Ends up being passed to the API as 0 or 1. WARNING: this SDK does not include this field in the data.
        show_asset_id (Optional[bool]) #Whether to show the asset IDs. Default is 'False'. ends up being passed to API as 0 or 1.
        include_vuln_type (Optional[Literal["confirmed", "potential"]]) #The type of vulnerability to include. If not specified, both types are included.
        
        DETECTION FILTERS:
        show_results (Optional[bool]) #Whether to show the results. Default is True. Ends up being passed to the API as 0 or 1.
        show_reopened_info (Optional[bool]) #Whether to show why reopened vulns were reopened. Default is False. Ends up being passed to the API as 0 or 1.
        arf_kernel_filter (Optional[Literal[0,1,2,3,4]]) #Specify vulns for Linux kernels. 0 = don't filter, 1 = exclude kernel vulns that are not exploitable, 2 = only include kernel related vulns that are not exploitable, 3 = only include exploitable kernel vulns, 4 = only include kernel vulns. If specified, results are in a host's <AFFECT_RUNNING_KERNEL> tag.
        arf_service_filter (Optional[Literal[0,1,2,3,4]]) #Specify vulns found on running or nonrunning ports/services. 0 = don't filter, 1 = exclude service related vulns that are exploitable, 2 = only include service vulns that are exploitable, 3 = only include service vulns that are not exploitable, 4 = only include service vulns. If specified, results are in a host's <AFFECT_RUNNING_SERVICE> tag.
        arf_config_filter (Optional[Literal[0,1,2,3,4]]) #Specify vulns that can be vulnerable based on host config. 0 = don't filter, 1 = exclude vulns that are exploitable due to host config, 2 = only include config related vulns that are exploitable, 3 = only include config related vulns that are not exploitable, 4 = only include config related vulns. If specified, results are in a host's <AFFECT_EXPLOITABLE_CONFIG> tag.
        active_kernels_only (Optional[Literal[0,1,2,3]]) #Specify vulns related to running or non-running kernels. 0 = don't filter, 1 = exclude non-running kernels, 2 = only include vulns on non-running kernels, 3 = only include vulns with running kernels. If specified, results are in a host's <AFFECT_RUNNING_KERNEL> tag.
        output_format (Optional[Literal["XML", "CSV"]]) #The format of the output. Default is 'XML'. WARNING: this SDK will overwrite any value you pass with 'XML'. It is just recognized as valid for the sake of completeness.
        supress_duplicated_data_from_csv (Optional[bool]) #Whether to suppress duplicated data from CSV. Default is False. Ends up being passed to the API as 0 or 1. WARNING: this SDK does not include this field in the data.
        truncation_limit (Optional[int]) #The truncation limit for a page. Default is 1000.
        max_days_since_detection_updated (Optional[int]) #The maximum number of days since the detection was last updated. For detections that have never changed, the value is applied to the last detection date.
        detection_updated_since (Optional[str]) #The date and time since the detection was updated.
        detection_updated_before (Optional[str]) #The date and time before the detection was updated.
        detection_processed_before (Optional[str]) #The date and time before the detection was processed.
        detection_processed_after (Optional[str]) #The date and time after the detection was processed.
        detection_last_tested_since (Optional[str]) #The date and time since the detection was last tested.
        detection_last_tested_since_days (Optional[int]) #The number of days since the detection was last tested.
        detection_last_tested_before (Optional[str]) #The date and time before the detection was last tested.
        detection_last_tested_before_days (Optional[int]) #The number of days before the detection was last tested.
        include_ignored (Optional[bool]) #Whether to include ignored detections. Default is False. Ends up being passed to the API as 0 or 1.
        include_disabled (Optional[bool]) #Whether to include disabled detections. Default is False. Ends up being passed to the API as 0 or 1.

        HOST FILTERS:
        ids (Optional[str]) #A comma-separated string of host IDs to include.
        id_min (Optional[Union[int,str]]) #The minimum host ID to include.
        id_max (Optional[Union[int,str]]) #The maximum host ID to include.
        ips (Optional[str]) #The IP address of the host to include. Can be a comma-separated string, and also supports ranges with a hyphen: 10.0.0.0-10.0.0.255.
        ipv6 (Optional[str]) #The IPv6 address of the host to include. Can be a comma-separated string. Does not support ranges.
        ag_ids (Optional[str]) #Show only hosts belonging to the specified asset group IDs. Can be a comma-separated string, and also supports ranges with a hyphen: 1-5.
        ag_titles (Optional[str]) #Show only hosts belonging to the specified asset group titles. Can be a comma-separated string.
        TODO: add more filters.

        ```


    Returns:
        List: A list of VMDRHost objects, with their DETECTIONS attribute populated.
    """