"""
get_host_list_detections.py - contains the get_host_list_detections function for the qualysdk package.

This endpoint is used to get a list of hosts and their QID detections. The function is multithreaded and uses the hld_backend function to pull the data.
"""

from typing import List, Union
from urllib.parse import parse_qs, urlparse
from threading import current_thread, Thread, Lock
from queue import Queue, Empty
from os import cpu_count

from .data_classes.hosts import VMDRHost, VMDRID
from ..base.base_list import BaseList
from ..base.call_api import call_api
from ..auth.token import BasicAuth
from .get_host_list import (
    get_host_list,
)  # Used to grab list of IDs for multithreaded detection list pulls
from ..exceptions.Exceptions import *
from ..base.xml_parser import xml_parser

LOCK = Lock()


def normalize_id_list(id_list):
    """
    normalize_id_list - formats the kwarg ids, if it is passed.

    Since the API accepts multiple values, either as comma-separated or as a range, this function
    normalizes the input to a list of integers that satisfy the API requirements.
    """
    id_list = id_list.split(",")
    new_list = []
    for i in id_list:
        if "-" in i:
            # if there is a hyphen, split by hyphen and create a range
            new_list.extend(range(int(i.split("-")[0]), int(i.split("-")[1]) + 1))
        else:
            # if there is no hyphen, just append the integer
            new_list.append(int(i))
    # Sort the list to ensure the range is correct
    new_list.sort()
    return new_list


def pull_id_set(auth: BasicAuth, ids: str = None) -> BaseList[VMDRID]:
    """
    pull_id_set - pull a set of host IDs from the VMDR API.

    Params:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        ids (str): A comma-separated string of host IDs to use. If specified, this will be used instead of pulling the full set.

    Returns:
        List[int]: A BaseList of host IDs as VMDRIDs.
    """
    if ids:
        return [
            str(i)
            for i in get_host_list(auth, details=None, truncation_limit=0, ids=ids)
        ]
    else:
        return [str(i) for i in get_host_list(auth, details=None, truncation_limit=0)]


def hld_backend(
    auth: BasicAuth,
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> List:
    """
    hld_backend - get a list of hosts and their QID detections.

    Params:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        page_count (Union[int, "all"]): The number of pages to retrieve. Defaults to "all".
        **kwargs: Additional keyword arguments to pass to the API. See below.

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
        List: A list of VMDRHost objects, with their DETECTIONS attribute populated.
    """

    # Set the kwargs
    kwargs["action"] = "list"
    kwargs["echo_request"] = 0
    kwargs["show_results"] = 1
    kwargs["output_format"] = "XML"

    responses = BaseList()
    pulled = 0

    while True:
        with LOCK:
            print(
                f"{current_thread().name} - Pulling page {pulled+1} for ids {kwargs.get('ids')}. KWARGS: {kwargs}"
            )

        # make the request:
        response = call_api(
            auth=auth,
            module="vmdr",
            endpoint="get_hld",
            params=kwargs,
            headers={"X-Requested-With": "qualysdk SDK"},
        )

        if response.status_code != 200:
            with LOCK:
                print(f"{current_thread().name} - No data returned on page {pulled}")
            pulled += 1
            if pulled != "all":
                if pulled == page_count:
                    print(f"{current_thread().name} - Pulled all pages.")
                    break
                else:
                    continue

        # cleaned = remove_problem_characters(response.text)
        xml = xml_parser(response.content)

        # check if there is no host list
        if "HOST_LIST" not in xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]:
            with LOCK:
                print(f"{current_thread().name} - No host list returned.")
        else:
            # check if ["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"] is a list of dictionaries
            # or just a dictionary. if it is just one, put it inside a list
            if not isinstance(
                xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"],
                list,
            ):
                xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"][
                    "HOST"
                ] = [
                    xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"][
                        "HOST"
                    ]
                ]

            for host in xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"][
                "HOST"
            ]:
                host_obj = VMDRHost.from_dict(host)
                responses.append(host_obj)

        pulled += 1
        if page_count != "all":
            if pulled == page_count:
                break

        if "WARNING" in xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]:
            if "URL" in xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]["WARNING"]:
                # get the id_min parameter from the URL to pass into kwargs:
                params = parse_qs(
                    urlparse(
                        xml["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"]["WARNING"][
                            "URL"
                        ]
                    ).query
                )
                with LOCK:
                    print(
                        f"{current_thread().name} - Pagination detected. Pulling next page with id_min: {params['id_min'][0]}"
                    )
                kwargs["id_min"] = params["id_min"][0]

            else:
                break
        else:
            break

    return responses


def create_id_queue(
    auth: BasicAuth, chunk_size: int = 100, ids: str = None
) -> BaseList:
    """
    create_id_queue - create a queue of host IDs to pull. the queue contains chunks (lists) of chunk_size
    length with host IDs.

    Params:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        chunk_size (int): The size of each chunk. Defaults to 100.
        ids (str): A comma-separated string of host IDs to use. If specified, this will be used instead of pulling the full set.

    Returns:
        Queue: A queue of host IDs to pull.
    """

    if ids:
        id_list = pull_id_set(auth, ids=ids)
    else:
        id_list = pull_id_set(auth)

    if not id_list:
        raise QualysAPIError("No IDs returned from API.")

    print(f"ID set pulled. Total IDs: {len(id_list)}")

    id_queue = Queue()

    for i in range(0, len(id_list), chunk_size):
        id_queue.put(id_list[i : i + chunk_size])

    singular_chunk = True if id_queue.qsize() == 1 else False

    print(
        f"Queue created with {id_queue.qsize()} {'chunks' if not singular_chunk else 'chunk'} of ~{chunk_size} IDs{' each.' if not singular_chunk else '.'}"
    )

    return id_queue


def get_hld(
    auth: BasicAuth,
    chunk_size: int = 3000,
    threads: int = 5,
    page_count: Union[int, "all"] = "all",
    chunk_count: Union[int, "all"] = "all",
    **kwargs,
) -> List:
    """
    get_hld - get a list of hosts and their QID detections using multiple threads. Read
    hld_backend for more information on the kwargs.

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

    # Ensure that threads, chunk_size, and page_count (if not 'all') are all integers above 0
    if any(
        [
            threads < 1,
            chunk_size < 1,
            (page_count != "all" and page_count < 1),
            (chunk_count != "all" and chunk_count < 1),
        ]
    ):
        raise ValueError(
            "threads, chunk_size, page_count (if not 'all') and chunk_count (if not 'all') must all be integers above 0."
        )

    # Make sure the user hasn't set threads to more than the cpu count
    if threads > cpu_count():
        print(
            f"Warning: The number of threads ({threads}) is greater than the number of CPUs ({cpu_count()}). This may cause performance issues."
        )

    # Second, get concurrency rate limit from auth object. NOTE: eventually, auth class should have an attribute for this.
    rl = auth.get_ratelimit()
    if threads > rl["X-Concurrency-Limit-Limit"]:
        print(
            f"Warning: The number of threads ({threads}) is greater than the concurrency rate limit ({rl['X-Concurrency-Limit-Limit']}). Setting threads to {rl['X-Concurrency-Limit-Limit']}."
        )
        threads = rl["X-Concurrency-Limit-Limit"]

    (
        print(f"Pulling/creating queue for full ID list...")
        if not kwargs.get("ids")
        else print(
            f"Pulling/creating queue for user-specified IDs: {kwargs.get('ids')}..."
        )
    )

    id_queue = create_id_queue(auth, chunk_size=chunk_size, ids=kwargs.get("ids"))
    print(f"Starting get_hld with {threads} {'threads.' if threads > 1 else 'thread.'}")

    threads_list = []

    responses = BaseList()

    for i in range(threads):
        thread = Thread(
            target=threaded_hld_worker,
            args=(auth, id_queue, responses, page_count, chunk_count, kwargs),
        )
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    print("All threads have completed. Returning responses.")
    return responses


def threaded_hld_worker(
    auth: BasicAuth,
    id_queue: Queue,
    responses: BaseList,
    page_count: Union[int, "all"],
    chunk_count: Union[int, "all"],
    kwargs,
):
    """
    threaded_hld_worker - the worker function for get_hld/hld_backend functions.

    Params:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        id_queue (Queue): The queue of host IDs to pull.
        responses (BaseList): The list of responses to append to.
        page_count (Union[int, "all"]): The number of pages to retrieve. Defaults to "all".
        chunk_count (Union[int, "all"]): The number of chunks to retrieve. Defaults to "all".
        **kwargs: Additional keyword arguments to pass to the API. See get_hld() for details.
    """
    while True:
        pages_pulled = 0
        chunks_pulled = 0
        try:
            ids = (
                id_queue.get_nowait()
            )  # nowait allows us to check if the queue is empty without blocking
        except Empty:
            with LOCK:
                print(f"{current_thread().name} - Queue is empty. Terminating thread.")
            break

        if not ids:
            with LOCK:
                print(f"{current_thread().name} - No IDs to pull. Terminating thread.")
            break

        kwargs["ids"] = f"{ids[0]}-{ids[-1]}"
        responses.extend(hld_backend(auth, page_count=page_count, **kwargs))
        id_queue.task_done()
        with LOCK:
            print(f"{current_thread().name} - Chunk complete.")
        pages_pulled += 1
        chunks_pulled += 1
        # check if the queue is empty, or if the threads are done (via pulled var)
        if id_queue.empty():
            with LOCK:
                print(f"{current_thread().name} - Queue is empty. Terminating thread.")
            break
        if pages_pulled == page_count:
            with LOCK:
                print(
                    f"{current_thread().name} - Thread has pulled all pages. Terminating thread."
                )
            break
        if chunks_pulled == chunk_count:
            with LOCK:
                print(
                    f"{current_thread().name} - Thread has pulled all chunks. Terminating thread."
                )
            break
