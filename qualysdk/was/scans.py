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
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}")

    response = call_api(
        auth=auth,
        override_method="GET" if endpoint == "get_finding_details" else "POST",
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
