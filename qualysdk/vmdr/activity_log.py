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
from qualysdk.base.logging import ProgressTracker, get_logger

logger = get_logger(__name__)


def extract_sections(csv_data: str) -> tuple[Union[str, None], Union[str, None]]:
    """
    Split the CSV data into the body and footer sections.

    Args:
        csv_data (str): The raw requests.response.text data.

    Returns:
        tuple[Union[str, None], Union[str, None]]: The body and footer sections, in that order. None if not found.
    """

    body_pattern = compile(r"----BEGIN_RESPONSE_BODY_CSV\n(.*?)\n----END_RESPONSE_BODY_CSV", DOTALL)
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
    completion_reason = "all pages complete"
    progress = ProgressTracker(
        logger=logger,
        operation="get_activity_log",
        item_label="activity log entries collected",
        page_interval=10,
        time_interval=20.0,
        total_pages=page_count if isinstance(page_count, int) else None,
        remaining_label="page(s) remaining",
    )

    if kwargs:
        params.update(kwargs)

    logger.info("Starting get_activity_log.")

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
            completion_reason = "no data returned"
            break

        # Rip the data out of the header/footer/warning comments:
        data, pagination_data = extract_sections(response.text)

        if not data:
            completion_reason = "no data returned"
            break

        page_rows = [
            ActivityLog.from_dict({k.replace(" ", "_"): v for k, v in row.items()})
            for row in DictReader(data.splitlines())
        ]
        responses.extend(page_rows)

        pulled += 1
        progress.record(items=len(page_rows), pages=1)

        # Check for pagination:
        if pagination_data:
            url = pagination_data.split(",")[~0]

            # Parse the params out of the URL:
            url_params = parse_qs(url)

            # Look for the id_max parameter and update the params:
            if "id_max" in url_params:
                params["id_max"] = url_params["id_max"][0].strip().replace('"', "")
                logger.debug(
                    f"Pagination detected. Pulling next page with id_max: {params['id_max']}"
                )
            else:
                completion_reason = "no more records"
                logger.debug("No more pages to pull.")
                break
        else:
            completion_reason = "no more records"
            break

        if page_count != "all" and pulled >= page_count:
            completion_reason = "page count reached"
            break

    progress.complete(extra=completion_reason)
    return responses
