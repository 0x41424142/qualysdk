"""
Work with Qualys WAS findings
"""

from typing import Union, List, Dict, Literal

from .data_classes.Finding import WASFinding
from .base.parse_kwargs import validate_kwargs
from .base.web_app_service_requests import build_service_request
from ..auth.basic import BasicAuth
from ..base.call_api import call_api
from .base.web_app_service_requests import validate_response
from ..exceptions.Exceptions import QualysAPIError
from ..base.base_list import BaseList


def call_findings_api(
    auth: BasicAuth, endpoint: str, payload: dict
) -> Union[int, BaseList[WASFinding], WASFinding]:
    """
    Call the Qualys WAS findings API

    Args:
        auth (BasicAuth): The authentication object
        endpoint (str): The endpoint to call
        payload (dict): The payload to send

    Returns:
        Union[int, BaseList[WASFinding], WASFinding]: The response from the API
    """

    match endpoint:
        case "count_findings":
            params = {"placeholder": "count", "findingId": ""}
        case "get_findings":
            params = {"placeholder": "search", "findingId": ""}
        case "get_finding_details":
            params = {"placeholder": "get", "findingId": payload.pop("findingId")}
        case _:
            raise ValueError("Invalid endpoint: {endpoint}")

    response = call_api(
        auth=auth,
        override_method="GET" if endpoint == "get_finding_details" else "POST",
        module="was",
        endpoint="call_findings_api",
        payload=payload,
        params=params,
        headers={"Content-Type": "text/xml"},
    )

    return validate_response(response)


def count_findings(auth: BasicAuth, **kwargs) -> int:
    """
    Count how many findings are in the Qualys WAS module
    according to the filters provided

    Args:
        auth (BasicAuth): The authentication object

    ## Kwargs:

        - id (int): The finding ID
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - uniqueId (str): The unique ID of the finding
        - qid (int): The Qualys ID of the finding
        - qid_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the QID filter.
        - name (str): The name of the finding
        - name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the name filter.
        - type (Literal["VULNERABILITY", "SENSITIVE_CONTENT", "INFORMATION_GATHERED"]): The type of the finding
        - type_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the type filter.
        - url (str): The URL of the finding
        - url_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the URL filter.
        - webApp_tags_id (int): The ID of the web application tag on a web application
        - webApp_tags_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the webApp_tags_id filter.
        - webApp_tags_name (str): The name of a web application tag on a web application
        - webApp_tags_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp_tags_name filter.
        - status (Literal["NEW", "ACTIVE", "REOPENED", "PROTECTED", "FIXED"]): The status of the finding
        - status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the status filter.
        - patch (int): Use WAF to protect against vulnerabilities by installing virtual patches
        - patch_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the patch filter.
        - webApp_id (int): The ID of the web application
        - webApp_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the webApp_id filter.
        - webApp_name (str): The name of the web application
        - webApp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp_name filter.
        - severity (Literal[1, 2, 3, 4, 5]): The severity of the finding
        - severity_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the severity filter.
        - externalRef (str): The external reference of the finding
        - externalRef_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the externalRef filter.
        - ignoredDate (str): The date the finding was ignored as a UTC timestamp
        - ignoredDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ignoredDate filter.
        - ignoredReason (Literal["FALSE_POSITIVE", "RISK_ACCEPTED", "NOT_APPLICABLE"]): The reason the finding was ignored
        - ignoredReason_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the ignoredReason filter.
        - group (Literal["XSS", "SQL", "INFO", "PATH", "CC", "SSN_US", "CUSTOM"]): The group of the finding
        - group_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the group filter.
        - owasp_name (str): The OWASP name of the finding
        - owasp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the owasp_name filter.
        - owasp_code (int): The OWASP code of the finding
        - owasp_code_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the owasp_code filter.
        - wasc_name (str): The WASC name of the finding
        - wasc_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the wasc_name filter.
        - wasc_code (int): The WASC code of the finding
        - wasc_code_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the wasc_code filter.
        - cwe_id (int): The CWE ID of the finding
        - cwe_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the cwe_id filter.
        - firstDetectedDate (str): The date the finding was first detected as a UTC timestamp
        - firstDetectedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the firstDetectedDate filter.
        - lastDetectedDate (str): The date the finding was last detected as a UTC timestamp
        - lastDetectedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the lastDetectedDate filter.
        - lastTestedDate (str): The date the finding was last tested as a UTC timestamp
        - lastTestedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the lastTestedDate filter.
        - timesDetected (int): The number of times the finding was detected
        - timesDetected_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the timesDetected filter.

    Returns:
        int: Number of findings
    """

    payload = None

    if kwargs:
        for key, value in kwargs.items():
            # cast all to string:
            kwargs[key] = str(value)
        kwargs = validate_kwargs(endpoint="count_findings", **kwargs)

        payload = build_service_request(**kwargs)

    # Make the API call
    parsed = call_findings_api(auth=auth, endpoint="count_findings", payload=payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response code was not SUCCESS: {serviceResponse.get('responseCode')}"
        )

    return int(serviceResponse.get("count"))


def get_findings(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> BaseList[WASFinding]:
    """
    Get a list of findings from Qualys WAS according
    to the filters provided

    Args:
        auth (BasicAuth): The authentication object
        page_count (Union[int, "all"]): The number of pages to retrieve. Default is "all"

    ## Kwargs:

        - id (int): The finding ID
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - uniqueId (str): The unique ID of the finding
        - qid (int): The Qualys ID of the finding
        - qid_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the QID filter.
        - name (str): The name of the finding
        - name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the name filter.
        - type (Literal["VULNERABILITY", "SENSITIVE_CONTENT", "INFORMATION_GATHERED"]): The type of the finding
        - type_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the type filter.
        - url (str): The URL of the finding
        - url_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the URL filter.
        - webApp_tags_id (int): The ID of the web application tag on a web application
        - webApp_tags_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the webApp_tags_id filter.
        - webApp_tags_name (str): The name of a web application tag on a web application
        - webApp_tags_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp_tags_name filter.
        - status (Literal["NEW", "ACTIVE", "REOPENED", "PROTECTED", "FIXED"]): The status of the finding
        - status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the status filter.
        - patch (int): Use WAF to protect against vulnerabilities by installing virtual patches
        - patch_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the patch filter.
        - webApp_id (int): The ID of the web application
        - webApp_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the webApp_id filter.
        - webApp_name (str): The name of the web application
        - webApp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp_name filter.
        - severity (Literal[1, 2, 3, 4, 5]): The severity of the finding
        - severity_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the severity filter.
        - externalRef (str): The external reference of the finding
        - externalRef_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the externalRef filter.
        - ignoredDate (str): The date the finding was ignored as a UTC timestamp
        - ignoredDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ignoredDate filter.
        - ignoredReason (Literal["FALSE_POSITIVE", "RISK_ACCEPTED", "NOT_APPLICABLE"]): The reason the finding was ignored
        - ignoredReason_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the ignoredReason filter.
        - group (Literal["XSS", "SQL", "INFO", "PATH", "CC", "SSN_US", "CUSTOM"]): The group of the finding
        - group_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the group filter.
        - owasp_name (str): The OWASP name of the finding
        - owasp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the owasp_name filter.
        - owasp_code (int): The OWASP code of the finding
        - owasp_code_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the owasp_code filter.
        - wasc_name (str): The WASC name of the finding
        - wasc_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the wasc_name filter.
        - wasc_code (int): The WASC code of the finding
        - wasc_code_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the wasc_code filter.
        - cwe_id (int): The CWE ID of the finding
        - cwe_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the cwe_id filter.
        - firstDetectedDate (str): The date the finding was first detected as a UTC timestamp
        - firstDetectedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the firstDetectedDate filter.
        - lastDetectedDate (str): The date the finding was last detected as a UTC timestamp
        - lastDetectedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the lastDetectedDate filter.
        - lastTestedDate (str): The date the finding was last tested as a UTC timestamp
        - lastTestedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the lastTestedDate filter.
        - timesDetected (int): The number of times the finding was detected
        - timesDetected_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the timesDetected filter.
        - fixedDate (str): The date the finding was fixed as a UTC timestamp
        - fixedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the fixedDate filter.
        - verbose (bool): Whether to return verbose output

    Returns:
        BaseList[WASFinding]: A list of WASFinding objects
    """

    if page_count != "all" and not (isinstance(page_count, int) or page_count < 0):
        raise ValueError("page_count must be 'all' or a positive integer")

    pageNo = 0
    payload = None

    # If kwargs are provided, validate them:
    if kwargs:
        kwargs = validate_kwargs(endpoint="get_findings", **kwargs)
        payload = build_service_request(**kwargs)

    findingList = BaseList()

    while True:
        # Make the API call:
        parsed = call_findings_api(auth, "get_findings", payload)

        # Parse the XML response:
        serviceResponse = parsed.get("ServiceResponse")
        if not serviceResponse:
            raise QualysAPIError("No ServiceResponse tag returned in the API response")

        if serviceResponse.get("responseCode") != "SUCCESS":
            raise QualysAPIError(
                f"API response returned error: {serviceResponse.get('responseCode')}"
            )

        if serviceResponse.get("count") == "0":
            print(f"No findings found on page {pageNo}. Exiting.")
            break

        data = serviceResponse.get("data")

        if data.get("Finding"):
            data = data.get("Finding")

        if isinstance(data, dict):
            data = [data]

        for finding in data:
            # Create the objects:
            findingList.append(WASFinding.from_dict(finding))

        print(
            f"Retrieved {serviceResponse.get('count')} WAS findings on page {pageNo}. Running total: {len(findingList)}"
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

    return findingList


def get_finding_details(auth: BasicAuth, findingId: Union[str, int]) -> WASFinding:
    """
    Pull all details of a single finding from Qualys WAS
    by its finding # or unique ID

    Args:
        auth (BasicAuth): The authentication object
        findingId (Union[str, int]): The finding number or unique ID of the finding

    Returns:
        WASFinding: The WASFinding object
    """

    if not isinstance(findingId, (str, int)):
        raise ValueError("findingId must be a string or integer")

    # Make the API call
    parsed = call_findings_api(auth, "get_finding_details", {"findingId": findingId})

    # Parse the XML response:
    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    data = serviceResponse.get("data")

    if data.get("Finding"):
        data = data.get("Finding")

    return WASFinding.from_dict(data)


def get_findings_verbose(
    auth: BasicAuth, thread_count: int = 5, **kwargs
) -> BaseList[WASFinding]:
    """
    Uses ```was.get_findings()``` and ```was.get_finding_details()``` to return a ```BaseList``` of ```WASFinding```s with
    all attributes populated.

    This function is multi-threaded, placing all ```WASFinding```s found
    from ```was.get_findings()``` into a queue and then spawning threads to pull the details one
    by one.

    The details threads wait for work to be added to the queue and then pull
    the details for each ```WASFinding.id```.

    Args:
        auth (BasicAuth): The authentication object.
        thread_count (int): The number of threads to spawn. Defaults to 5.

    ## Kwargs:

        - id (int): The finding ID
        - id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ID filter.
        - uniqueId (str): The unique ID of the finding
        - qid (int): The Qualys ID of the finding
        - qid_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the QID filter.
        - name (str): The name of the finding
        - name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the name filter.
        - type (Literal["VULNERABILITY", "SENSITIVE_CONTENT", "INFORMATION_GATHERED"]): The type of the finding
        - type_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the type filter.
        - url (str): The URL of the finding
        - url_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the URL filter.
        - webApp_tags_id (int): The ID of the web application tag on a web application
        - webApp_tags_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the webApp_tags_id filter.
        - webApp_tags_name (str): The name of a web application tag on a web application
        - webApp_tags_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp_tags_name filter.
        - status (Literal["NEW", "ACTIVE", "REOPENED", "PROTECTED", "FIXED"]): The status of the finding
        - status_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the status filter.
        - patch (int): Use WAF to protect against vulnerabilities by installing virtual patches
        - patch_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the patch filter.
        - webApp_id (int): The ID of the web application
        - webApp_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the webApp_id filter.
        - webApp_name (str): The name of the web application
        - webApp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the webApp_name filter.
        - severity (Literal[1, 2, 3, 4, 5]): The severity of the finding
        - severity_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the severity filter.
        - externalRef (str): The external reference of the finding
        - externalRef_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the externalRef filter.
        - ignoredDate (str): The date the finding was ignored as a UTC timestamp
        - ignoredDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the ignoredDate filter.
        - ignoredReason (Literal["FALSE_POSITIVE", "RISK_ACCEPTED", "NOT_APPLICABLE"]): The reason the finding was ignored
        - ignoredReason_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the ignoredReason filter.
        - group (Literal["XSS", "SQL", "INFO", "PATH", "CC", "SSN_US", "CUSTOM"]): The group of the finding
        - group_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the group filter.
        - owasp_name (str): The OWASP name of the finding
        - owasp_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the owasp_name filter.
        - owasp_code (int): The OWASP code of the finding
        - owasp_code_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the owasp_code filter.
        - wasc_name (str): The WASC name of the finding
        - wasc_name_operator (Literal["EQUALS", "NOT EQUALS", "CONTAINS"]): Operator for the wasc_name filter.
        - wasc_code (int): The WASC code of the finding
        - wasc_code_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the wasc_code filter.
        - cwe_id (int): The CWE ID of the finding
        - cwe_id_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the cwe_id filter.
        - firstDetectedDate (str): The date the finding was first detected as a UTC timestamp
        - firstDetectedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the firstDetectedDate filter.
        - lastDetectedDate (str): The date the finding was last detected as a UTC timestamp
        - lastDetectedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the lastDetectedDate filter.
        - lastTestedDate (str): The date the finding was last tested as a UTC timestamp
        - lastTestedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the lastTestedDate filter.
        - timesDetected (int): The number of times the finding was detected
        - timesDetected_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the timesDetected filter.
        - fixedDate (str): The date the finding was fixed as a UTC timestamp
        - fixedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the fixedDate filter.

    Returns:
        BaseList[WASFinding]: The list of WASFinding objects.
    """

    # Check thread_count for a valid value:
    if not isinstance(thread_count, int) or thread_count < 1:
        raise ValueError("thread_count must be an integer >= 1.")

    # Set up Queue and List, with some cheeky as-needed imports:
    from queue import Queue
    from threading import Thread, Lock, current_thread

    q = Queue()
    findingList = BaseList()
    LOCK = Lock()
    threads = []

    # Get the findings:
    print(f"({current_thread().name}) Getting base finding list...")
    findings = get_findings(auth, **kwargs)

    print(
        f"({current_thread().name}) Pulled {len(findings)} findings. Starting {thread_count} thread(s) for details pull.."
    )

    # Add the findings to the queue:
    for record in findings:
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

                finding = q.get()
                # Exit condition 2: authrecord is None (because Queue is empty)
                if not finding:
                    with LOCK:
                        print(
                            f"({current_thread().name}) Queue is empty. Thread exiting."
                        )
                        q.task_done()
                    break

                details = get_finding_details(auth, finding.id)
                findingList.append(details)
                q.task_done()
                with LOCK:
                    if len(findingList) % 10 == 0:
                        print(
                            f"({current_thread().name}) Pulled {len(findingList)} finding details so far..."
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

    print(f"Pulled {len(findingList)} finding details.")
    return findingList
