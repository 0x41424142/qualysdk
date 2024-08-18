"""
call_api.py - contains the call_api function for the qualysdk package.

This function handles all API calls to the Qualys API. It takes in a URL, headers, and a payload, and returns the response from the API.
Qualys uses many tricks in their API, such as using both url params and post data.
"""

from requests import request, Response
from typing import Literal, Union
from datetime import datetime

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
        case _:
            raise ValueError(f"Invalid url_type {SCHEMA['url_type']}.")

    # if token auth, check if token is not 4+ hours old:
    if isinstance(auth, TokenAuth):
        # check that the time delta between now and the token generation time is less than 4 hours:
        if (datetime.now() - auth.generated_on).seconds > 14400:
            print("Token is 4+ hours old. Refreshing token.")
            auth.get_token()

    # check params:
    if params:
        for key in params.keys():
            if key not in SCHEMA["valid_params"]:
                raise ValueError(
                    f"Invalid parameter {key} for {module}-{endpoint}. Valid parameters are: {SCHEMA['valid_params']}."
                )

    # check post data:
    if payload:
        for key in payload.keys():
            if key not in SCHEMA["valid_POST_data"]:
                raise ValueError(f"Invalid payload key {key} for {module}-{endpoint}.")

    # check if data should be POSTed as requests.post(json=):
    if SCHEMA["use_requests_json_data"]:
        use_json = True
    else:
        use_json = False

    # set up JWT auth header if needed:
    if auth.auth_type == "token":
        headers = auth.as_header()
    # or set up the tuple for basic auth:
    elif auth.auth_type == "basic":
        auth_tuple = (auth.username, auth.password)

    # Make certain payloads/params requests-friendly:
    if payload:
        payload = convert_bools_and_nones(payload)
    if params:
        params = convert_bools_and_nones(params)

    # and finally, make the request:
    response = request(
        method=SCHEMA["method"][0] if not override_method else override_method.upper(),
        url=url,
        headers=headers,
        params=params,
        data=payload if not use_json else None,
        json=jsonbody if use_json else None,
        auth=(auth_tuple if auth.auth_type == "basic" else None),
    )

    # check for errors:
    if response.status_code in range(400, 599):
        # print(f"Error: {response.text}")
        # response.raise_for_status()
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
            raise QualysAPIError(response.text)

    return response
