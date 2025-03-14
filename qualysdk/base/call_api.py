"""
call_api.py - contains the call_api function for the qualysdk package.

This function handles all API calls to the Qualys API. It takes in a URL, headers, and a payload, and returns the response from the API.
Qualys uses many tricks in their API, such as using both url params and post data.
"""

from requests import request, Response
from typing import Literal, Union
from datetime import datetime, timedelta
from time import sleep

from ..auth.token import TokenAuth
from ..auth.basic import BasicAuth
from ..exceptions.Exceptions import *
from .call_schema import CALL_SCHEMA
from .convert_bools_and_nones import convert_bools_and_nones
from .xml_parser import xml_parser


def call_api(
    auth: Union[BasicAuth, TokenAuth],
    module: str,
    endpoint: str,
    headers: dict = None,
    params: dict = None,
    payload: dict = None,
    jsonbody: dict = None,
    override_method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = None,
) -> Response:
    """
    Base call function for the Qualys API.

    This function is used across all modules and endpoints as the actual
    API call function.

    Params:
    ```
    auth (Union[BasicAuth, TokenAuth]) The authentication object.
    module (str) The module to call using the CALL_SCHEMA.
    endpoint (str) The endpoint to call using the CALL_SCHEMA.
    headers (dict) The headers to send.
    payload (dict) The payload to send.
    params (dict) The parameters to send.
    jsonbody (dict) The JSON body to send.
    override_method (Literal["GET", "POST", "PUT", "PATCH", "DELETE"]) The method to override the schema with.
    ```
    """
    while True:  # loop to handle hitting the rate limit
        # check module and endpoint:
        if module.lower() not in CALL_SCHEMA.keys():
            raise ValueError(
                f"Invalid module {module}. Valid modules are: {CALL_SCHEMA.keys()}."
            )
        if endpoint.lower() not in CALL_SCHEMA[module].keys():
            raise ValueError(
                f"Invalid endpoint {endpoint} for module {module}. Valid endpoints are: {[i for i in CALL_SCHEMA[module].keys() if i != 'url_type']}."
            )

        SCHEMA = CALL_SCHEMA[module][endpoint]

        # check the auth type:
        if SCHEMA["auth_type"] != auth.auth_type:
            raise AuthTypeMismatchError(
                f"Auth type mismatch. Expected {SCHEMA['auth_type']} but got {auth.auth_type}."
            )

        # check override:
        if override_method:
            if override_method.upper() not in SCHEMA["method"]:
                raise ValueError(
                    f"Invalid override method {override_method}. Valid methods are: {SCHEMA['method']}."
                )

        # match the url_type to get the proper template:
        match CALL_SCHEMA[module]["url_type"]:
            case "gateway":
                url = f"https://gateway.{auth.platform}.apps.qualys.com{SCHEMA['endpoint']}"
            case "api":
                if (
                    auth.platform == "qg1"
                ):  # Special case for qg1 platform: no qg or apps in the URL
                    url = f"https://qualysapi.qualys.com{SCHEMA['endpoint']}"
                else:
                    url = f"https://qualysapi.{auth.platform}.apps.qualys.com{SCHEMA['endpoint']}"
            case "base":
                if auth.platform == "qg1":
                    url = f"https://qualysguard.qualys.com{SCHEMA['endpoint']}"
                else:
                    url = f"https://qualysguard.{auth.platform}.apps.qualys.com{SCHEMA['endpoint']}"
            case _:
                raise ValueError(f"Invalid url_type {SCHEMA['url_type']}.")

        # if token auth, check if token is not 4+ hours old:
        if isinstance(auth, TokenAuth):
            # check that the time delta between now and the token generation time is less than ~4 hours:
            if (datetime.now() - auth.generated_on).seconds > 14395:
                print("Token is 4+ hours old. Refreshing token...")
                auth.token = auth.get_token()

        # check params:
        if params:
            for key in params.keys():
                if key not in SCHEMA["valid_params"]:
                    raise ValueError(
                        f"Invalid parameter {key} for {module}-{endpoint}. Valid parameters are: {SCHEMA['valid_params'].sort() if SCHEMA['valid_params'].sort() else SCHEMA['valid_params']}."
                    )

        # check post data:
        if payload:
            for key in payload.keys():
                if key not in SCHEMA["valid_POST_data"]:
                    raise ValueError(
                        f"Invalid payload key {key} for {module}-{endpoint}."
                    )

        # check if data should be POSTed as requests.post(json=):
        if SCHEMA["use_requests_json_data"]:
            use_json = True
        else:
            use_json = False

        # set up JWT auth header if needed:
        if auth.auth_type == "token":
            if not headers:
                headers = auth.as_header()
            else:
                headers["Authorization"] = auth.as_header()["Authorization"]
        # or set up the tuple for basic auth:
        elif auth.auth_type == "basic":
            auth_tuple = (auth.username, auth.password)

        # Make certain payloads/params requests-friendly:
        # TODO: need to evaluate other modules this may apply to.
        if module != "pm":
            if payload:
                payload = convert_bools_and_nones(payload)
            if params:
                params = convert_bools_and_nones(params)

        # If the URL of an endpoint has the substring
        # {placeholder}, .pop() from the params/payload
        # and format the url with the value:
        if any(
            keyword in url
            for keyword in [
                "{placeholder}",
                "{cloudprovider}",
                "{connectorid}",
                "{controlid}",
                "{webappId}",
                "{findingId}",
                "{scanId}",
                "{tagId}",
            ]
        ):
            if params and (
                any(
                    keyword in params
                    for keyword in [
                        "placeholder",
                        "cloudprovider",
                        "connectorid",
                        "controlid",
                        "webappId",
                        "findingId",
                        "scanId",
                        "tagId",
                    ]
                )
            ):
                url = url.format(
                    placeholder=str(params.pop("placeholder", None)),
                    cloudprovider=str(params.pop("cloudprovider", None)),
                    connectorid=str(params.pop("connectorid", None)),
                    controlid=str(params.pop("controlid", None)),
                    resourceid=str(params.pop("resourceid", None)),
                    webappId=str(params.pop("webappId", None)),
                    webappAuthRecordId=str(params.pop("webappAuthRecordId", None)),
                    findingId=str(params.pop("findingId", None)),
                    scanId=str(params.pop("scanId", None)),
                    tagId=str(params.pop("tagId", None)),
                )
            elif payload and (
                any(
                    keyword in payload
                    for keyword in [
                        "placeholder",
                        "cloudprovider",
                        "connectorid",
                        "controlid",
                        "resourceid",
                        "webappId",
                        "findingId",
                        "scanId",
                        "tagId",
                    ]
                )
            ):
                url = url.format(
                    placeholder=str(payload.pop("placeholder", None)),
                    cloudprovider=str(payload.pop("cloudprovider", None)),
                    connectorid=str(payload.pop("connectorid", None)),
                    controlid=str(payload.pop("controlid", None)),
                    resourceid=str(payload.pop("resourceid", None)),
                    webappId=str(payload.pop("webappId", None)),
                    findingId=str(payload.pop("findingId", None)),
                    scanId=str(payload.pop("scanId", None)),
                    tagId=str(payload.pop("tagId", None)),
                )
            else:
                raise ValueError(
                    f"Endpoint {module}-{endpoint} requires a placeholder or cloudprovider value in the URL however none was found in params/POST data. Base URL is: {url}"
                )

        # If _xml_data key is defined in call schema,
        # use it as the payload/params:
        if payload and SCHEMA.get("_xml_data") and payload.get("_xml_data"):
            payload = payload["_xml_data"]

        if params and SCHEMA.get("_xml_data") and params.get("_xml_data"):
            params = params["_xml_data"]

        # and finally, make the request:
        response = request(
            method=(
                SCHEMA["method"][0] if not override_method else override_method.upper()
            ),
            url=url,
            headers=headers,
            params=params,
            data=payload if not use_json else None,
            json=jsonbody if use_json else None,
            auth=(auth_tuple if auth.auth_type == "basic" else None),
        )

        # check for errors not related to rate limiting:
        if (
            module
            not in [
                "gav",
                "cloud_agent",
                "cloudview",
                "containersecurity",
                "was",
                "pm",
                "cert",
                "tagging",
            ]
            and response.status_code in range(400, 599)
            and response.status_code not in [429, 414]
            and endpoint != "get_kb_qvs"
            and (
                response.status_code != 409
                and "This API cannot be run again for another"
                not in xml_parser(response.text)
                .get("SIMPLE_RETURN")
                .get("RESPONSE")
                .get("TEXT")
            )
        ):
            parsed = xml_parser(response.text) if module not in ["gav"] else None

            # Common path is [SIMPLE_RETURN][RESPONSE][TEXT] for XML
            if parsed:
                if "SIMPLE_RETURN" in parsed:
                    raise QualysAPIError(parsed["SIMPLE_RETURN"]["RESPONSE"]["TEXT"])
                elif "html" in parsed:
                    raise Exception(
                        f"Error: {parsed['html']['body']['h1']}: {parsed['html']['body']['p'][1]['#text']}"
                    )
                else:
                    # yeah... turns out a homegrown xml parsers aren't super easy...
                    raise Exception(
                        f"Error: {parsed['{http://www.w3.org/1999/xhtml}html']['{http://www.w3.org/1999/xhtml}body']['{http://www.w3.org/1999/xhtml}h1']}"
                    )
            else:  # or JSON
                raise QualysAPIError(
                    response.text if response.text else response.reason
                )

        # Check rate limit details from headers.
        if (
            "X-RateLimit-Remaining" in response.headers
            and int(response.headers["X-RateLimit-Remaining"]) < 10
        ) or response.status_code == 429:
            # Rate limit reached:
            # Qualys does not return X-RateLimit headers for PM as of 12-2024. Sigh...
            if module != "pm" and int(response.headers["X-RateLimit-Remaining"]) == 0:
                # Call API again for the X-RateLimit-ToWait-Sec header.
                # Qualys sometimes only includes this header when the rate limit is reached and retried:
                response = request(
                    method=(
                        SCHEMA["method"][0]
                        if not override_method
                        else override_method.upper()
                    ),
                    url=url,
                    headers=headers,
                    params=params,
                    data=payload if not use_json else None,
                    json=jsonbody if use_json else None,
                    auth=(auth_tuple if auth.auth_type == "basic" else None),
                )

                # Isolate the wait time from the header:
                to_wait = response.headers.get("X-RateLimit-ToWait-Sec")
                if to_wait:
                    to_wait = (
                        int(to_wait) + 3
                    )  # Add 3 seconds to the wait time to be safe.
                else:
                    to_wait = 3601  # Default to 1h 1s if no header is present.

                print(
                    f"WARNING: You have reached the rate limit for this endpoint. qualysdk will automatically sleep for {to_wait} seconds and try again at approximately {datetime.now() + timedelta(seconds=to_wait)}."
                )
                sleep(to_wait)
                # Go to next iteration of the loop to try again:
                continue
            # Qualys does not return X-RateLimit headers for PM. Sigh...
            elif module == "pm":
                return response
            else:
                # Almost at rate limit:
                print(
                    f"Warning: This endpoint will accept {response.headers['X-RateLimit-Remaining']} more calls before rate limiting you. qualysdk will automatically sleep once remaining calls hits 0."
                )

        return response
