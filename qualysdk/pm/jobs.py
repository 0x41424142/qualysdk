"""
Contains code to interact with Patch
Management jobs in Qualys.
"""

from __future__ import annotations
from typing import Union, Literal, overload, Sequence
from json import JSONDecodeError
from threading import Thread, Lock, current_thread
from queue import Queue

from .data_classes import *
from .base.page_limit import check_page_size_limit
from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *


def manage_jobs(
    auth: TokenAuth,
    method: Literal["GET", "POST", "PATCH", "DELETE"] = "GET",
    _use_singular_in_url: bool = False,
    **kwargs,
) -> dict:
    """
    Backend function to interact with PM jobs.
    This is not meant to be called directly.

    Args:
        auth (TokenAuth): The authentication object.
        method (Literal['GET','POST','PATCH','DELETE']): The HTTP method to use. Default is 'GET'.
        _use_singular_in_url (bool): Used for jobs and reports. URLs can be */job/* or */jobs/*.

    ## Kwargs:

        - kwargs from the calling function.

    Returns:
        API Response
    """

    if kwargs.get("platform"):
        kwargs["platform"] = kwargs["platform"].title()

    if kwargs.get("platform") not in ["Windows", "Linux", None]:
        raise ValueError(
            f"Invalid platform {kwargs.get('platform')}. Valid platforms are 'windows' or 'linux'"
        )

    if method not in ["GET", "POST", "PATCH", "DELETE"]:
        raise ValueError(
            f"Invalid method {method}. Valid methods are 'GET', 'POST', 'PATCH', 'DELETE'"
        )

    if kwargs.get("pageSize"):
        check_page_size_limit(kwargs["pageSize"])

    call_data = None

    call_data = call_api(
        auth=auth,
        module="pm",
        endpoint="deploymentjob" if _use_singular_in_url else "deploymentjobs",
        params=kwargs if method in ["GET", "DELETE"] else {},
        payload=kwargs if method in ["POST", "PATCH"] else {},
        override_method=method,
    )

    if call_data.status_code not in range(200, 299):
        err_data = call_data.json()

        # Check for 2501 error code - indicating we have hit the
        # limit of resources we can pull. (Fix this, Qualys!!!)
        if err_data["_error"].get("errorCode") == "2501":
            raise QualysAPIError(call_data.json())

    return call_data


def _list_jobs_backend(
    auth: TokenAuth,
    platform: Literal["Windows", "Linux"],
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList[PMJob]:
    """
    Backend function for listing jobs.

    Not meant to be called directly.

    **_result_bl is a shared resource for threads.
    """
    if page_count != "all":
        if not isinstance(page_count, int) or page_count < 1:
            raise ValueError(
                "page_count must be an integer greater than or equal to 1, or 'all'"
            )

    kwargs["platform"] = platform
    pages_pulled = 0
    # If called from a thread, we need to use a shared resource
    responses = (
        BaseList()
        if "_response_bl" not in kwargs.keys()
        else kwargs.pop("_response_bl")
    )

    # Set up URL format
    kwargs["placeholder"] = "summary"
    kwargs["pageNumber"] = pages_pulled
    lock = Lock()

    while True:
        response = manage_jobs(auth=auth, **kwargs)

        if not response:
            break

        try:
            parsed = response.json()
        except JSONDecodeError:
            raise QualysAPIError(response.status_code, response.text)

        if len(parsed) < 1:
            break

        # Protect BaseList if threads are used:
        with lock:
            responses.extend([PMJob.from_dict(**job) for job in parsed])

        if page_count != "all":
            pages_pulled += 1
            kwargs["pageNumber"] = pages_pulled
            if pages_pulled >= page_count:
                print(
                    f"{current_thread().name} - Hit user-defined limit of {page_count} pages for platform={platform}."
                )
                break
        else:
            pages_pulled += 1
            kwargs["pageNumber"] = pages_pulled

        if len(parsed) == 0:
            break

    return responses


def list_jobs(
    auth: TokenAuth,
    platform: Literal["all", "windows", "linux"] = "all",
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList[PMJob]:
    """
    Return a list of Patch Management jobs
    in the user's scope.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['all', 'windows', 'linux']): The platform to get jobs for. Default is 'all'.
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

    match platform.title():
        case "All":
            # Shared resource for threads to return results
            kwargs["_response_bl"] = BaseList()
            threads = [
                Thread(
                    target=_list_jobs_backend,
                    args=(auth, "Windows", page_count),
                    kwargs=kwargs,
                    name="WindowsJobThread",
                ),
                Thread(
                    target=_list_jobs_backend,
                    args=(auth, "Linux", page_count),
                    kwargs=kwargs,
                    name="LinuxJobThread",
                ),
            ]

            print(f"Spawned threads for both Windows and Linux jobs...")

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            results = kwargs["_response_bl"]

        case "Windows":
            results = _list_jobs_backend(
                auth=auth, platform="Windows", page_count=page_count, **kwargs
            )
        case "Linux":
            results = _list_jobs_backend(
                auth=auth, platform="Linux", page_count=page_count, **kwargs
            )
        case _:
            raise ValueError(
                f"Invalid platform {platform}. Valid platforms are 'all', 'windows' or 'linux'"
            )

    return results


# Overload 1 for str jobId
@overload
def get_job_results(auth: TokenAuth, jobId: str, **kwargs) -> JobResultSummary:
    ...


# Overload 2 for list/BaseList of PMJob
@overload
def get_job_results(
    auth: TokenAuth, jobId: Union[list[PMJob], BaseList[PMJob]], **kwargs
) -> BaseList[JobResultSummary]:
    ...


def get_job_results(auth: TokenAuth, jobId: Union[str, Sequence[PMJob]], **kwargs):
    """
    Returns the results of a Patch Management job, or
    a specific instance of a job.

    Args:
        auth (TokenAuth): The authentication object.
        jobId (Union[str, BaseList[PMJob]]): The ID of the job to get results for.
        If a list of PMJob objects is passed, the function will thread the requests.

    ## Kwargs:

        - jobInstanceId (str): The ID of a specific instance of a job.
        - pageSize (int): The number of results to return per page. Default is 10.
        - sort (str): The field to sort results by.

    Returns:
        Union[JobResultSummary, BaseList[JobResultSummary]]: The response from the
        API as a JobResultSummary object or a BaseList of JobResultSummary objects.
    """
    lock = Lock()
    if isinstance(jobId, str):
        kwargs["placeholder"] = f"{jobId}/deploymentjobresult/summary"
        kwargs_no_bl = kwargs.copy()
        kwargs_no_bl.pop("_response_bl", None)
        result = manage_jobs(
            auth=auth, method="POST", _use_singular_in_url=True, **kwargs_no_bl
        )
        if not kwargs.get("_response_bl") and kwargs.get("_response_bl") != BaseList():
            return JobResultSummary.from_dict(**result.json())
        else:
            with lock:
                kwargs["_response_bl"].extend(
                    [JobResultSummary.from_dict(**result.json())]
                )
            return

    elif isinstance(jobId, (list, BaseList)) and all(
        isinstance(job, (PMJob, str)) for job in jobId
    ):
        # Shared resource for threads to return results
        kwargs["_response_bl"] = BaseList()
        threads = []
        print(f"Spawning threads for {len(jobId)} jobs...")
        q = Queue()
        for job in jobId:
            if isinstance(job, PMJob):
                q.put(job.id)
            else:
                q.put(job)

        # Each thread will pop a job from the queue and process it.
        # at no point should the threads list have a len > 5.
        while not q.empty():
            if len(threads) < 5:
                job = q.get()
                thread = Thread(
                    target=get_job_results,
                    args=(auth, job),
                    kwargs=kwargs,
                    name=f"JobResultThread-{job}",
                )
                thread.start()
                threads.append(thread)
            else:
                for thread in threads:
                    thread.join()
                threads = []

            with lock:
                if q.qsize() % 25 == 0:
                    print(f"Requests left in queue: {q.qsize()}")

        for thread in threads:
            thread.join()

        return kwargs["_response_bl"]

    else:
        raise ValueError(
            "jobId must be a string, or a list/BaseList of PMJob objects or strings."
        )


def get_job_runs(
    auth: TokenAuth, jobId: Union[str, BaseList[PMJob], list[PMJob]]
) -> BaseList[PMRun]:
    """
    Get a list of job runs for a specific job.

    Args:
        auth (TokenAuth): The authentication object.
        jobId (str) The ID of the job to get runs for.

    Returns:
        BaseList[PMRun]: The response from the API as a BaseList of PMRun objects.
    """

    params = {"placeholder": f"{jobId}/runs"}

    result = manage_jobs(auth=auth, _use_singular_in_url=True, **params)

    result = result.json()

    for run in result:
        run["jobId"] = jobId

    return BaseList([PMRun.from_dict(**run) for run in result])
