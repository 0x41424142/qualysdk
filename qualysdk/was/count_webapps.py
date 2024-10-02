"""
Contains the count_webapps method for the WAS module.
"""

from typing import Union, Literal
from datetime import datetime

from .base.parse_kwargs import validate_kwargs
from ..base.call_api import call_api
from ..base.xml_parser import xml_parser
from ..auth.basic import BasicAuth
from ..exceptions.Exceptions import QualysAPIError


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

        """
        Build the XML request. Users pass in the filters as kwargs.
        there is the filter itself as well as a filter_operator kwarg.
        If the filter_operator is not provided, default to "EQUALS". 
        Do not create a Criteria tag for any _operator kwargs.
        """
        xml = "<ServiceRequest><filters>{REPLACE}</filters></ServiceRequest>"
        user_xml = ""
        for kwarg, value in kwargs.items():
            if kwarg.endswith("operator"):
                continue
            user_xml += f'<Criteria field="{kwarg}" operator="{kwargs.get(kwarg + ".operator", "EQUALS")}">{value}</Criteria>'

        xml = xml.replace("{REPLACE}", user_xml)
        payload = {"_xml_data": xml}

    # Make the API call
    response = call_api(
        auth=auth,
        module="was",
        endpoint="count_webapps",
        payload=payload,
        headers={"Content-Type": "text/xml"},
    )

    # Parse the XML response
    parsed = xml_parser(response.text)

    if response.status_code != 200:
        errorMessage = (
            parsed.get("ServiceResponse")
            .get("responseErrorDetails")
            .get("errorMessage")
        )
        responseCode = parsed.get("ServiceResponse").get("responseCode")
        raise QualysAPIError(
            f"Error retrieving web application count. Status code: {response.status_code}. Endpoint reporting: {responseCode}. Error message: {errorMessage}"
        )

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    return int(serviceResponse.get("count"))
