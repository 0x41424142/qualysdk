"""
Contains user-facing functions for interacting with authentication records in WAS
"""

from typing import Union

from .data_classes.WebAppAuthRecord import WebAppAuthRecord
from .base.service_requests import build_service_request, build_update_request
from .base.parse_kwargs import validate_kwargs
from .base.service_requests import validate_response
from ..base.call_api import call_api
from ..auth.basic import BasicAuth
from ..exceptions.Exceptions import QualysAPIError
from ..base.base_list import BaseList


def call_auth_api(
    auth: BasicAuth, endpoint: str, payload: dict
) -> Union[int, WebAppAuthRecord]:
    """
    Call a Qualys WAS API auth record endpoint and return the parsed response. This is
    a backend function and should not be called directly.

    Args:
        auth (BasicAuth): The authentication object.
        endpoint (str): The API endpoint to call.
        payload (dict): The payload to send to the API.

    Returns:
        Union[int, WebAppAuthRecord]: The parsed response from the API.
    """

    match endpoint:
        case "count_authentication_records":
            params = {"placeholder": "count", "webappAuthRecordId": ""}
        case "get_authentication_records":
            params = {"placeholder": "search", "webappAuthRecordId": ""}
        case "get_authentication_record_details":
            params = {
                "placeholder": "get",
                "webappAuthRecordId": payload.pop("recordId"),
            }
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}")

    response = call_api(
        auth=auth,
        override_method=(
            "GET" if endpoint == "get_authentication_record_details" else "POST"
        ),
        module="was",
        endpoint="call_auth_api",
        params=params,
        payload=payload,
        headers={"Content-Type": "text/xml"},
    )

    return validate_response(response)


def count_authentication_records(auth: BasicAuth, **kwargs) -> int:
    """
    Return a count of auth records in the Qualys WAS module
    according to the provided filters.

    Args:
        auth (BasicAuth): The authentication object.

    ## Kwargs:

        - id (Union[str, int]): Authentication object ID.
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): Auth object name.
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the name filter.
        - tags (Union[str, int]): Tag ID.
        - tags_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tags filter.
        - tags_name (str): Tag name.
        - tags_name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the tag name filter.
        - tags_id (Union[str, int]): Tag ID.
        - tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tag ID filter.
        - createdDate (str): Date the Auth object was created in UTC date/time format.
        - createdDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the created date filter.
        - updatedDate (str): Date the Auth object was last updated in UTC date/time format.
        - updatedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the updated date filter.
        - isUsed (bool): Whether the Auth object is in use.
        - isUsed (Literal["EQUALS", "NOT EQUALS"]): Operator for the isUsed filter.
        - lastScan_authStatus (Literal["NONE", "NOT_USED", "PARTIAL", "FAILED", "SUCCESSFUL"]): Status of the last scan.
        - lastScan_authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the last scan status filter.
        - lastScan_date (str): Date of the last scan in UTC date/time format.
        - lastScan_date_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the last scan date filter.
        - contents (Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]): Auth object contents.
        - contents_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the contents filter.

    Returns:
        int: The count of Auth objects that match the filters.
    """

    payload = None

    # If kwargs are provided, validate them:
    if kwargs:
        kwargs = validate_kwargs(endpoint="count_authentication_records", **kwargs)
        payload = build_service_request(**kwargs)

    # Make the API call:
    parsed = call_auth_api(auth, "count_authentication_records", payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    return int(serviceResponse.get("count"))


def get_authentication_records(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> object:
    """
    Get a list of auth records in the Qualys WAS module
    according to the provided filters.

    Args:
        auth (BasicAuth): The authentication object.
        page_count (int): The number of pages to return. If 'all', return all pages. Default is 'all'.

    ## Kwargs:

        - id (Union[str, int]): Authentication object ID.
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): Auth object name.
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the name filter.
        - tags (Union[str, int]): Tag ID.
        - tags_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tags filter.
        - tags_name (str): Tag name.
        - tags_name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the tag name filter.
        - tags_id (Union[str, int]): Tag ID.
        - tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tag ID filter.
        - createdDate (str): Date the Auth object was created in UTC date/time format.
        - createdDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the created date filter.
        - updatedDate (str): Date the Auth object was last updated in UTC date/time format.
        - updatedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the updated date filter.
        - isUsed (bool): Whether the Auth object is in use.
        - isUsed (Literal["EQUALS", "NOT EQUALS"]): Operator for the isUsed filter.
        - lastScan_authStatus (Literal["NONE", "NOT_USED", "PARTIAL", "FAILED", "SUCCESSFUL"]): Status of the last scan.
        - lastScan_authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the last scan status filter.
        - lastScan_date (str): Date of the last scan in UTC date/time format.
        - lastScan_date_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the last scan date filter.
        - contents (Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]): Auth object contents.
        - contents_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the contents filter.

    Returns:
        object: The auth records that match the filters.
    """

    # Ensure that page_count is either the string 'all' or an integer >= 1:
    if isinstance(page_count, int) and page_count < 1:
        raise QualysAPIError("page_count must be 'all' or an integer >= 1.")
    elif isinstance(page_count, str) and page_count != "all":
        raise QualysAPIError("page_count must be 'all' or an integer >= 1.")

    pageNo = 0
    payload = None

    # If kwargs are provided, validate them:
    if kwargs:
        kwargs = validate_kwargs(endpoint="get_authentication_records", **kwargs)
        payload = build_service_request(**kwargs)

    appList = BaseList()

    while True:
        # Make the API call:
        parsed = call_auth_api(auth, "get_authentication_records", payload)

        # Parse the XML response:
        serviceResponse = parsed.get("ServiceResponse")
        if not serviceResponse:
            raise QualysAPIError("No ServiceResponse tag returned in the API response")

        if serviceResponse.get("responseCode") != "SUCCESS":
            raise QualysAPIError(
                f"API response returned error: {serviceResponse.get('responseCode')}"
            )

        if serviceResponse.get("count") == "0":
            print(f"No web applications found on page {pageNo}. Exiting.")
            break

        data = serviceResponse.get("data")

        if data.get("WebAppAuthRecord"):
            data = data.get("WebAppAuthRecord")

        if isinstance(data, dict):
            data = [data]

        for record in data:
            # Create the objects:
            appList.append(WebAppAuthRecord.from_dict(record))

        print(
            f"Retrieved {serviceResponse.get('count')} auth records on page {pageNo}. Running total: {len(appList)}"
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

    return appList


def get_authentication_record_details(
    auth: BasicAuth, recordId: Union[int, str]
) -> WebAppAuthRecord:
    """
    Pull a single authentication record with all attributes populated.

    Args:
        auth (BasicAuth): The authentication object.
        recordId (Union[int, str]): The ID of the record to pull.

    Returns:
        WebAppAuthRecord: The authentication record.
    """
    # Make the API call:
    parsed = call_auth_api(
        auth, "get_authentication_record_details", {"recordId": recordId}
    )

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    data = serviceResponse.get("data")
    if data.get("WebAppAuthRecord"):
        data = data.get("WebAppAuthRecord")
        return WebAppAuthRecord.from_dict(data)
    else:
        print(f"No data found for web application ID {recordId}. Exiting.")


def get_authentication_records_verbose(
    auth: BasicAuth, thread_count: int = 5, **kwargs
) -> BaseList[WebAppAuthRecord]:
    """
    Uses ```was.get_authentication_records()``` and ```was.get_authentication_record_details()``` to return a ```BaseList``` of ```WebAppAuthRecord```s with
    all attributes populated.

    This function is multi-threaded, placing all ```WebAppAuthRecords``` found
    from ```was.get_authentication_records()``` into a queue and then spawning threads to pull the details one
    by one.

    The details threads wait for work to be added to the queue and then pull
    the details for each ```WebAppAuthRecord.id```.

    Args:
        auth (BasicAuth): The authentication object.
        thread_count (int): The number of threads to spawn. Defaults to 5.

    ## Kwargs:

        - id (Union[str, int]): Authentication object ID.
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): Auth object name.
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the name filter.
        - tags (Union[str, int]): Tag ID.
        - tags_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tags filter.
        - tags_name (str): Tag name.
        - tags_name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the tag name filter.
        - tags_id (Union[str, int]): Tag ID.
        - tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tag ID filter.
        - createdDate (str): Date the Auth object was created in UTC date/time format.
        - createdDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the created date filter.
        - updatedDate (str): Date the Auth object was last updated in UTC date/time format.
        - updatedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the updated date filter.
        - isUsed (bool): Whether the Auth object is in use.
        - isUsed (Literal["EQUALS", "NOT EQUALS"]): Operator for the isUsed filter.
        - lastScan_authStatus (Literal["NONE", "NOT_USED", "PARTIAL", "FAILED", "SUCCESSFUL"]): Status of the last scan.
        - lastScan_authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the last scan status filter.
        - lastScan_date (str): Date of the last scan in UTC date/time format.
        - lastScan_date_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the last scan date filter.
        - contents (Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]): Auth object contents.
        - contents_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the contents filter.

    Returns:
        BaseList[WebAppAuthRecord]: The list of auth records.
    """

    # Check thread_count for a valid value:
    if not isinstance(thread_count, int) or thread_count < 1:
        raise ValueError("thread_count must be an integer >= 1.")

    # Set up Queue and List, with some cheeky as-needed imports:
    from queue import Queue
    from threading import Thread, Lock, current_thread

    q = Queue()
    authList = BaseList()
    LOCK = Lock()
    threads = []

    # Get the auth records:
    print(f"({current_thread().name}) Getting base auth record list...")
    authrecords = get_authentication_records(auth, page_count="all", **kwargs)

    print(
        f"({current_thread().name}) Pulled {len(authrecords)} auth records. Starting {thread_count} thread(s) for details pull.."
    )

    # Add the auth records to the queue:
    for record in authrecords:
        q.put(record)

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

                authrecord = q.get()
                # Exit condition 2: authrecord is None (because Queue is empty)
                if not authrecord:
                    with LOCK:
                        print(
                            f"({current_thread().name}) Queue is empty. Thread exiting."
                        )
                        q.task_done()
                    break

                details = get_authentication_record_details(auth, authrecord.id)
                authList.append(details)
                q.task_done()
                with LOCK:
                    if len(authList) % 10 == 0:
                        print(
                            f"({current_thread().name}) Pulled {len(authList)} auth record details so far..."
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

    print(f"Pulled {len(authList)} auth record details.")
    return authList
