"""
Contains functions to interact with Web applications in the Qualys WAS module.
"""

from typing import Union

from .data_classes.WebApp import WebApp
from .base.service_requests import build_service_request
from .base.parse_kwargs import validate_kwargs
from .base.service_requests import validate_response
from ..base.call_api import call_api
from ..auth.basic import BasicAuth
from ..exceptions.Exceptions import QualysAPIError
from ..base.base_list import BaseList


def call_webapp_api(
    auth: BasicAuth, endpoint: str, payload: dict
) -> Union[int, WebApp]:
    """
    Call a Qualys WAS API endpoint and return the parsed response. This is
    a backend function and should not be called directly.

    Args:
        auth (BasicAuth): The authentication object.
        endpoint (str): The API endpoint to call.
        payload (dict): The payload to send to the API.

    Returns:
        Union[int, WebApp]: The parsed response from the API.
    """

    match endpoint:
        case "count_webapps":
            params = {"placeholder": "count", "webappId": ""}
        case "get_webapps":
            params = {"placeholder": "search", "webappId": ""}
        case "get_webapp_details":
            params = {"placeholder": "get", "webappId": payload.pop("webappId")}
        case "create_webapp":
            params = {"placeholder": "create", "webappId": ""}
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}")

    response = call_api(
        auth=auth,
        override_method="GET" if endpoint == "get_webapp_details" else "POST",
        module="was",
        endpoint="call_webapp_api",
        params=params,
        payload=payload,
        headers={"Content-Type": "text/xml"},
    )

    return validate_response(response)


def count_webapps(auth: BasicAuth, **kwargs) -> int:
    """
    Return a count of web applications in the Qualys WAS module
    according to the provided filters.

    Args:
        auth (BasicAuth): The authentication object.

    ## Kwargs:

        - id (Union[str, int]): Web application ID.
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): Web application name.
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the name filter.
        - url (str): Web application URL.
        - url_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the URL filter.
        - tags_name (str): Tag name.
        - tags_name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the tag name filter.
        - tags_id (Union[str, int]): Tag ID.
        - tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tag ID filter.
        - createdDate (str): Date the web application was created in UTC date/time format.
        - createdDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the created date filter.
        - updatedDate (str): Date the web application was last updated in UTC date/time format.
        - updatedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the updated date filter.
        - isScheduled (bool): Whether the web application has a scan scheduled.
        - isScheduled_operator (Literal["EQUALS", "NOT EQUALS"]): Operator for the isScheduled filter.
        - isScanned (bool): Whether the web application has been scanned.
        - isScanned_operator (Literal["EQUALS", "NOT EQUALS"]): Operator for the isScanned filter.
        - lastScan_status (Literal["SUBMITTED", "RUNNING", "FINISHED", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "ERROR", "CANCELLED"]): Status of the last scan.
        - lastScan_status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the last scan status filter.
        - lastScan_date (str): Date of the last scan in UTC date/time format.
        - lastScan_date_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the last scan date filter.

    Returns:
        int: The count of web applications that match the filters.
    """

    payload = None

    # If kwargs are provided, validate them:
    if kwargs:
        # kwargs = validate_kwargs(endpoint="count_webapps", **kwargs)
        kwargs = validate_kwargs(endpoint="count_webapps", **kwargs)
        payload = build_service_request(**kwargs)

    # Make the API call:
    parsed = call_webapp_api(auth, "count_webapps", payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    return int(serviceResponse.get("count"))


def get_webapps(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> object:
    """
    Get a list of web applications in the Qualys WAS module
    according to the provided filters.

    Args:
        auth (BasicAuth): The authentication object.
        page_count (int): The number of pages to return. If 'all', return all pages. Default is 'all'.

    ## Kwargs:

        - id (Union[str, int]): Web application ID.
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): Web application name.
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the name filter.
        - url (str): Web application URL.
        - url_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the URL filter.
        - tags_name (str): Tag name.
        - tags_name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the tag name filter.
        - tags_id (Union[str, int]): Tag ID.
        - tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tag ID filter.
        - createdDate (str): Date the web application was created in UTC date/time format.
        - createdDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the created date filter.
        - updatedDate (str): Date the web application was last updated in UTC date/time format.
        - updatedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the updated date filter.
        - isScheduled (bool): Whether the web application has a scan scheduled.
        - isScheduled_operator (Literal["EQUALS", "NOT EQUALS"]): Operator for the isScheduled filter.
        - isScanned (bool): Whether the web application has been scanned.
        - isScanned_operator (Literal["EQUALS", "NOT EQUALS"]): Operator for the isScanned filter.
        - lastScan_status (Literal["SUBMITTED", "RUNNING", "FINISHED", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "ERROR", "CANCELLED"]): Status of the last scan.
        - lastScan_status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the last scan status filter.
        - lastScan_date (str): Date of the last scan in UTC date/time format.
        - lastScan_date_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the last scan date filter.
        - verbose (bool): Whether to return verbose output.

    Returns:
        object: The web applications that match the filters.
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
        kwargs = validate_kwargs(endpoint="get_webapps", **kwargs)
        payload = build_service_request(**kwargs)

    appList = BaseList()

    while True:
        # Make the API call:
        parsed = call_webapp_api(auth, "get_webapps", payload)

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

        if data.get("WebApp"):
            data = data.get("WebApp")

        if isinstance(data, dict):
            data = [data]

        for webapp in data:
            # Create the objects:
            appList.append(WebApp.from_dict(webapp))

        print(
            f"Retrieved {serviceResponse.get('count')} web applications on page {pageNo}. Running total: {len(appList)}"
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


def get_webapp_details(
    auth: BasicAuth, webappId: Union[int, str]
) -> Union[WebApp, None]:
    """
    Get the details of a single web application in the Qualys WAS module.

    Args:
        auth (BasicAuth): The authentication object.
        webappId (Union[int, str]): The ID of the web application.

    Returns:
        WebApp: The web application details.
    """

    # Make the API call:
    parsed = call_webapp_api(auth, "get_webapp_details", {"webappId": webappId})

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    data = serviceResponse.get("data")
    if data.get("WebApp"):
        data = data.get("WebApp")
        return WebApp.from_dict(data)
    else:
        print(f"No data found for web application ID {webappId}. Exiting.")


def get_webapps_verbose(
    auth: BasicAuth, thread_count: int = 5, **kwargs
) -> BaseList[WebApp]:
    """
    Uses ```was.get_webapps()``` and ```was.get_webapp_details()``` to return a ```BaseList``` of ```WebApp```s with
    all attributes populated.

    This function is multi-threaded, placing all ```WebApps``` found
    from ```was.get_webapps()``` into a queue and then spawning threads to pull the details one
    by one.

    The details threads wait for work to be added to the queue and then pull
    the details for each ```WebApp.id```.

    Args:
        auth (BasicAuth): The authentication object.
        thread_count (int): The number of threads to spawn. Defaults to 5.

    ## Kwargs:

        - id (Union[str, int]): Web application ID.
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - name (str): Web application name.
        - name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the name filter.
        - url (str): Web application URL.
        - url_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the URL filter.
        - tags_name (str): Tag name.
        - tags_name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the tag name filter.
        - tags_id (Union[str, int]): Tag ID.
        - tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tag ID filter.
        - createdDate (str): Date the web application was created in UTC date/time format.
        - createdDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the created date filter.
        - updatedDate (str): Date the web application was last updated in UTC date/time format.
        - updatedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the updated date filter.
        - isScheduled (bool): Whether the web application has a scan scheduled.
        - isScheduled_operator (Literal["EQUALS", "NOT EQUALS"]): Operator for the isScheduled filter.
        - isScanned (bool): Whether the web application has been scanned.
        - isScanned_operator (Literal["EQUALS", "NOT EQUALS"]): Operator for the isScanned filter.
        - lastScan_status (Literal["SUBMITTED", "RUNNING", "FINISHED", "TIME_LIMIT_EXCEEDED", "SCAN_NOT_LAUNCHED", "SCANNER_NOT_AVAILABLE", "ERROR", "CANCELLED"]): Status of the last scan.
        - lastScan_status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the last scan status filter.
        - lastScan_date (str): Date of the last scan in UTC date/time format.
        - lastScan_date_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the last scan date filter.

    Returns:
        BaseList[WebApp]: The list of web applications.
    """

    # Check thread_count for a valid value:
    if not isinstance(thread_count, int) or thread_count < 1:
        raise ValueError("thread_count must be an integer >= 1.")

    # Set up Queue and List, with some cheeky as-needed imports:
    from queue import Queue
    from threading import Thread, Lock, current_thread

    q = Queue()
    appList = BaseList()
    LOCK = Lock()
    threads = []

    # Get the webapps:
    print(f"({current_thread().name}) Getting base Webapp list...")
    webapps = get_webapps(auth, page_count="all", **kwargs)

    print(
        f"({current_thread().name}) Pulled {len(webapps)} webapps. Starting {thread_count} thread(s) for details pull.."
    )

    # Add the webapps to the queue:
    for webapp in webapps:
        q.put(webapp)

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

                webapp = q.get()
                # Exit condition 2: webapp is None (because Queue is empty)
                if not webapp:
                    with LOCK:
                        print(
                            f"({current_thread().name}) Queue is empty. Thread exiting."
                        )
                        q.task_done()
                    break

                details = get_webapp_details(auth, webapp.id)
                appList.append(details)
                q.task_done()
                with LOCK:
                    if len(appList) % 10 == 0:
                        print(
                            f"({current_thread().name}) Pulled {len(appList)} webapp details so far..."
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

    print(f"Pulled {len(appList)} webapp details.")
    return appList


def create_webapp(auth: BasicAuth, name: str, url: str, **kwargs) -> WebApp:
    """
    Create a new WAS web application.

    Args:
        auth (BasicAuth): The authentication object.
        name (str): The name of the web application.
        url (str): The URL of the web application.

    ## Kwargs:

            - authRecord_id (Union[str, int]): A single authentication record ID to associate with the web application.
            - uris (Union[str, list[str]]): A list or comma-separated string of URIs to associate with the web application.
            - tag_ids (Union[int, list[int]]): A single tag ID or a list of tag IDs to associate with the web application.

    Returns:
        WebApp: The new web application as a qualysdk WAS WebApp object.
    """

    kwargs["name"] = name
    kwargs["url"] = url

    # Validate the kwargs:
    kwargs = validate_kwargs(endpoint="create_webapp", **kwargs)

    # Build the XML payload:
    payload = build_service_request(
        _webapp_creation_or_edit=True,
        authRecord_id=kwargs.get("authRecord.id"),
        _uris=kwargs.get("uris"),
        tag_ids=kwargs.get("tag.ids"),
        **kwargs,
    )

    # Make the API call:
    parsed = call_webapp_api(auth, "create_webapp", payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    data = serviceResponse.get("data")
    if data.get("WebApp"):
        data = data.get("WebApp")
        return WebApp.from_dict(data)
    else:
        print("No data found. Exiting.")
