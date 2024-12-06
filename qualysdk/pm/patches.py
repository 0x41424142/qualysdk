"""
Contains the user-facing functions for interacting with
the /pm/v*/patches* endpoints
"""

from typing import Union, Literal
from threading import Thread, Lock

from .data_classes.Patch import Patch
from .base.page_limit import check_page_size_limit
from ..auth.token import TokenAuth
from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..exceptions.Exceptions import QualysAPIError


def get_patches_backend(
    auth: TokenAuth,
    platform: Literal["windows", "linux"] = "Windows",
    _ResponsesList: BaseList = BaseList(),
    **kwargs,
) -> None:
    """
    Backend function for threads to call get_patches.

    Do not call this function directly.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal["all", "windows", "linux"]): The platform to filter by.
        _ResponsesList (BaseList): The list of responses for threads to make their responses available to. Should not be called directly.
        **kwargs: Any additional valid parameters.

    ## Kwargs:

        - pageSize (int): The number of patches to return per page. Default is 1000.
        - query (str): A patch QQL query. By default for Windows this is "patchStatus:[Missing,Installed] and isSuperseded:false", which returns all the latest patches.
        - havingQuery (str): A PM asset QQL query.
        - attributes (list[str]): A list of attributes to return.
        - searchAfter (str): The searchAfter value. Do not use this parameter directly.
        - page_count (Union[int, 'all']): The number of pages to retrieve. Default is 'all'.

    Returns:
        None
    """

    platform = platform.title()
    LOCK = Lock()

    if kwargs.get("pageSize"):
        check_page_size_limit(kwargs["pageSize"])

    match platform:
        case "Windows":
            query = "patchStatus:[Missing,Installed] and isSuperseded:false"
        case _:
            query = None

    payload = {
        "query": query,
        "havingQuery": kwargs.get("havingQuery"),
        "attributes": kwargs.get("attributes"),
    }

    headers = {
        "searchAfter": kwargs.get("searchAfter"),
    }

    params = {
        "pageSize": kwargs.get("pageSize", 1000),
        "platform": platform,
    }

    # Get id of any None valued keys across all dictionaries:
    none_keys = (
        [key for key in payload if payload[key] is None]
        + [key for key in headers if headers[key] is None]
        + [key for key in params if params[key] is None]
    )
    for key in none_keys:
        if key in payload:
            payload.pop(key)
        if key in headers:
            headers.pop(key)
        if key in params:
            params.pop(key)

    pulled = 0
    page_count = kwargs.get("page_count", "all")
    if not isinstance(page_count, int) and page_count != "all":
        raise ValueError("page_count must be an integer or 'all'.")

    while True:
        response = call_api(
            auth=auth,
            module="pm",
            endpoint="get_patches",
            params=params if params else None,
            jsonbody=payload if payload else None,
            headers=headers if headers else None,
        )

        if response.status_code not in range(200, 299):
            raise QualysAPIError(response.text)
        j = response.json()
        for patch in j:
            patch["platform"] = platform
            _ResponsesList.append(Patch(**patch))

        if response.headers.get("searchAfter"):
            headers["searchAfter"] = response.headers["searchAfter"]

        pulled += 1

        if pulled % 5 == 0:
            with LOCK:
                print(f"{platform} Thread has pulled {pulled} pages so far.")

        if page_count != "all" and pulled >= page_count:
            with LOCK:
                print(
                    f"{platform} Thread has hit user-defined page limit of {page_count}."
                )
            break

        if len(j) < params["pageSize"]:
            with LOCK:
                print(f"{platform} Thread has reached the end of the list.")
            break

    return


def get_patches(
    auth: TokenAuth,
    platform: Literal["all", "windows", "linux"] = "all",
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList:
    """
    Get a list of patches according to the specified kwarg filters.

    By default, returns all patches across both Windows and Linux platforms.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['all', 'windows', 'linux']): The platform to filter by. Default is 'windows'.
        page_count (Union[int, 'all']): The number of pages to retrieve. Default is 'all'.
        **kwargs: Any additional valid parameters.

    ## Kwargs:

        - pageSize (int): The number of patches to return per page. Default is 1000.
        - query (str): A patch QQL query.
        - havingQuery (str): A PM asset QQL query.
        - attributes (list[str]): A list of attributes to return.
    """

    responses = BaseList()

    if kwargs.get("pageSize"):
        check_page_size_limit(kwargs["pageSize"])

    if page_count != "all" and (not isinstance(page_count, int) or page_count < 1):
        raise ValueError("page_count must be an integer or 'all'.")

    kwargs["_ResponsesList"] = responses
    kwargs["page_count"] = page_count

    match platform.title():
        case "All":
            threads = [
                Thread(
                    target=get_patches_backend,
                    args=(auth, "Windows"),
                    kwargs=kwargs,
                    name="GetPatches-WindowsThread",
                ),
                Thread(
                    target=get_patches_backend,
                    args=(auth, "Linux"),
                    kwargs=kwargs,
                    name="GetPatches-LinuxThread",
                ),
            ]
        case "Windows":
            threads = [
                Thread(
                    target=get_patches_backend,
                    args=(auth, "Windows"),
                    kwargs=kwargs,
                    name="GetPatches-WindowsThread",
                )
            ]
        case "Linux":
            threads = [
                Thread(
                    target=get_patches_backend,
                    args=(auth, "Linux"),
                    kwargs=kwargs,
                    name="GetPatches-LinuxThread",
                )
            ]
        case _:
            raise ValueError("Invalid platform. Must be 'all', 'windows', or 'linux'.")

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    return responses
