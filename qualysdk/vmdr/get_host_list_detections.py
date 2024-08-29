"""
get_host_list_detections.py - contains the get_host_list_detections function for the qualysdk package.

This endpoint is used to get a list of hosts and their QID detections. The function is multithreaded and uses the hld_backend function to pull the data.
"""

from typing import Union
from threading import Thread

from .base.helpers import create_id_queue, thread_worker, prepare_args
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *


def get_hld(
    auth: BasicAuth,
    chunk_size: int = 3000,
    threads: int = 5,
    page_count: Union[int, "all"] = "all",
    chunk_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList:
    """
    get_hld - get a list of hosts and their QID detections using multiple threads.

    Params:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        chunk_size (int): The size of each chunk. Defaults to 3000.
        threads (int): The number of threads to use. Defaults to 5.
        page_count (Union[int, "all"]): The number of pages to retrieve. Defaults to "all".
        chunk_count (Union[int, "all"]): The number of chunks to retrieve. Defaults to "all".
        **kwargs: Additional keyword arguments to pass to the API.

    Kwargs:

        action (Optional[str]) #The action to perform. Default is 'list'. WARNING: any value you pass is overwritten with 'list'. It is just recognized as valid for the sake of completeness.
        echo_request (Optional[bool]) #Whether to echo the request. Default is False. Ends up being passed to the API as 0 or 1. WARNING: this SDK does not include this field in the data.
        show_asset_id (Optional[bool]) #Whether to show the asset IDs. Default is 'False'. ends up being passed to API as 0 or 1.
        include_vuln_type (Optional[Literal["confirmed", "potential"]]) #The type of vulnerability to include. If not specified, both types are included.

        DETECTION FILTERS:
        show_results (Optional[bool]) #Whether to show the results. Default is True. Ends up being passed to the API as 0 or 1. WARNING: this SDK overwrites any value you pass with '1'. It is just recognized as valid for the sake of completeness.
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
        network_ids (Optional[str]) #Show only hosts belonging to the specified network IDs. Can be a comma-separated string.
        network_names (Optional[str]) #displays the name of the network corresponding to the network ID.
        vm_scan_since (Optional[str]) #The date and time since the last VM scan. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        no_vm_scan_since (Optional[str]) #The date and time since the last VM scan. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        max_days_since_last_vm_scan (Optional[int]) #The maximum number of days since the last VM scan.
        vm_processed_before (Optional[str]) #The date and time before the VM scan was processed. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        vm_processed_after (Optional[str]) #The date and time after the VM scan was processed. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        vm_scan_date_before (Optional[str]) #The date and time before the VM scan. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        vm_scan_date_after (Optional[str]) #The date and time after the VM scan. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        vm_auth_scan_date_before (Optional[str]) #The date and time before the VM authenticated scan. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        vm_auth_scan_date_after (Optional[str]) #The date and time after the VM authenticated scan. Format is 'YYYY-MM-DD[THH:MM:SS]'.
        status (Optional[Literal["New", "Active", "Fixed", "Re-Opened"]]) #The status of the detection.
        compliance_enabled (Optional[bool]) #Whether compliance is enabled. Default is False. Ends up being passed to the API as 0 or 1.
        os_pattern (Optional[str]) #PCRE Regex to match operating systems.

        QID FILTERS:
        qids (Optional[str]) #A comma-separated string of QIDs to include.
        severities (Optional[str]) #A comma-separated string of severities to include. Can also be a hyphenated range, i.e. '2-4'.
        filter_superseded_qids (Optional[bool]) #Whether to filter superseded QIDs. Default is False. Ends up being passed to the API as 0 or 1.
        include_search_list_titles (Optional[str]) #A comma-separated string of search list titles to include.
        exclude_search_list_titles (Optional[str]) #A comma-separated string of search list titles to exclude.
        include_search_list_ids (Optional[str]) #A comma-separated string of search list IDs to include.
        exclude_search_list_ids (Optional[str]) #A comma-separated string of search list IDs to exclude.

        ASSET TAG FILTERS:
        use_tags (Optional[bool]) #Whether to use tags. Default is False. Ends up being passed to the API as 0 or 1.
        tag_set_by (Optional[Literal['id','name']]) #When filtering on tags, whether to filter by tag ID or tag name.
        tag_include_selector (Optional[Literal['any','all']]) #When filtering on tags, choose if asset has to match any or all tags specified.
        tag_exclude_selector (Optional[Literal['any','all']]) #When filtering on tags, choose if asset has to match any or all tags specified.
        tag_set_include (Optional[str]) #A comma-separated string of tag IDs or names to include.
        tag_set_exclude (Optional[str]) #A comma-separated string of tag IDs or names to exclude.
        show_tags (Optional[bool]) #Whether to show tags. Default is False. Ends up being passed to the API as 0 or 1.

        QDS FILTERS:
        show_qds (Optional[bool]) #Whether to show QDS. Default is False. Ends up being passed to the API as 0 or 1.
        qds_min (Optional[int]) #The minimum QDS to include.
        qds_max (Optional[int]) #The maximum QDS to include.
        show_qds_factors (Optional[bool]) #Whether to show QDS factors. Default is False. Ends up being passed to the API as 0 or 1.

        EC2/AZURE METADATA FILTERS:
        host_metadata (Optional[Literal['all,'ec2', 'azure']]) #The type of metadata to include. Default is 'all'.
        host_metadata_fields (Optional[str]) #A comma-separated string of metadata fields to include. Use carefully.
        show_cloud_tags (Optional[bool]) #Whether to show cloud tags. Default is False. Ends up being passed to the API as 0 or 1.
        cloud_tag_fields (Optional[str]) #A comma-separated string of cloud tag fields to include. Use carefully.

    Returns:
        BaseList: A list of VMDRHost objects, with their DETECTIONS attribute populated.
    """

    prepare_args(
        auth=auth,
        chunk_size=chunk_size,
        threads=threads,
        page_count=page_count,
        chunk_count=chunk_count,
        ids=kwargs.get("ids"),
    )

    id_queue = create_id_queue(auth, chunk_size=chunk_size, ids=kwargs.get("ids", None))
    print(f"Starting get_hld with {threads} {'threads.' if threads > 1 else 'thread.'}")

    threads_list = []

    responses = BaseList()

    for i in range(threads):
        thread = Thread(
            target=thread_worker,
            args=(
                auth,
                id_queue,
                responses,
                page_count,
                chunk_count,
                "get_hld",
                kwargs,
            ),
        )
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    print("All threads have completed. Returning responses.")
    return responses
