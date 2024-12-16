"""
Contains functions to interact with Web applications in the Qualys WAS module.
"""

from typing import Union

from .data_classes.WebApp import WebApp
from .base.web_app_service_requests import build_service_request, build_update_request
from .base.parse_kwargs import validate_kwargs
from .base.web_app_service_requests import validate_response
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
        case "update_webapp":
            params = {"placeholder": "update", "webappId": payload.pop("webappId")}
        case "delete_webapp":
            params = {"placeholder": "delete", "webappId": ""}
            if payload.pop("removeFromSubscription", None):
                params["action"] = "removeFromSubscription"
        case "get_selenium_script":
            params = {"placeholder": "downloadSeleniumScript", "webappId": ""}
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
) -> WebApp:
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
        - verbose (bool): If True, returns tag information in the response.

    Returns:
        WebApp: The web applications that match the filters.
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
    webapps = get_webapps(auth, **kwargs)

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
            - domains (Union[str, list[str]]): A single domain or a list of domains to associate with the web application.
            - scannerTag_ids (Union[int, list[int]]): A tag ID representing 1+ scanners to associate with the web application.

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
        _domains=kwargs.get("domains"),
        _scannerTag_ids=kwargs.get("scannerTag.ids"),
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


def update_webapp(auth: BasicAuth, webappId: Union[int, str], **kwargs) -> str:
    """
    Update a WAS web application.

    Args:
        auth (BasicAuth): The authentication object.
        webappId (Union[int, str]): The ID of the web application.

    ## Kwargs:

            - name (str): The name of the web application.
            - url (str): The URL of the web application.
            - attributes (dict["add": {"attr_name": "attr_value"}, "remove": ["attr_name"]]): Dictionary containing a list of attributes to add or remove.)
            - defaultProfile_id (Union[str, int]): The ID of the default profile to associate with the web application.
            - urlExcludelist (list[str]): A list of URLs to exclude from the scan.
            - urlAllowlist (list[str]): A list of URLs to allow in the scan.
            - postDataExcludelist (list[str]): A list of post data to exclude from the scan.
            - useSitemap (bool): Whether to use the sitemap.
            - headers (list[str]): A list of headers to include in the scan.
            - authRecord_id (dict["add": [int], "remove": [int]]): A dictionary containing a list of authentication record IDs to add or remove.

    Returns:
        str: A status message indicating the result of the update.
    """

    # Validate the kwargs:
    kwargs = validate_kwargs(endpoint="update_webapp", **kwargs)

    # Build the XML payload:
    payload = build_update_request(
        _authRecord_id=kwargs.get("authRecord.id"),
        tag_ids=kwargs.get("tag.ids"),
        _domains=kwargs.get("domains"),
        _scannerTag_ids=kwargs.get("scannerTag.ids"),
        defaultProfile_id=kwargs.get("defaultProfile.id"),
        _urlExcludelist=kwargs.get("urlExcludelist"),
        _urlAllowlist=kwargs.get("urlAllowlist"),
        _postDataExcludelist=kwargs.get("postDataExcludelist"),
        _useSitemap=kwargs.get("useSitemap"),
        _headers=kwargs.get("headers"),
        **kwargs,
    )

    # Make the API call:
    payload["webappId"] = webappId
    parsed = call_webapp_api(auth, "update_webapp", payload)

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
        return f"WebaApp {data} updated successfully."
    else:
        print("No data found. Exiting.")


def delete_webapp(
    auth: BasicAuth, removeFromSubscription: bool = True, **kwargs
) -> list[str]:
    """
    Delete webapps out of Qualys WAS.

    To delete a single asset, use kwarg 'id' set to
    a single int/str.

    To delete multiple assets,
    set 'id' to a list of int/str, or use the other
    kwargs/operators listed below.

    If both 'id' and other kwargs are provided, the 'id'
    kwarg will take precedence.

    Args:
        auth (BasicAuth): The authentication object.
        removeFromSubscription (bool): Whether to remove the webapp from the subscription (True) or just WAS (False). Default is True.

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
        list[str]: A list of IDs that were successfully deleted.
    """

    # Make sure user passed in a kwarg:
    if not kwargs:
        raise ValueError("No kwargs provided. Please provide at least one kwarg.")

    TO_STR = [
        "id",
        "tags_id",
    ]

    for key in TO_STR:
        if key in kwargs:
            kwargs[key] = str(kwargs[key])

    # Validate the kwargs:
    kwargs = validate_kwargs(endpoint="delete_webapp", **kwargs)

    # Build the XML payload:
    payload = build_service_request(**kwargs)
    payload["removeFromSubscription"] = removeFromSubscription

    # Make the API call:
    parsed = call_webapp_api(auth, "delete_webapp", payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    if serviceResponse.get("count") == "0":
        print("No applicable web apps found. Exiting.")
        return []

    deleted = []
    data = serviceResponse.get("data")
    if data.get("WebApp"):
        data = data.get("WebApp")
        if isinstance(data, dict):
            data = [data]
        for webapp in data:
            deleted.append(webapp)

    return deleted


def purge_webapp(auth: BasicAuth, **kwargs) -> list[str]:
    """
    Purge webapp scan data out of Qualys WAS.

    To delete a single asset's scan history, use kwarg 'id' set to
    a single int/str.

    To delete multiple assets' scan history,
    set 'id' to a list of int/str, or use the other
    kwargs/operators listed below.

    If both 'id' and other kwargs are provided, the 'id'
    kwarg will take precedence.

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
        list[str]: A list of IDs that had their scan data purged.
    """

    # Make sure user passed in a kwarg:
    if not kwargs:
        raise ValueError("No kwargs provided. Please provide at least one kwarg.")

    TO_STR = [
        "id",
        "tags_id",
    ]

    for key in TO_STR:
        if key in kwargs:
            kwargs[key] = str(kwargs[key])

    # Validate the kwargs. purge uses the same kwargs as delete:
    kwargs = validate_kwargs(endpoint="delete_webapp", **kwargs)

    # Build the XML payload:
    payload = build_service_request(**kwargs)

    # Make the API call:
    parsed = call_webapp_api(auth, "delete_webapp", payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    if serviceResponse.get("count") == "0":
        print("No applicable web apps found. Exiting.")
        return []

    deleted = []
    data = serviceResponse.get("data")
    if data.get("WebApp"):
        data = data.get("WebApp")
        if isinstance(data, dict):
            data = [data]
        for webapp in data:
            deleted.append(webapp)

    return deleted


def get_selenium_script(
    auth: BasicAuth, id: Union[int, str], crawlingScripts_id: Union[int, str]
) -> object:
    """
    Download the associated Selenium script for a web application, identified by 1+ web app IDs.

    Args:
        auth (BasicAuth): The authentication object.
        id (Union[int, str]): The ID of the web application.
        crawlingScripts_id (Union[int, str]): The ID of the crawling script.

    Returns:
        object: The Selenium script.
    """

    # Validate the kwargs:
    validate_kwargs(
        endpoint="get_selenium_script",
        id=id,
        crawlingScripts_id=str(crawlingScripts_id),
    )

    # Format crawlingScripts ID:
    kwargs = {"id": str(id), "crawlingScripts.id": str(crawlingScripts_id)}

    # Build the XML payload:
    payload = build_service_request(**kwargs)

    # Make the API call:
    parsed = call_webapp_api(auth, "get_selenium_script", payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    data = serviceResponse.get("data")
    print(
        "[WARNING] Code to parse data from this endpoint is not yet implemented. Please submit a PR. Returning raw data..."
    )
    return data
    # if data.get("SeleniumScript"):
    #    data = data.get("SeleniumScript")
    #    return data
    # else:
    #    print("No data found. Exiting.")
