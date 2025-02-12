"""
Helper functions for multithreading get_hld and get_host_list functions.
"""

from queue import Queue, Empty
from typing import Union, List, Literal
from threading import current_thread, Lock
from urllib.parse import urlparse, parse_qs
from os import cpu_count

from ..data_classes.hosts import VMDRID, VMDRHost
from ...exceptions import QualysAPIError
from ...base.call_api import call_api
from ...base.xml_parser import xml_parser
from ...auth.basic import BasicAuth
from ...base.base_list import BaseList

LOCK = Lock()


def prepare_args(
    auth: BasicAuth,
    chunk_size: int,
    threads: int,
    page_count: Union[int, "all"],
    chunk_count: Union[int, "all"],
    ids: str = None,
) -> dict:
    """
    Performs necessary checks for thread count, CPU count, rate
    limits.

    Args:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        chunk_size (int): The size of each chunk.
        threads (int): The number of threads.
        page_count (Union[int, 'all']): The number of pages to retrieve.
        chunk_count (Union[int, 'all']): The number of chunks to retrieve.
        ids (str): A comma-separated string of host IDs to use. If specified, this will be used instead of pulling the full set.

    Returns:
        None

    Raises:
        ValueError: If threads, chunk_size, page_count, or chunk_count are less than 1.
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
        with LOCK:
            print(
                f"Warning: The number of threads ({threads}) is greater than the number of CPUs ({cpu_count()}). This may cause performance issues."
            )

    # Second, get concurrency rate limit from auth object. NOTE: eventually, auth class should have an attribute for this.
    rl = auth.get_ratelimit()
    if threads > rl["X-Concurrency-Limit-Limit"]:
        with LOCK:
            print(
                f"Warning: The number of threads ({threads}) is greater than the concurrency rate limit ({rl['X-Concurrency-Limit-Limit']}). Setting threads to {rl['X-Concurrency-Limit-Limit']}."
            )
        threads = rl["X-Concurrency-Limit-Limit"]

    (
        print("Pulling/creating queue for full ID list...")
        if not ids
        else print(f"Pulling/creating queue for user-specified IDs: {ids}...")
    )


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
        # User has specified specific IDs to pull:
        res = get_host_list_backend(auth, details=None, truncation_limit=0, ids=ids)
    else:
        # User has not specified specific IDs to pull, so pull all:
        res = get_host_list_backend(auth, details=None, truncation_limit=0)

    if not res:
        raise QualysAPIError("No IDs returned from API!")

    return [str(i) for i in res]


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
    with LOCK:
        print(f"ID set pulled. Total IDs: {len(id_list)}")

    id_queue = Queue()

    for i in range(0, len(id_list), chunk_size):
        id_queue.put(id_list[i : i + chunk_size])

    singular_chunk = True if id_queue.qsize() == 1 else False

    # If there is only 1 chunk, split it up where each new
    # chunk only contains 1 ID. This is to ensure that each
    # thread has something to pull.
    if singular_chunk:
        new_queue = Queue()
        for i in range(0, len(id_list)):
            new_queue.put(id_list[i : i + 1])
        id_queue = new_queue

    with LOCK:
        print(f"Queue created with {id_queue.qsize()} chunks")

    return id_queue


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
                    with LOCK:
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
                        f"{current_thread().name} (get_hld) - Pagination detected. Pulling next page with id_min: {params['id_min'][0]}"
                    )
                kwargs["id_min"] = params["id_min"][0]

            else:
                break
        else:
            break

    return responses


def get_cve_hld_backend(
    auth: BasicAuth,
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> List:
    """
    Backend for CVE Host List Detection.
    """

    # Set the kwargs
    kwargs["action"] = "list"

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
            endpoint="get_cve_hld",
            params=kwargs,
            headers={"X-Requested-With": "qualysdk SDK"},
        )

        if response.status_code != 200:
            with LOCK:
                print(f"{current_thread().name} - No data returned on page {pulled}")
            pulled += 1
            if pulled != "all":
                if pulled == page_count:
                    with LOCK:
                        print(f"{current_thread().name} - Pulled all pages.")
                    break
                else:
                    continue

        # cleaned = remove_problem_characters(response.text)
        xml = xml_parser(response.content)

        # check if there is no host list
        if "HOST_LIST" not in xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]:
            with LOCK:
                print(f"{current_thread().name} - No host list returned.")
        else:
            # check if ["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"] is a list of dictionaries
            # or just a dictionary. if it is just one, put it inside a list
            if not isinstance(
                xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"][
                    "HOST"
                ],
                list,
            ):
                xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"][
                    "HOST"
                ] = [
                    xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]["HOST_LIST"][
                        "HOST"
                    ]
                ]

            for host in xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"][
                "HOST_LIST"
            ]["HOST"]:
                # Ensure compatability:
                host["DETECTION_LIST"] = host.pop("CVE_DETECTION_LIST")
                host_obj = VMDRHost.from_dict(host)
                responses.append(host_obj)

        pulled += 1
        if page_count != "all":
            if pulled == page_count:
                break

        if "WARNING" in xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]:
            if "URL" in xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]["WARNING"]:
                # get the id_min parameter from the URL to pass into kwargs:
                params = parse_qs(
                    urlparse(
                        xml["HOST_LIST_CVE_VM_DETECTION_OUTPUT"]["RESPONSE"]["WARNING"][
                            "URL"
                        ]
                    ).query
                )
                with LOCK:
                    print(
                        f"{current_thread().name} (get_hld) - Pagination detected. Pulling next page with id_min: {params['id_min'][0]}"
                    )
                kwargs["id_min"] = params["id_min"][0]

            else:
                break
        else:
            break

    return responses


def thread_worker(
    auth: BasicAuth,
    id_queue: Queue,
    responses: BaseList,
    page_count: Union[int, "all"],
    chunk_count: Union[int, "all"],
    endpoint_called: Literal["get_hld", "get_host_list", "get_cve_hld"],
    kwargs,
):
    """
    thread_worker - the worker function for get_hld/hld_backend functions.

    Params:
        auth (BasicAuth): The BasicAuth object containing the username and password.
        id_queue (Queue): The queue of host IDs to pull.
        responses (BaseList): The list of responses to append to.
        page_count (Union[int, "all"]): The number of pages to retrieve. Defaults to "all".
        chunk_count (Union[int, "all"]): The number of chunks to retrieve. Defaults to "all".
        endpoint_called (Union['get_hld', 'get_host_list', 'get_cve_hld']): The function that was called.
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

        if len(ids) != 1:
            kwargs["ids"] = f"{ids[0]}-{ids[-1]}"
        else:
            kwargs["ids"] = ids[0]

        if endpoint_called == "get_hld":
            responses.extend(hld_backend(auth, page_count=page_count, **kwargs))
        elif endpoint_called == "get_host_list":
            responses.extend(
                get_host_list_backend(auth, page_count=page_count, **kwargs)
            )
        elif endpoint_called == "get_cve_hld":
            responses.extend(get_cve_hld_backend(auth, page_count=page_count, **kwargs))
        else:
            raise ValueError(
                "endpoint_called must be either 'get_hld' or 'get_host_list'."
            )
        id_queue.task_done()
        with LOCK:
            print(f"{current_thread().name} ({endpoint_called}) - Chunk complete.")
        pages_pulled += 1
        chunks_pulled += 1
        # check if the queue is empty, or if the threads are done (via pulled var)
        if id_queue.empty():
            with LOCK:
                print(
                    f"{current_thread().name} ({endpoint_called}) - Queue is empty. Terminating thread."
                )
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


def get_host_list_backend(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> list:
    """
    Get the host list from the VMDR API.
    For a full list of parameters, see the Qualys API documentation: [Qualys API VMPc User Guide](https://cdn2.qualys.com/docs/qualys-api-vmpc-user-guide.pdf)

    Parameters:
        auth (BasicAuth): The authentication object.
        page_count (Union[int, "all"]): The number of pages to get. If "all", get all pages. Defaults to "all".

    :Kwargs:

        action (Optional[str]): The action to perform. Default is 'list'. WARNING: any value you pass is overwritten with 'list'. It is just recognized as valid for the sake of completeness.
        echo_request (Optional[bool]): Whether to show the request. Default is 'False'. ends up being passed to API as 0 or 1.
        show_asset_id (Optional[bool]): Whether to show the asset IDs. Default is 'False'. ends up being passed to API as 0 or 1.
        details (Optional[Union[Literal["Basic", "Basic/AGs", "All", "All/AGs", "None"], None]]): The level of detail to return. Default is 'Basic'. Basic includes host ID, IP, tracking method, DNS, netBIOS, and OS. Basic/AGs includes basic host information plus asset group information. Asset group information includes the asset group ID and title. All shows all basic host information plus last vulnerability and compliance scan dates. All/AGs includes all information plus asset group information: group ID and title. None shows only the host ID (or asset ID if show_asset_id is set to 1 (True)).
        os_pattern (Optional[str]): The OS regex pattern to search for. It follows the PCRE standard, and must be URL-encoded. To match an empty string, use '%5E%24'.
        truncation_limit (Optional[int]): The maximum number of characters to return for each field. Default is 1000, and can be set to 0 for no truncation all the way up to 1,000,000. Past 1M, the API will return an error.
        ips (Optional[str]): Only show assets with certain IP addresses/ranges. Multiple values specified as a comma-separated string. A range is specified with a hyphen. Example: 10.0.0.1-10.0.0.255
        ipv6 (Optional[str]): Only show assets with certain IPv6 addresses/ranges. Multiple values specified as a comma-separated string.
        ag_ids (Optional[str]): Only show assets in certain asset group IDs. Multiple values specified as a comma-separated string. A range is specified with a hyphen. Example: 1-5. A valid ID is required or the API will return an error.
        ag_titles (Optional[str]): Only show assets with specified string in the asset group title. Multiple values specified as a comma-separated string.
        ids (Optional[str]): Only show assets with certain asset IDs. Multiple values specified as a comma-separated string. A range is specified with a hyphen. Example: 1-5. A valid ID is required or the API will return an error.
        id_min (Optional[int]): Only show assets with asset IDs greater than or equal to this value.
        id_max (Optional[int]): Only show assets with asset IDs less than or equal to this value.
        network_ids (Optional[str]): Valid only when the Network Support feature is enabled for the users account). Restrict the request to certain custom network IDs. Multiple network IDs are comma separated.
        compliance_enabled (Optional[bool]): Only show assets with compliance enabled. Default is 'False'. ends up being passed to API as 0 or 1.

        DATE PARAMS

        no_vm_scan_since (Optional[str]): Only show assets that have not been scanned since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        no_compliance_scan_since (Optional[str]): Only show assets that have not had a compliance scan since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_scan_since (Optional[str]): Only show assets that have been scanned since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        compliance_scan_since (Optional[str]): Only show assets that have had a compliance scan since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_processed_before (Optional[str]): Only show assets that have been processed by the VM module before this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_processed_after (Optional[str]): Only show assets that have been processed by the VM module after this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_scan_date_before (Optional[str]): Only show assets that have been scanned by the VM module before this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_scan_date_after (Optional[str]): Only show assets that have been scanned by the VM module after this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_auth_scan_date_before (Optional[str]): Only show assets that have been authenticated scanned by the VM module before this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_auth_scan_date_after (Optional[str]): Only show assets that have been authenticated scanned by the VM module after this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        scap_scan_since (Optional[str]): Only show assets that have been scanned by the SCAP module since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        no_scap_scan_since (Optional[str]): Only show assets that have not been scanned by the SCAP module since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.

        TAG PARAMS

        use_tags (bool): Whether to use tags. Default is 'False'. ends up being passed to API as 0 or 1.
        tag_set_by (Optional[Literal["id","name"]]): search for tags by ID or name. Default is 'id'.
        tag_include_selector (Optional[Literal["any","all"]]): Specified tags will be included if any or all are matched. Default is 'any'. Only valid if use_tags is set to 1 (True).
        tag_exclude_selector (Optional[Literal["any","all"]]): Specified tags will be excluded if any or all are matched. Default is 'any'. Only valid if use_tags is set to 1 (True).
        tag_set_include (Optional[str]): Only show assets with tags that match this string. Multiple values specified as a comma-separated string. Only valid if use_tags is set to 1 (True).
        tag_set_exclude (Optional[str]): Only show assets with tags that do not match this string. Multiple values specified as a comma-separated string. Only valid if use_tags is set to 1 (True).
        show_tags (Optional[bool]): Whether to show tags. Default is 'False'. ends up being passed to API as 0 or 1.

        ARS (Asset Risk Score) PARAMS

        show_ars (Optional[bool]): Whether to show the ARS. Default is 'False'. ends up being passed to API as 0 or 1.
        ars_min (Optional[int]): Only show assets with an ARS greater than or equal to this value.
        ars_max (Optional[int]): Only show assets with an ARS less than or equal to this value.
        show_ars_factors (Optional[bool]): Whether to show the ARS factors. Default is 'False'. ends up being passed to API as 0 or 1.

        TRURISK PARAMS

        show_trurisk (Optional[bool]): Whether to show the TruRisk. Default is 'False'. ends up being passed to API as 0 or 1.
        trurisk_min (Optional[int]): Only show assets with a TruRisk greater than or equal to this value.
        trurisk_max (Optional[int]): Only show assets with a TruRisk less than or equal to this value.
        show_trurisk_factors (Optional[bool]): Whether to show the TruRisk factors. Default is 'False'. ends up being passed to API as 0 or 1.

        CLOUD HOST PARAMS

        host_metadata (Optional[Literal["all", "ec2", "azure", "google"]]): Specify all to list all cloud and non-cloud assets. Specify a service to just get cloud assets for that service plus non-cloud assets.
        host_metadata_fields (Optional[str]): Specify the fields to return for cloud assets. Multiple values specified as a comma-separated string. Only valid if host_metadata is set to a cloud service.
        show_cloud_tags (Optional[bool]): Whether to show cloud tags. Default is 'False'. ends up being passed to API as 0 or 1.
        cloud_tag_fields (Optional[str]): Specify the cloud tag name and value, separated by a colon. Multiple values specified as a comma-separated string. If this is not specified and show_cloud_tags is 1, all tags are returned.

    Returns:

        list[Union[VMDRHost, VMDRID]]: A list of VMDRHost or VMDRID objects.
    """

    responses = BaseList()
    pulled = 0

    # add the action to the kwargs:
    kwargs["action"] = "list"

    if kwargs.get("truncation_limit") and (
        kwargs["truncation_limit"] in [0, "0"]
        and kwargs["details"] not in ["None", None]
    ):
        with LOCK:
            print(
                "[!] Warning: You have specified to pull all data with no pagination. This is generally not recommended, as it uses lots of resources and take a long time to complete. Please consider specifying a page_count or truncation_limit to avoid this issue."
            )

    while True:
        # make the request:
        response = call_api(
            auth=auth,
            module="vmdr",
            endpoint="get_host_list",
            params=kwargs,
            headers={"X-Requested-With": "qualysdk SDK"},
        )
        if response.status_code != 200:
            with LOCK:
                print("No data returned.")
            return responses

        xml = xml_parser(response.content)

        if (
            "HOST_LIST" not in xml["HOST_LIST_OUTPUT"]["RESPONSE"]
            and "ID_SET" not in xml["HOST_LIST_OUTPUT"]["RESPONSE"]
        ):
            with LOCK:
                print("No host list returned.")
            return

        # If details is none, ID_SET will be returned instead of HOST_LIST
        if "ID_SET" in xml["HOST_LIST_OUTPUT"]["RESPONSE"]:
            # check if ID_SET is a list of dicts/str or a single dict/str:
            if isinstance(
                xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"], (dict, str)
            ):
                # if it's a single dict, convert it to a list of dicts:
                xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"] = [
                    xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"]
                ]

            for ID in xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"]:
                # create a VMDRID object and append to responses
                # This code will only run if details=None, so now we just need to check if show_asset_id is set to 1:
                if kwargs.get("show_asset_id"):
                    responses.append(VMDRID(ID=ID, TYPE="asset"))
                else:  # elif not kwargs.get("show_asset_id"):
                    responses.append(VMDRID(ID=ID, TYPE="host"))
        else:
            # HOST_LIST will be returned
            # first, check if xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"]
            # is a list of dicts or a single dict:
            if isinstance(
                xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"], dict
            ):
                # if it's a single dict, convert it to a list of dicts:
                xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"] = [
                    xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"]
                ]

            for host in xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"]:
                # return a list of VMDRHost objects
                responses.append(VMDRHost.from_dict(host))

        pulled += 1

        if page_count != "all" and pulled >= page_count:
            with LOCK:
                print(f"{current_thread().name} Page count reached.")
            break

        if "WARNING" in xml["HOST_LIST_OUTPUT"]["RESPONSE"]:
            if "URL" in xml["HOST_LIST_OUTPUT"]["RESPONSE"]["WARNING"]:
                with LOCK:
                    print(
                        f"{current_thread().name} (get_host_list) Pagination detected. Pulling next page from url: {xml['HOST_LIST_OUTPUT']['RESPONSE']['WARNING']['URL']}"
                    )
                # get the id_min parameter from the URL to pass into kwargs:
                params = parse_qs(
                    urlparse(
                        xml["HOST_LIST_OUTPUT"]["RESPONSE"]["WARNING"]["URL"]
                    ).query
                )
                kwargs["id_min"] = params["id_min"][0]

            else:
                break
        else:
            break

    return responses
