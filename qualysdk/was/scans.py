"""
Contains functions to interact with scans in the Qualys WAS module.
"""

from typing import Union, Literal
from os import path, makedirs

from xmltodict import unparse

from .data_classes.Scan import WASScan
from .base.parse_kwargs import validate_kwargs
from .base.web_app_service_requests import build_service_request
from .base.scan_service_requests import build_scan_service_request
from .base.web_app_service_requests import validate_response
from ..base.call_api import call_api
from ..auth.basic import BasicAuth
from ..exceptions.Exceptions import QualysAPIError
from ..base.base_list import BaseList


def call_scan_api(
    auth: BasicAuth, endpoint: str, payload: dict, cancel_with_results: bool = False
) -> Union[int, WASScan, BaseList[WASScan]]:
    """
    Call a Qualys WAS API scan endpoint and return the parsed response. This is
    a backend function and should not be called directly.

    Args:
        auth (BasicAuth): The authentication object.
        endpoint (str): The API endpoint to call.
        payload (dict): The payload to send to the API.
        cancel_with_results (bool): Whether to cancel the scan with results. Default is False. Only applies to cancel_scan.

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
        case "launch_scan":
            params = {"placeholder": "launch", "scanId": ""}
        case "cancel_scan":
            params = {"placeholder": "cancel", "scanId": payload.pop("scanId")}
            if cancel_with_results:
                payload = {
                    "_xml_data": unparse(
                        {
                            "ServiceRequest": {
                                "data": {
                                    "WasScan": {
                                        "cancelWithResults": "true",
                                    }
                                }
                            }
                        },
                        pretty=True,
                    )
                }
        case "get_scan_status":
            params = {"placeholder": "status", "scanId": payload.pop("scanId")}
        case "delete_scan":
            params = {"placeholder": "delete", "scanId": ""}
        case "download_results":
            params = {"placeholder": "download", "scanId": payload.pop("scanId")}
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}")

    response = call_api(
        auth=auth,
        override_method="GET"
        if endpoint in ["get_scan_details", "get_scan_status", "download_results"]
        else "POST",
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

        - id (int): The scan ID
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
        scanId (Union[str, int]): The scanId

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
        - id (int): The scan ID
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


def launch_scan(
    auth: BasicAuth,
    name: str,
    scan_type: Literal["DISCOVERY", "VULNERABILITY"],
    profile_id: Union[str, int],
    **kwargs,
) -> int:
    """
    Launch a new scan in Qualys WAS, targeting one or more web applications.

    **[!] Either `web_app_ids` or `included_tag_ids` is required and are mutually exclusive.**

    Args:
        auth (BasicAuth): The authentication object.
        name (str): The name of the scan.
        profile_id: The ID of the option profile to use.

    ## Kwargs:

        - web_app_ids (Union[str, int, list[Union[str, int]]]): The ID(s) of the web application(s) to scan. Required if included_tag_ids is not provided.
        - included_tags_option (Literal["ALL", "ANY"]): The option for included tags.
        - included_tag_ids (Union[str, int, list[Union[str, int]]]): The ID(s) of the tag(s) to include. Required if web_app_ids is not provided.
        - scanner_appliance_type (Literal["EXTERNAL", "INTERNAL"]): The type of scanner appliance.
        - auth_record_option (Union[str, int]): The authentication record ID.
        - profile_option (Literal["DEFAULT", "ALL", "ANY"]): The profile option.
        - scanner_option (Union[str, int]): The scanner ID.
        - send_mail (bool): Whether to send an email.
        - send_one_mail (bool): Whether to send one email.


    Returns:
        int: The ID of the scan that was launched.

    """

    # Ensure either target_webApp_id or target_tags_included_tagList_tag_id is provided:
    if not kwargs.get("web_app_ids") and not kwargs.get("included_tag_ids"):
        raise ValueError("Either web_app_ids or included_tag_ids is required.")

    kwargs["name"] = name
    kwargs["type"] = scan_type
    kwargs["profile_id"] = profile_id

    # check for single values and convert to list for web_app_ids and included_tag_ids:
    for arg in ["web_app_ids", "included_tag_ids"]:
        if kwargs.get(arg) and not isinstance(kwargs[arg], list):
            kwargs[arg] = [kwargs[arg]]

    # Validate the kwargs:
    kwargs = validate_kwargs(endpoint="launch_scan", **kwargs)

    # Build the payload:
    payload = build_scan_service_request(**kwargs)

    # Make the API call:
    parsed = call_scan_api(auth, "launch_scan", payload)

    data = parsed.get("ServiceResponse").get("data")

    if data.get("WasScan"):
        data = data.get("WasScan")

    return int(data.get("id"))


def cancel_scan(
    auth: BasicAuth, scanId: Union[str, int], retain_results: bool = False
) -> str:
    """
    Cancel an ongoing scan in Qualys WAS.

    Args:
        auth (BasicAuth): The authentication object.
        scanId (Union[str, int]): The ID of the scan to cancel.
        retain_results (bool): Whether to save the results of the scan up until the point of cancellation. Default is False.

    Returns:
        str: Status message indicating the scan was cancelled.
    """

    if not isinstance(scanId, (str, int)):
        raise ValueError("scanId must be a string or integer")

    payload = {"scanId": scanId}

    parsed = call_scan_api(
        auth, "cancel_scan", payload, cancel_with_results=retain_results
    )

    if parsed.get("ServiceResponse", dict()).get("responseCode") != "SUCCESS":
        fullMessage = parsed.get("ServiceResponse", dict()).get(
            "responseErrorDetails", dict()
        )
        return f"Error cancelling scan: {fullMessage.get('errorMessage')} - {fullMessage.get('errorResolution')}"

    return parsed.get("ServiceResponse", dict()).get("responseCode", "UNKNOWN")


def get_scan_status(auth: BasicAuth, scanId: Union[str, int]) -> dict:
    """
    Retrieve the status and authentication status of a scan in Qualys WAS.

    Args:
        auth (BasicAuth): The authentication object.
        scanId (Union[str, int]): The ID of the scan.

    Returns:
        dict: A dictionary representation of the API's XML response.
    """

    if not isinstance(scanId, (str, int)):
        raise ValueError("scanId must be a string or integer")

    parsed = call_scan_api(auth, "get_scan_status", {"scanId": scanId})

    return parsed.get("ServiceResponse")


def scan_again(auth: BasicAuth, scanId: Union[str, int], newName: str = None) -> int:
    """
    Launch a rescan of a previous scan in Qualys WAS, optionally with a new name.

    Args:
        auth (BasicAuth): The authentication object.
        scanId (Union[str, int]): The ID of the scan to rescan.
        newName (str): The new name for the scan.

    Returns:
        int: The ID of the new scan that was launched.
    """

    if not isinstance(scanId, (str, int)):
        raise ValueError("scanId must be a string or integer")

    payload = dict()

    if newName:
        payload = {
            "_xml_data": unparse(
                {
                    "ServiceRequest": {
                        "data": {
                            "WasScan": {
                                "name": newName,
                            }
                        }
                    }
                }
            )
        }

    params = {"scanId": scanId}

    result = call_api(
        auth=auth,
        module="was",
        endpoint="scan_again",
        payload=payload if payload else None,
        params=params,
        headers={"Content-Type": "text/xml"},
    )

    data = validate_response(result)

    return int(data.get("ServiceResponse").get("data").get("WasScan").get("id"))


def delete_scan(auth: BasicAuth, **kwargs) -> list[int]:
    """
    Delete 1+ scans in Qualys WAS.

    NOTE: Scans must be in a terminal state (FINISHED, ERROR, CANCELED, etc.) to be deleted.

    Args:
        auth (BasicAuth): The authentication object.

    ## Kwargs:

        - id (Union[str, int]): The ID of the scan to delete.
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): The name of the scan.
        - name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the name filter.
        - webApp_name (str): The name of the web application.
        - webApp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp.name filter.
        - webApp_id (Union[str, int]): The ID of the web application.
        - webApp_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the webApp.id filter.
        - reference (str): The reference of the scan.
        - reference_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the reference filter.
        - launchedDate (str): The date the scan was launched.
        - launchedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the launchedDate filter.
        - type (Literal["DISCOVERY", "VULNERABILITY"]): The type of scan.
        - type_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the type filter.
        - mode (Literal["ONDEMAND", "SCHEDULED", "API"]): The mode of the scan.
        - mode_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the mode filter.
        - status (Literal["SUBMITTED", "RUNNING", "FINISHED", "ERROR", "CANCELLED", "PROCESSING"]): The status of the scan.
        - status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the status filter.
        - authStatus (Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]): The authentication status of the scan.
        - authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the authStatus filter.
        - resultsStatus (Literal["NOT_USED", "TO_BE_PROCESSED", "NO_HOST_ALIVE", "NO_WEB_SERVICE", "SERVICE_ERROR", "TIME_LIMIT_REACHED", "SCAN_INTERNAL_ERROR", "SCAN_RESULTS_INVALID", "SUCCESSFUL", "PROCESSING", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "SUBMITTED", "RUNNING", "CANCELED", "CANCELING", "ERROR", "DELETED", "CANCELED_WITH_RESULTS"]): The results status of the scan.
        - resultsStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the resultsStatus filter.

    Returns:
        list[int]: The IDs of the scans that were deleted.
    """

    if not kwargs:
        raise ValueError("At least one filter is required.")

    # Validate the kwargs:
    kwargs = validate_kwargs(endpoint="delete_scan", **kwargs)

    # Build the payload:
    payload = build_service_request(**kwargs)

    # Make the API call:
    parsed = call_scan_api(auth, "delete_scan", payload)

    deleted = []
    scans = parsed.get("ServiceResponse", dict()).get("data", dict()).get("WasScan", [])
    if isinstance(scans, dict):
        scans = [scans]
    if len(scans) == 0:
        print("No scans found to delete...")
    for scan in scans:
        deleted.append(int(scan.get("id")))

    return deleted


def get_scan_results(
    auth: BasicAuth, scanId: Union[str, int], writeToFile: str = None
) -> dict:
    """
    Download the results of a scan.

    Args:
        auth (BasicAuth): The authentication object.
        scanId (Union[str, int]): The ID of the scan.
        writeToFile (str): The filepath to write the results to. Default is None (do not write to file).

    Returns:
        dict: The results of the scan.
    """

    if not isinstance(scanId, (str, int)):
        raise ValueError("scanId must be a string or integer")

    if writeToFile and not isinstance(writeToFile, str):
        raise ValueError("writeToFile must be a string or None")

    parsed = call_scan_api(auth, "download_results", {"scanId": scanId})

    if writeToFile:
        if not writeToFile.lower().endswith(".xml"):
            writeToFile += ".xml"

        if not path.exists(path.dirname(writeToFile)):
            makedirs(path.dirname(writeToFile))

        with open(writeToFile, "w") as f:
            f.write(unparse(parsed, pretty=True))
            print(f"Results written to {writeToFile}")

    return parsed.get("WasScan")
