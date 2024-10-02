"""
Code to generate XML service requests to Qualys WAS API
"""

from requests import Response

from ...base.xml_parser import xml_parser
from ...exceptions.Exceptions import QualysAPIError


def build_service_request(**kwargs):
    """
    Build the XML request. Users pass in the filters as kwargs.
    there is the filter itself as well as a filter_operator kwarg.
    If the filter_operator is not provided, default to "EQUALS".
    Do not create a Criteria tag for any _operator kwargs.
    """

    xml = "<ServiceRequest>{PREFERENCES}<filters>{REPLACE}</filters></ServiceRequest>"
    user_xml = ""

    # Check for any tags that need to be under preferences instead of filters:
    PREFERENCE_TAGS = ["verbose"]

    for tag in PREFERENCE_TAGS:
        if kwargs.get(tag):
            # If boolean, convert to string:
            if isinstance(kwargs.get(tag), bool):
                kwargs[tag] = str(kwargs.get(tag)).lower()
            # If this is the first preference found,
            # build the structure. If not, just add the line of
            # XML to the existing structure.
            if "{PREFERENCES}" in xml:
                xml = xml.replace(
                    "{PREFERENCES}",
                    f"<preferences><{tag}>{kwargs.pop(tag)}</{tag}></preferences>",
                )
            else:
                # Add the key as a tag within the preferences tag.
                xml = xml.replace(
                    "</preferences>", f"<{tag}>{kwargs.pop(tag)}</{tag}</preferences>"
                )

    # If no preferences were found, remove the placeholder:
    xml = xml.replace("{PREFERENCES}", "")

    for kwarg, value in kwargs.items():
        if kwarg.endswith("operator"):
            continue
        # If boolean, convert to string:
        if isinstance(value, bool):
            value = str(value).lower()

        user_xml += f'<Criteria field="{kwarg}" operator="{kwargs.get(kwarg + ".operator", "EQUALS")}">{value}</Criteria>'

    xml = xml.replace("{REPLACE}", user_xml)
    payload = {"_xml_data": xml}

    # if no filters were provided, remove the filters tag:
    if not user_xml:
        payload = {"_xml_data": xml.replace("<filters></filters>", "")}

    return payload


def validate_response(response: Response) -> dict:
    """
    Parse the XML response from the Qualys API
    and check for errors.

    Args:
        response (Response): The response object from the API call.

    Returns:
        dict: The parsed XML response.
    """
    parsed = xml_parser(response.text)

    if response.status_code != 200:
        errorMessage = (
            parsed.get("ServiceResponse")
            .get("responseErrorDetails")
            .get("errorMessage")
        )
        responseCode = parsed.get("ServiceResponse").get("responseCode")
        raise QualysAPIError(
            f"Error retrieving web applications. Status code: {response.status_code}. Endpoint reporting: {responseCode}. Error message: {errorMessage}"
        )

    serviceResponse = parsed.get("ServiceResponse")
    if not serviceResponse:
        raise QualysAPIError("No ServiceResponse tag returned in the API response")

    if serviceResponse.get("responseCode") != "SUCCESS":
        errorMessage = (
            parsed.get("ServiceResponse")
            .get("responseErrorDetails")
            .get("errorMessage")
        )
        responseCode = parsed.get("ServiceResponse").get("responseCode")
        raise QualysAPIError(
            f"Error retrieving web applications. Status code: {response.status_code}. Endpoint reporting: {responseCode}. Error message: {errorMessage}"
        )

    return parsed
