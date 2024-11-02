"""
Pull resources from a cloud provider account.
"""

from threading import Lock, Thread, current_thread
from queue import Queue
from typing import Literal, Union

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.AWSResources import *
from .data_classes.AzureResources import *
from .data_classes.resource_mappings import *


termination_flag = False


def fetch_page(
    auth: BasicAuth,
    provider: str,
    resourceType: str,
    pageNo: int,
    results: BaseList,
    lock: Lock,
    page_count: Union[int, "all"],
    **kwargs,
):
    """
    Worker function to fetch a single page of resources.
    """
    global termination_flag

    kwargs["placeholder"] = resourceType
    kwargs["cloudprovider"] = provider

    match kwargs["cloudprovider"].upper():
        case "AWS":
            kwargs["cloudprovider"] = "AWS"
        case "AZURE":
            kwargs["cloudprovider"] = "Azure"
        case _:
            raise ValueError("Invalid provider. Must be 'aws' or 'azure'.")

    kwargs["pageNo"] = pageNo

    response = call_api(
        auth=auth,
        module="cloudview",
        endpoint="get_inventory",
        params=kwargs,
    )

    if response.status_code not in [200, 400, 404]:
        if not response.text:
            raise QualysAPIError(
                "An error occurred while retrieving the inventory. Most likely, a parameter you set is incorrect."
            )
        else:
            raise QualysAPIError(response.json())

    # Check for empty response or invalid page count
    if (
        not response.text
        or response.status_code in [400, 404]
        or (page_count != "all" and pageNo >= 199)
    ):
        with lock:
            termination_flag = True
        return

    j = response.json()

    if j.get("empty", True):
        with lock:
            termination_flag = True
        return

    with lock:
        for i in j["content"]:
            resource_class = resource_map.get(resourceType, None)
            if resource_class:
                if "type" in i.keys():
                    i["_type"] = i.pop("type")
                i = resource_class(**i)
            else:
                raise ValueError(
                    f"Invalid resource type {resourceType} for provider {provider}. Valid resource types are:\n{VALID_RESOURCETYPES[provider]}"
                )
            results.append(i)

        if (pageNo + 1) % 20 == 0:
            print(
                f"({current_thread().name}) Page {pageNo+1} of {provider}-{resourceType} retrieved successfully."
            )

        if "INTERNAL_SERVER_ERROR" in response.text and response.status_code == 502:
            # We have reached the end of the pages
            with lock:
                termination_flag = True


def worker(
    auth,
    provider,
    resourceType,
    results,
    queue,
    lock,
    page_count,
    **kwargs,
):
    global termination_flag

    while True:
        if termination_flag:
            break

        pageNo = queue.get()
        if pageNo is None:
            break

        fetch_page(
            auth,
            provider,
            resourceType,
            pageNo,
            results,
            lock,
            page_count,
            **kwargs,
        )
        queue.task_done()


def check_termination_or_empty(queue):
    return queue.empty() or termination_flag


def get_inventory(
    auth: BasicAuth,
    provider: Literal["aws", "azure"],
    resourceType: str,
    page_count: Union[int, "all"] = "all",
    thread_count: int = 5,
    **kwargs,
) -> BaseList:
    """
    Get resources from a cloud provider account.

    Args:
        auth (BasicAuth): The authentication object.
        provider (Literal["aws", "azure"]): The cloud provider to get resources from.
        resourceType (str): The type of resource to get.
        page_count (Union[int, "all"]): The number of pages to return. MAX VALUE IS 200. If 'all', return all pages. Default is 'all'.
        thread_count (int): The number of threads to use for fetching data.

     ## Kwargs:

         sort (Literal['lastSyncedOn:asc', 'lastSyncedOn:desc']): Sort the resources by lastSyncedOn in ascending or descending order.
         updated (str): Filter resources by the last updated date. Format is Qualys QQL, like [2024-01-01 ... 2024-12-31], [2024-01-01 ... now-1m] (month), 2024-01-01, etc.
         filter (str): Filter resources by providing a Qualys QQL query.


    Returns:
        BaseList: The response from the API as a BaseList of Resource objects.
    """

    global termination_flag
    termination_flag = False

    # Validate provider
    provider = provider.lower()
    resourceType = resourceType.upper()

    kwargs["pageSize"] = 50

    if provider not in ["aws", "azure"]:
        raise ValueError("Invalid provider. Must be 'aws' or 'azure'.")

    # Handle common names
    resourceType = resourceType.replace(" ", "_")
    for key, value in COMMON_NAMES[provider].items():
        if resourceType in value:
            resourceType = key
            break

    if resourceType not in VALID_RESOURCETYPES[provider]:
        raise ValueError(
            f"Invalid resource type for provider {provider}. Valid resource types are: {VALID_RESOURCETYPES[provider]}"
        )

    if page_count != "all" and (not isinstance(page_count, int)):
        raise ValueError("page_count must be an integer <= 200 or 'all'.")

    # If user has set page_count to a number >= 200, set it to 199
    if page_count != "all" and page_count >= 200:
        page_count = 199
    elif page_count != "all" and page_count < 1:
        raise ValueError("page_count must be an integer >= 1.")

    if not isinstance(thread_count, int) or thread_count < 1:
        raise ValueError("thread_count must be an integer >= 1.")

    results = BaseList()
    page_queue = Queue()
    lock = Lock()

    # Pre-fill the queue with page numbers
    for i in range(200) if page_count == "all" else range(page_count):
        page_queue.put(i)

    # Start worker threads
    threads = []
    for _ in range(thread_count):
        t = Thread(
            target=worker,
            args=(auth, provider, resourceType, results, page_queue, lock, page_count),
            kwargs=kwargs,
        )
        threads.append(t)

    for t in threads:
        t.start()

    # Wait for the queue to be empty, or the termination flag to be set
    while not check_termination_or_empty(page_queue):
        pass

    # Stop the worker threads
    for _ in range(thread_count):
        page_queue.put(None)
    for t in threads:
        t.join()

    # print(f"{str(len(results))} {provider} {resourceType} records retrieved.")
    return results
