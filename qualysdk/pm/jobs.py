"""
Contains code to interact with Patch
Management jobs in Qualys.
"""

from typing import Union, Literal
from json import loads, JSONDecodeError

from .data_classes.Job import PMJob
from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *


def manage_jobs(
    auth: TokenAuth,
    platform: Literal["windows", "linux"],
    method: Literal["GET", "POST", "PATCH", "DELETE"] = "GET",
    **kwargs,
):
    """
    Backend function to interact with PM jobs.
    This is not meant to be called directly.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['windows', 'linux']): The platform to manage jobs for.
        method (Literal['GET','POST','PATCH','DELETE']): The HTTP method to use. Default is 'GET'.

    ## Kwargs:

        - kwargs from the calling function.

    Returns:
        API Response
    """
    if platform not in ["windows", "linux"]:
        raise ValueError(
            f"Invalid platform {platform}. Valid platforms are 'windows' or 'linux'"
        )

    if method not in ["GET", "POST", "PATCH", "DELETE"]:
        raise ValueError(
            f"Invalid method {method}. Valid methods are 'GET', 'POST', 'PATCH', 'DELETE'"
        )

    if (
        kwargs.get("pageSize")
        and isinstance(kwargs.get("pageSize"), int)
        and kwargs.get("pageSize") > 10_000
    ):
        raise ValueError("pageSize cannot be greater than 10,000")

    call_data = None

    call_data = call_api(
        auth=auth,
        module="pm",
        endpoint="deploymentjobs",
        params=kwargs if method in ["GET", "DELETE"] else {},
        jsonbody=kwargs if method in ["POST", "PATCH"] else {},
        override_method=method,
    )

    if call_data.status_code not in range(200, 299):
        err_data = loads(call_data.text)

        # Check for 2501 error code - indicating we have hit the
        # limit of resources we can pull. (Fix this, Qualys!!!)
        if err_data["_error"].get("errorCode") == "2501":
            raise QualysAPIError(loads(call_data.text))

    return call_data


def list_jobs(
    auth: TokenAuth,
    platform: Literal["windows", "linux"],
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList:
    """
    Return a list of Patch Management jobs
    in the user's scope.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['windows', 'linux']): The platform to get jobs for.
        page_count (int): The number of pages to return. Default is 'all'.

    ## Kwargs:

        - filter (str): a Windows/Linux Job QQL filter.
        - attributes (str): The job attributes to return as a comma-separated string.
        - coauthorJob (bool): Only return jobs that the user is a co-author of (Default is False).
        - ownedJob (bool): Only return jobs that the user solely owns (Default is False).
        - pageSize (int): The number of jobs to return per page. Default is 10.

    Returns:
        BaseList: The response from the API as a BaseList of Job objects.
    """

    if page_count != "all":
        if not isinstance(page_count, int) or page_count < 1:
            raise ValueError(
                "page_count must be an integer greater than or equal to 1, or 'all'"
            )

    pages_pulled = 0
    responses = BaseList()

    # Set up URL format
    kwargs["placeholder"] = "summary"
    kwargs["pageNumber"] = pages_pulled

    while True:
        response = manage_jobs(auth=auth, platform=platform, **kwargs)

        if not response:
            break

        try:
            parsed = loads(response.text)
        except JSONDecodeError:
            raise QualysAPIError(response.status_code, response.text)

        if len(parsed) < 1:
            break

        responses.extend([PMJob.from_dict(**job) for job in parsed])

        if page_count != "all":
            pages_pulled += 1
            if pages_pulled >= page_count:
                print(f"Hit user-defined limit of {page_count} pages.")
                break
        else:
            pages_pulled += 1
            kwargs["pageNumber"] = pages_pulled

        if len(parsed) == 0:
            break

    return responses
