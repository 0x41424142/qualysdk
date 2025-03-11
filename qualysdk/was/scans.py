"""
Contains functions to interact with scans in the Qualys WAS module.
"""

from typing import Union

from .data_classes.Scan import WASScan
from .base.parse_kwargs import validate_kwargs
from .base.web_app_service_requests import build_service_request
from .base.web_app_service_requests import validate_response
from ..base.call_api import call_api
from ..auth.basic import BasicAuth
from ..exceptions.Exceptions import QualysAPIError
from ..base.base_list import BaseList


def call_scan_api(
    auth: BasicAuth, endpoint: str, payload: dict
) -> Union[int, WASScan, BaseList[WASScan]]:
    """
    Call a Qualys WAS API scan endpoint and return the parsed response. This is
    a backend function and should not be called directly.

    Args:
        auth (BasicAuth): The authentication object.
        endpoint (str): The API endpoint to call.
        payload (dict): The payload to send to the API.

    Returns:
        Union[int, WASScan, BaseList[WASScan]]: The parsed response from the API.
    """

    match endpoint:
        case "count_scans":
            params = {"placeholder": "count", "scanId": ""}
        case "get_scans":
            params = {"placeholder": "search", "scanId": ""}
        case "get_scan_details":
            params = {"placeholder": "get", "scanId": payload.pop("scanId")}
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}")

    response = call_api(
        auth=auth,
        override_method="GET" if endpoint == "get_scan_details" else "POST",
        module="was",
        endpoint="call_scans_api",
        payload=payload,
        params=params,
        headers={"Content-Type": "text/xml"},
    )

    return validate_response(response)


def count_scans(auth: BasicAuth, **kwargs) -> int:
    """
    Count the number of scans in the subscription that match the given kwargs.

    Args:
        auth (BasicAuth): The authentication object.

        ## Kwargs:

            - id (Union[str, int]): Scan ID.
            - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
            - name (str): Scan name.
            - name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the name filter.
            - reference (str): Scan reference.
            - reference_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the reference filter.
            - type (Literal["DISCOVERY", "VULNERABILITY"]): Scan type.
            - type_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the type filter.
            - mode (Literal["ONDEMAND", "SCHEDULED, "API"]): Scan mode.
            - mode_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the mode filter.
            - status (Literal["SUBMITTED", "RUNNING", "FINISHED", "ERROR", "CANCELLED", "PROCESSING"]): Scan status.
            - status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the status filter.
            - webApp.id (Union[str, int]): Web application ID.
            - webApp.id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the webApp.id filter.
            - webApp.name (str): Web application name.
            - webApp.name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp.name filter.
            - webApp.tags.id (Union[str, int]): Web application tag ID.
            - webApp.tags.id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the webApp.tags.id filter.
            - resultsStatus (Literal["NOT_USED", "TO_BE_PROCESSED", "NO_HOST_ALIVE", "NO_WEB_SERVICE", "SERVICE_ERROR", "TIME_LIMIT_REACHED", "SCAN_INTERNAL_ERROR", "SCAN_RESULTS_INVALID", "SUCCESSFUL", "PROCESSING", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "SUBMITTED", "RUNNING", "CANCELED", "CANCELING", "ERROR", "DELETED", "CANCELED_WITH_RESULTS"]): Results status.
            - resultsStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the resultsStatus filter.
            - authStatus (Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]): Authentication status.
            - authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the authStatus filter.
            - launchedDate (str): Scan launch date in UTC: YYYY-MM-DDTHH:MM:SSZ
            - launchedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the launchedDate filter.

    Returns:
        int: The number of scans that match the given kwargs.
    """

    payload = None

    if kwargs:
        for key, value in kwargs.items():
            # cast all to string:
            kwargs[key] = str(value)
        kwargs = validate_kwargs(endpoint="count_scans", **kwargs)

        payload = build_service_request(**kwargs)

    # Make the API call
    parsed = call_scan_api(auth=auth, endpoint="count_scans", payload=payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response code was not SUCCESS: {serviceResponse.get('responseCode')}"
        )

    return int(serviceResponse.get("count"))


def get_scans(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> BaseList[WASScan]:
    """
    Get a list of scans from Qualys WAS according
    to the filters provided

    Args:
        auth (BasicAuth): The authentication object
        page_count (Union[int, "all"]): The number of pages to retrieve. Default is "all"

    ## Kwargs:

        - id (int): The finding ID
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): The scan name
        - name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the name filter.
        - reference (str): The scan reference
        - reference_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the reference filter.
        - type (Literal["DISCOVERY", "VULNERABILITY"]): The scan type
        - type_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the type filter.
        - mode (Literal["ONDEMAND", "SCHEDULED", "API"]): The scan mode
        - mode_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the mode filter.
        - status (Literal["SUBMITTED", "RUNNING", "FINISHED", "ERROR", "CANCELLED", "PROCESSING"]): The scan status
        - status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the status filter.
        - webApp_id (int): The web application ID
        - webApp_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the webApp.id filter.
        - webApp_name (str): The web application name
        - webApp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp.name filter.
        - webApp_tags_id (int): The web application tag ID
        - webApp_tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the webApp.tags.id filter.
        - resultsStatus (Literal["NOT_USED", "TO_BE_PROCESSED", "NO_HOST_ALIVE", "NO_WEB_SERVICE", "SERVICE_ERROR", "TIME_LIMIT_REACHED", "SCAN_INTERNAL_ERROR", "SCAN_RESULTS_INVALID", "SUCCESSFUL", "PROCESSING", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "SUBMITTED", "RUNNING", "CANCELED", "CANCELING", "ERROR", "DELETED", "CANCELED_WITH_RESULTS"]): The results status
        - resultsStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the resultsStatus filter.
        - authStatus (Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]): The authentication status
        - authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the authStatus filter.
        - launchedDate (str): The scan launch date in UTC: YYYY-MM-DDTHH:MM:SSZ
        - launchedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the launchedDate filter.

    Returns:
        BaseList[WASScan]: A list of WASScan objects
    """

    if page_count != "all" and not (isinstance(page_count, int) or page_count < 0):
        raise ValueError("page_count must be 'all' or a positive integer")

    pageNo = 0
    payload = None

    # If kwargs are provided, validate them:
    if kwargs:
        kwargs = validate_kwargs(endpoint="get_scans", **kwargs)
        payload = build_service_request(**kwargs)

    scanList = BaseList()

    while True:
        # Make the API call:
        parsed = call_scan_api(auth, "get_scans", payload)

        # Parse the XML response:
        serviceResponse = parsed.get("ServiceResponse")
        if not serviceResponse:
            raise QualysAPIError("No ServiceResponse tag returned in the API response")

        if serviceResponse.get("responseCode") != "SUCCESS":
            raise QualysAPIError(
                f"API response returned error: {serviceResponse.get('responseCode')}"
            )

        if serviceResponse.get("count") == "0":
            print(f"No scans found on page {pageNo}. Exiting.")
            break

        data = serviceResponse.get("data")

        if data.get("WasScan"):
            data = data.get("WasScan")

        if isinstance(data, dict):
            data = [data]

        for scan in data:
            # Create the objects:
            scanList.append(WASScan.from_dict(scan))

        print(
            f"Retrieved {serviceResponse.get('count')} WAS scans on page {pageNo}. Running total: {len(scanList)}"
        )

        pageNo += 1

        if page_count != "all" and pageNo >= page_count:
            print(f"Reached page_count limit. Returning {pageNo} page(s).")
            break

        # Check for pagination:
        if serviceResponse.get("hasMoreRecords") == "true":
            # Update the XML payload with the new Criteria:
            # <Criteria field="id" operator="GREATER">XXX</Criteria>
            kwargs["id.operator"] = "GREATER"
            kwargs["id"] = serviceResponse.get("lastId")
            payload = build_service_request(**kwargs)
        else:
            break

    return scanList


def get_scan_details(auth: BasicAuth, scanId: Union[str, int]) -> WASScan:
    """
    Pull all details of a single scan from Qualys WAS
    by its finding # or unique ID

    Args:
        auth (BasicAuth): The authentication object
        scanId (Union[str, int]): The finding number or unique ID of the scanId

    Returns:
        WASFinding: The WASFinding object
    """

    if not isinstance(scanId, (str, int)):
        raise ValueError("scanId must be a string or integer")

    # Make the API call
    parsed = call_scan_api(auth, "get_scan_details", {"scanId": scanId})

    # Parse the XML response:
    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    data = serviceResponse.get("data")

    if data.get("WasScan"):
        data = data.get("WasScan")

    return WASScan.from_dict(data)


def get_scans_verbose(
    auth: BasicAuth, thread_count: int = 5, **kwargs
) -> BaseList[WASScan]:
    """
    Uses ```was.get_scans()``` and ```was.get_scan_details()``` to return a ```BaseList``` of ```WASScan```s with
    all attributes populated.

    This function is multi-threaded, placing all ```WASScan``` found
    from ```was.get_scans()``` into a queue and then spawning threads to pull the details one
    by one.

    The details threads wait for work to be added to the queue and then pull
    the details for each ```WASScan.id```.

    Args:
        auth (BasicAuth): The authentication object.
        thread_count (int): The number of threads to spawn. Defaults to 5.

    ## Kwargs:

        - page_count (Union[int, "all"]): The number of pages to retrieve. Default is "all"
        - id (int): The finding ID
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): The scan name
        - name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the name filter.
        - reference (str): The scan reference
        - reference_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the reference filter.
        - type (Literal["DISCOVERY", "VULNERABILITY"]): The scan type
        - type_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the type filter.
        - mode (Literal["ONDEMAND", "SCHEDULED", "API"]): The scan mode
        - mode_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the mode filter.
        - status (Literal["SUBMITTED", "RUNNING", "FINISHED", "ERROR", "CANCELLED", "PROCESSING"]): The scan status
        - status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the status filter.
        - webApp_id (int): The web application ID
        - webApp_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the webApp.id filter.
        - webApp_name (str): The web application name
        - webApp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp.name filter.
        - webApp_tags_id (int): The web application tag ID
        - webApp_tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the webApp.tags.id filter.
        - resultsStatus (Literal["NOT_USED", "TO_BE_PROCESSED", "NO_HOST_ALIVE", "NO_WEB_SERVICE", "SERVICE_ERROR", "TIME_LIMIT_REACHED", "SCAN_INTERNAL_ERROR", "SCAN_RESULTS_INVALID", "SUCCESSFUL", "PROCESSING", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "SUBMITTED", "RUNNING", "CANCELED", "CANCELING", "ERROR", "DELETED", "CANCELED_WITH_RESULTS"]): The results status
        - resultsStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the resultsStatus filter.
        - authStatus (Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]): The authentication status
        - authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the authStatus filter.
        - launchedDate (str): The scan launch date in UTC: YYYY-MM-DDTHH:MM:SSZ
        - launchedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the launchedDate filter.

    Returns:
        BaseList[WASScan]: The list of scans that match the given kwargs.
    """

    # Check thread_count for a valid value:
    if not isinstance(thread_count, int) or thread_count < 1:
        raise ValueError("thread_count must be an integer >= 1.")

    # Set up Queue and List, with some cheeky as-needed imports:
    from queue import Queue
    from threading import Thread, Lock, current_thread

    q = Queue()
    scanList = BaseList()
    LOCK = Lock()
    threads = []

    # Get the scans:
    print(f"({current_thread().name}) Getting base scan list...")
    scans = get_scans(auth, **kwargs)

    print(
        f"({current_thread().name}) Pulled {len(scans)} scans. Starting {thread_count} thread(s) for details pull.."
    )

    # Add the scans to the queue:
    for scan in scans:
        q.put(scan)

    def worker():
        while True:
            try:
                # Exit condition 1: Queue is empty
                if q.empty():
                    with LOCK:
                        print(
                            f"({current_thread().name}) Queue is empty. Thread exiting."
                        )
                        break

                scan = q.get()
                # Exit condition 2: scan is None (because Queue is empty)
                if not scan:
                    with LOCK:
                        print(
                            f"({current_thread().name}) Queue is empty. Thread exiting."
                        )
                        q.task_done()
                    break

                details = get_scan_details(auth, scan.id)
                scanList.append(details)
                q.task_done()
                with LOCK:
                    if len(scanList) % 10 == 0:
                        print(
                            f"({current_thread().name}) Pulled {len(scanList)} scan details so far..."
                        )

            except Exception as e:
                with LOCK:
                    print(
                        f"[ERROR - THREAD EXITING] ({current_thread().name}) Error: {e}"
                    )
                q.task_done()
                break

    # Start the threads:
    for i in range(thread_count):
        t = Thread(target=worker)
        threads.append(t)
        t.start()

    # Wait for the threads to finish:
    for t in threads:
        t.join()

    print(f"Pulled {len(scanList)} scan details.")
    return scanList
