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
        kwargs = validate_kwargs(endpoint="count_webapps", **kwargs)
        payload = build_service_request(**kwargs)

    # Make the API call
    response = call_api(
        auth=auth,
        module="was",
        endpoint="count_webapps",
        payload=payload,
        headers={"Content-Type": "text/xml"},
    )

    # Parse the XML response
    parsed = validate_response(response)

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
        # Make the API call
        response = call_api(
            auth=auth,
            module="was",
            endpoint="get_webapps",
            payload=payload,
            headers={"Content-Type": "text/xml"},
        )

        parsed = validate_response(response)

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
