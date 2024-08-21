"""
activity_log.py - Contains the user-facing functionality for interacting with the Qualys VMDR Activity Log API.
"""

from urllib.parse import parse_qs
from re import compile, DOTALL
from csv import DictReader
from typing import Union

from ..base.call_api import call_api
from ..auth.basic import BasicAuth
from ..base.base_list import BaseList
from ..vmdr.data_classes.activity_log import ActivityLog


def extract_sections(csv_data: str) -> tuple[Union[str, None], Union[str, None]]:
    """
    Split the CSV data into the body and footer sections.

    Args:
        csv_data (str): The raw requests.response.text data.

    Returns:
        tuple[Union[str, None], Union[str, None]]: The body and footer sections, in that order. None if not found.
    """

    body_pattern = compile(
        r"----BEGIN_RESPONSE_BODY_CSV\n(.*?)\n----END_RESPONSE_BODY_CSV", DOTALL
    )
    footer_patern = compile(
        r"----BEGIN_RESPONSE_FOOTER_CSV\n(.*?)\n----END_RESPONSE_FOOTER_CSV", DOTALL
    )

    body_match = body_pattern.search(csv_data)
    body_section = body_match.group(1) if body_match else None

    footer_match = footer_patern.search(csv_data)
    footer_section = footer_match.group(1) if footer_match else None

    return body_section, footer_section


def get_activity_log(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> BaseList[ActivityLog]:
    """
    Get the activity log for the subscription.

    Args:
        auth (BasicAuth): The BasicAuth object containing the user's credentials.
        page_count (Union[int, 'all']): The number of pages to pull. Defaults to 'all'.
        **kwargs: Additional parameters to pass to the API.

    :Kwargs:
        user_action (str): Filter by user action.
        action_details (str): Filter by action details.
        username (str): Filter by username.
        since_datetime (str): Filter by date and time since. Formatted like ```YYYY-MM-DD HH:ii:ss```.
        until_datetime (str): Filter by date and time until. Formatted like ```YYYY-MM-DD HH:ii:ss```.
        user_role (str): Filter by user role.
        truncation_limit (int): The maximum number of characters to return in the details field.

    Returns:
        BaseList[ActivityLog]: The list of activity log entries.
    """

    responses = BaseList()
    pulled = 0
    params = {"action": "list", "output_format": "csv"}

    if kwargs:
        params.update(kwargs)

    while True:
        # make the request:
        response = call_api(
            auth=auth,
            module="vmdr",
            endpoint="get_activity_log",
            params=params,
            headers={"X-Requested-With": "qualysdk SDK"},
        )
        if response.status_code != 200:
            print("No data returned.")
            return responses

        # Rip the data out of the header/footer/warning comments:
        data, pagination_data = extract_sections(response.text)

        if not data:
            print("No data returned.")
            return responses

        data = DictReader(data.splitlines())

        for row in data:
            # Keys with a space in the name need to be renamed to
            # have underscores instead of spaces.
            row = {k.replace(" ", "_"): v for k, v in row.items()}
            responses.append(ActivityLog.from_dict(row))

        # Check for pagination:
        if pagination_data:
            url = pagination_data.split(",")[~0]

            # Parse the params out of the URL:
            url_params = parse_qs(url)

            # Look for the id_max parameter and update the params:
            if "id_max" in url_params:
                params["id_max"] = url_params["id_max"][0].strip().replace('"', "")
                print(
                    f"Pagination detected. Pulling next page with id_max: {params['id_max']}"
                )
            else:
                print("No more pages to pull.")
                break

        pulled += 1

        if page_count != "all" and pulled >= page_count:
            print("Page count reached.")
            break

    return responses
