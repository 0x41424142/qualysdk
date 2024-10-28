"""
Contains user-facing functions for interacting with authentication records in WAS
"""

from typing import Union, Literal, List, Dict, Optional

from .data_classes.WebAppAuthRecord import WebAppAuthRecord
from .base.auth_record_service_requests import (
    create_service_request,
    unparse_to_xml_str,
)
from .base.web_app_service_requests import build_service_request
from .base.parse_kwargs import validate_kwargs
from .base.web_app_service_requests import validate_response
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
        case "create_authentication_record":
            params = {"placeholder": "create", "webappAuthRecordId": ""}
        case "delete_authentication_record":
            params = {"placeholder": "delete", "webappAuthRecordId": ""}
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
    authrecords = get_authentication_records(auth, **kwargs)

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


"""
format_tag_list takes in a list of ints 
and returns a properly structured list 
of dicts for the API payload.
"""
format_tag_list = lambda tags: [{"id": tag} for tag in tags]


def create_authentication_record(
    auth: BasicAuth,
    name: str,
    recordType: Literal["formRecord", "serverRecord", "oauth2Record"],
    fields: List[Dict[str, Union[str, bool]]] = None,
    subType: Optional[
        Literal[
            "STANDARD",
            "CUSTOM",
            "SELENIUM",
            "BASIC",
            "DIGEST",
            "NTLM",
            "AUTH_CODE",
            "IMPLICIT",
            "PASSWORD",
            "CLIENT_CREDS",
        ]
    ] = None,
    **kwargs,
) -> WebAppAuthRecord:
    """
    Create a new authentication record in WAS

    Args:
        auth (BasicAuth): The authentication object.
        name (str): The name of the authentication record.
        recordType (Literal["formRecord", "serverRecord", "oauth2Record"]): The type of authentication record to create.
        subType (Optional[Literal["STANDARD", "CUSTOM", "SELENIUM", "BASIC", "DIGEST", "NTLM", "AUTH_CODE", "IMPLICIT", "PASSWORD", "CLIENT_CREDS"]]): The subtype of the authentication record to create.
        fields (List[Dict[str, Union[str, bool]]]): The fields to include in the authentication record. Each field should be a dictionary with the keys 'name', 'value', and optionally 'secured'.

    ## Kwargs:

        - tags (List[int]): The tag ID numbers to associate with the authentication record as a list. Default is an empty list.
        - comments (Union[List[str], str]): Comments to associate with the authentication record. Default is an empty list.
        - sslOnly (bool): Whether the authentication record should only be used over encrypted connections. Default is False.
        - authVault (bool): Whether the authentication record should be stored in the Qualys Vault. Default is False.
        - certificate (Dict[str, str]): A dictionary containing the certificate information for the authentication record. Valid for serverRecord records. Example: certificate={"name": "certname", "contents": "certcontents", "passphrase": "certpassphrase"}}.
        - grantType (Literal["AUTH_CODE", "IMPLICIT", "PASSWORD", "CLIENT_CREDS"]): The grant type for the OAuth2 record. Default is None.
        - accessTokenUrl (str): The access token URL for OAuth2 records.
        - redirectUrl (str): The redirect URL for OAuth2 records.
        - username (str): The username for OAuth2/Server records.
        - password (str): The password for OAuth2/Server records.
        - clientId (str): The client ID for OAuth2 records.
        - clientSecret (str): The client secret for OAuth2 records.
        - scope (str): The scope for OAuth2 records.
        - accessTokenExpiredMsgPattern (str): The access token expired message pattern for OAuth2 records.
        - seleniumScript (Dict[str, str]): The Selenium script details for formRecord and OAuth2 records. Example: {"name": "ImplicitScript", "data": "implicit script data", "regex": "implicit regex pattern"}.
        - seleniumCreds (bool): Whether Selenium credentials are used. Default is None.

    Returns:
        WebAppAuthRecord: The created authentication record.
    """

    # Check validity of recordType:
    if recordType not in ["formRecord", "serverRecord", "oauth2Record"]:
        raise ValueError(
            "recordType must be one of 'formRecord', 'serverRecord', or 'oauth2Record'."
        )

    # Check validity of subType:
    acceptable_subtypes_by_recordType = {
        "formRecord": ["STANDARD", "CUSTOM", "SELENIUM"],
        "serverRecord": ["BASIC", "DIGEST", "NTLM", None],
        "oauth2Record": ["AUTH_CODE", "IMPLICIT", "PASSWORD", "CLIENT_CREDS"],
    }
    if subType and subType.upper() not in acceptable_subtypes_by_recordType[recordType]:
        raise ValueError(
            f"subType must be one of {acceptable_subtypes_by_recordType[recordType]} for a {recordType}, not {subType}."
        )

    # Ensure tags is a list
    if not isinstance(kwargs.get("tags", []), list):
        kwargs["tags"] = [kwargs["tags"]]

    # Ensure comments is a list
    if isinstance(kwargs.get("comments", []), str):
        kwargs["comments"] = [kwargs["comments"]]

    # Build the payload:
    payload = {
        "name": name,
        recordType: {
            "type" if recordType != "oauth2Record" else "grantType": subType,
            "sslOnly": kwargs.get("sslOnly"),
            "authVault": kwargs.get("authVault"),
            "fields": {"set": fields},
        },
        "tags": {"set": format_tag_list(kwargs.get("tags", []))},
        "comments": {"set": kwargs.get("comments", [])},
    }

    # Add optional fields based on recordType
    if recordType == "serverRecord" and "certificate" in kwargs:
        payload[recordType]["certificate"] = kwargs["certificate"]

    if recordType == "oauth2Record":
        oauth2_fields = [
            "grantType",
            "accessTokenUrl",
            "redirectUrl",
            "username",
            "password",
            "clientId",
            "clientSecret",
            "scope",
            "accessTokenExpiredMsgPattern",
            "seleniumScript",
            "seleniumCreds",
        ]
        for field in oauth2_fields:
            if field in kwargs:
                payload[recordType][field] = kwargs[field]

    # Create the service request
    xml_payload = unparse_to_xml_str(
        create_service_request(data={"WebAppAuthRecord": payload})
    )

    # Make the API call:
    parsed = call_auth_api(
        auth, "create_authentication_record", {"_xml_data": xml_payload}
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
        print("No data found. Exiting.")


def delete_authentication_record(auth: BasicAuth, **kwargs) -> list[str]:
    """
    Delete authentication records out of Qualys WAS.

    To delete a single record, use kwarg 'id' set to
    a single int/str.

    To delete multiple assets,
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
        - tags (Union[str, int]): Tag ID.
        - tags_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tags filter.
        - tags_name (str): Tag name.
        - tags_name_operator (Literal["CONTAINS", "EQUALS", "NOT EQUALS"]): Operator for the tag name filter.
        - tags_id (Union[str, int]): Tag ID.
        - tags_id_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"]): Operator for the tag ID filter.
        - createdDate (str): Date the web application was created in UTC date/time format.
        - createdDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the created date filter.
        - updatedDate (str): Date the web application was last updated in UTC date/time format.
        - updatedDate_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the updated date filter.
        - lastScan_authStatus (Literal["NONE", "NOT_USED", "SUCCESSFUL", "FAILED", "PARTIAL"]): Status of the last scan.
        - lastScan_authStatus_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the last scan status filter.
        - lastScan_date (str): Date of the last scan in UTC date/time format.
        - lastScan_date_operator (Literal["EQUALS", "NOT EQUALS", "GREATER", "LESSER"]): Operator for the last scan date filter.
        - isUsed (bool): Whether the web application is in use.
        - isUsed_operator (Literal["EQUALS", "NOT EQUALS"]): Operator for the isUsed filter.
        - contents (Literal["FORM_STANDARD", "FORM_CUSTOM", "FORM_SELENIUM", "SERVER_BASIC", "SERVER_DIGEST", "SERVER_NTLM", "CERTIFICATE", "OAUTH2_AUTH_CODE", "OAUTH2_IMPLICIT", "OAUTH2_PASSWORD", "OAUTH2_CLIENT_CREDS"]): Web application contents.
        - contents_operator (Literal["EQUALS", "NOT EQUALS", "IN"]): Operator for the contents filter.

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
    kwargs = validate_kwargs(endpoint="delete_authentication_record", **kwargs)

    # Build the XML payload:
    payload = build_service_request(**kwargs)

    # Make the API call:
    parsed = call_auth_api(auth, "delete_authentication_record", payload)

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        raise QualysAPIError(
            f"API response returned error: {serviceResponse.get('responseCode')}"
        )

    if serviceResponse.get("count") == "0":
        print(f"No auth records found. Exiting.")
        return []

    deleted = []
    data = serviceResponse.get("data")
    if data.get("WebAppAuthRecord"):
        data = data.get("WebAppAuthRecord")
        if isinstance(data, dict):
            data = [data]
        for record in data:
            deleted.append(record)

    return deleted
