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
    _jsonbody: dict = None,
    **kwargs,
) -> dict:
    """
    Backend function to interact with PM jobs.
    This is not meant to be called directly.

    Args:
        auth (TokenAuth): The authentication object.
        method (Literal['GET','POST','PATCH','DELETE']): The HTTP method to use. Default is 'GET'.
        _use_singular_in_url (bool): Used for jobs and reports. URLs can be */job/* or */jobs/*.
        - _jsonbody (dict): The JSON body to send with the request.

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
        jsonbody=_jsonbody,
        override_method=method,
    )

    if call_data.status_code not in range(200, 299):
        try:
            err_data = call_data.json()
            # Check for 2501 error code - indicating we have hit the
            # limit of resources we can pull. (Fix this, Qualys!!!)
            if err_data["_error"].get("errorCode") == "2501":
                raise QualysAPIError(call_data.json())
        except JSONDecodeError:
            err_data = call_data.text
            raise QualysAPIError(f"{call_data.status_code} - {err_data}")

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
    kwargs["placeholder"] = "/summary"
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
            responses.extend([PMJob.from_dict(job) for job in parsed])

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

            print("Spawned threads for both Windows and Linux jobs...")

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


def get_job_results(
    auth: TokenAuth, jobId: Union[str, Sequence[PMJob]], **kwargs
) -> Union[JobResultSummary, BaseList[JobResultSummary]]:
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
        kwargs["placeholder"] = f"/{jobId}/deploymentjobresult/summary"
        kwargs_no_bl = kwargs.copy()
        kwargs_no_bl.pop("_response_bl", None)
        result = manage_jobs(
            auth=auth, method="POST", _use_singular_in_url=True, **kwargs_no_bl
        )
        if not kwargs.get("_response_bl") and kwargs.get("_response_bl") != BaseList():
            return JobResultSummary.from_dict(result.json())
        else:
            with lock:
                kwargs["_response_bl"].extend(
                    [JobResultSummary.from_dict(result.json())]
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

    params = {"placeholder": f"/{jobId}/runs"}

    result = manage_jobs(auth=auth, _use_singular_in_url=True, **params)

    result = result.json()

    for run in result:
        run["jobId"] = jobId

    return BaseList([PMRun.from_dict(run) for run in result])


def remove_none_values(d):
    if not isinstance(d, dict):
        return d
    return {k: remove_none_values(v) for k, v in d.items() if v is not None}


def create_job(
    auth: TokenAuth,
    platform: Literal["Windows", "Linux"],
    name: str,
    jobType: Literal["Install", "Rollback"],
    scheduleType: Literal["On-demand", "Once", "Daily", "Weekly", "Monthly"],
    **kwargs,
) -> str:
    """
    Create a job in Patch Management.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['Windows', 'Linux']): The platform for the job.
        name (str): The name of the job.
        jobType (Literal['Install', 'Rollback']): The type of job.
        scheduleType (Literal['On-demand', 'Once', 'Daily', 'Weekly', 'Monthly']): The schedule type for the job.

    ## Kwargs:

        - approvedPatches (list[str]): A list of patch GUIDs that are explicitly approved for the job.
        - assetIds (list[str]): A list of asset GUIDs to target with the job.
        - assetTagIds (list[str]): A list of asset tag GUIDs to target with the job.
        - filterType (Literal["all", "any"] = 'any'): The filter type for the job. Default is 'any'.
        - exclusionAssetIds (list[str]): A list of asset GUIDs to exclude from the job.
        - exclusionTagIds (list[str]): A list of asset tag GUIDs to exclude from the job.
        - coAuthorUserIds (list[str]): A list of user GUIDs to co-author the job.
        - exclusionFilterType (Literal["all", "any"] = 'any'): The exclusion filter type for the job. Default is 'any'.
        - description (str): The description for the job.
        - startDateTime (str): The start date and time for the job. Not required for on-demand jobs, required for all other schedules.
        - recurring (bool): Whether the job is recurring. Default is False.
        - dayOfMonth (int, 0 <= x < 32): The day of the month for the job.
        - matchAllTagIds (list[str]): A list of asset tag GUIDs to match all of.
        - recurringLastDayOfMonth (bool): Whether the job is recurring on the last day of the month. Default is False.
        - monthlyRecurringType (Literal["0", "1", 0, 1]): If 1, job will run on Patch Tuesday.
        - patchTuesdayPlusXDays (int, -27 <= x <= 27): The number of days before/at/after Patch Tuesday to run the job.
        - recurringDayOfMonth (int, 1 <= x <= 5): Run the job on a specific weekday of the month.
        - recurringWeekDayOfMonth (int, 0 <= x <= 6): The day of the week to run the job.
        - recurringWeekDays (str, like "0,0,0,0,0,0,0"): The days of the week to run the job. Replace a 0 with a 1 to enable the day. str[0] is Sunday.
        - dynamicQQLType (Literal[0,1,2]): The dynamic QQL type for the job. 0 = Do not use QQL, 1 = Use patch QQL, 2 = Use vulnerability QQL.
        - isDynamicPatchesQQL (bool): Whether the job uses dynamic patches QQL. Default is False.
        - dynamicPatchesQQL (str): The dynamic patches QQL for the job.
        - continueOnPatchFailure (bool): Whether the job continues on patch failure. Default is True. *APPLIES TO LINUX ONLY!*.
        - preDeployment (str): Message to show the user before deployment.
        - duringDeployment (str): Message to show the user during deployment.
        - postDeployment (str): Message to show the user after deployment.
        - onComplete (str): Message to show the user after the job is complete.
        - rebootCountdown (str): Message to show the user before reboot.
        - rebootOption (str): Message to show the user after reboot.
        - suppressReboots (bool): Whether a user can suppress reboots. Default is False.
        - minimizeWindow (bool): Whether a user can minimize the job popup. Default is False.
        - status (Literal["Disabled", "Enabled"] = "Disabled"): The status of the job. Default is 'Disabled'.
        - timeout (int, 1 <= x <= 168 for hours, 1 <= x <= 10080 for minutes): The timeout for the job in either hours or minutes, which is specified by timeoutUnit.
        - timeoutUnit (Literal["Hours", "Minutes"]): The unit of time for the timeout.
        - timezoneType (Literal["AGENT_TZ", "SPECIFIC_TZ"]): The timezone type for the job.
        - timezone (str): The timezone for the job. See (here)[https://docs.qualys.com/en/pm/api/deployment_job_resource/time_zones.htm] for a list of valid timezones. For example, "America/New_York".
        - opportunisticDownloads (bool): Whether opportunistic downloads are enabled. Default is False.
        - linkedJobId (str): The GUID of a job to link to this job.
        - notificationType (bool): False = No notification, True = Email notification.
        - notificationConfigRecipientEmail (str): The email address to send notifications to.
        - notificationConfigCompletedPercentage (int, 1 <= x <= 100): The percentage of job completion to send notifications at.
        - notificationEvents (bool): False = No notification, True = Email notification when onJobStart or onJobComplete events occur.
        - downloadRandomizeTime (str): Provide a time in hours or minutes. Max is 2 hours or 120 minutes and must be less than timeout/timeoutUnit.
        - downloadRandomizeTimeUnit (Literal["HOURS", "MINUTES"]): The unit of time for downloadRandomizeTime.
        - additionalDynamicQQLType (Literal[1, 2]): 1 = Use patch QQL, 2 = Use vulnerability QQL.
        - additionalDynamicPatchesQQL (str): The additional dynamic patches QQL for the job.

    Returns:
        str: job ID for the created job
    """

    platform, jobType, scheduleType, status = (
        platform.title(),
        jobType.title(),
        scheduleType.capitalize(),
        kwargs.get("status", "Disabled").title(),
    )

    all_uppercase = ["timezoneType", "downloadRandomizeTimeUnit", "timeoutUnit"]
    for key in all_uppercase:
        if key in kwargs:
            kwargs[key] = kwargs[key].upper()

    base_payload = {
        "approvedPatches": kwargs.get("approvedPatches"),
        "assetIds": kwargs.get("assetIds"),
        "assetTagIds": kwargs.get("assetTagIds"),
        "coAuthorUserIds": kwargs.get("coAuthorUserIds"),
        "continueOnPatchFailure": kwargs.get(
            "continueOnPatchFailure", True if platform.lower() == "linux" else None
        ),
        "dayOfMonth": kwargs.get("dayOfMonth"),
        "description": kwargs.get("description"),
        "duringDeployment": {
            "description": kwargs.get("duringDeployment"),
            "userMessage": kwargs.get("duringDeployment"),
        },
        "dynamicPatchesQQL": kwargs.get("dynamicPatchesQQL"),
        "dynamicQQLType": kwargs.get("dynamicQQLType"),
        "additionalDynamicPatchesQQL": kwargs.get("additionalDynamicPatchesQQL"),
        "additionalDynamicQQLType": (
            str(kwargs.get("additionalDynamicQQLType"))
            if kwargs.get("additionalDynamicQQLType")
            else None
        ),
        "exclusionAssetIds": kwargs.get("exclusionAssetIds"),
        "exclusionFilterType": kwargs.get("exclusionFilterType"),
        "exclusionTagIds": kwargs.get("exclusionTagIds"),
        "filterType": kwargs.get("filterType"),
        "isDynamicPatchesQQL": kwargs.get("isDynamicPatchesQQL"),
        "matchAllTagIds": kwargs.get("matchAllTagIds"),
        "minimizeWindow": kwargs.get("minimizeWindow"),
        "monthlyRecurringType": (
            str(kwargs.get("monthlyRecurringType"))
            if kwargs.get("monthlyRecurringType")
            else None
        ),
        "name": name,
        "notification": {
            "notificationConfigs": {
                "recipientEmails": kwargs.get("notificationConfigRecipientEmail"),
                "completedPercentage": kwargs.get(
                    "notificationConfigCompletedPercentage"
                ),
            },
            "notificationTypes": {"email": kwargs.get("notificationType")},
            "notificationEvents": {
                "onJobStart": kwargs.get("notificationEvents"),
                "onJobComplete": kwargs.get("notificationEvents"),
            },
        },
        "opportunisticDownloads": kwargs.get("opportunisticDownloads"),
        "patchTuesdayPlusXDays": kwargs.get("patchTuesdayPlusXDays"),
        "platform": platform,
        "postDeployment": {
            "description": kwargs.get("postDeployment"),
            "userMessage": kwargs.get("postDeployment"),
        },
        "rebootCountdown": {
            "description": kwargs.get("rebootCountdown"),
            "userMessage": kwargs.get("rebootCountdown"),
        },
        "rebootOption": {
            "deferment": (
                {"count": 3, "interval": 30, "intervalUnit": "MINUTES"}
                if kwargs.get("suppressReboots")
                else None
            ),
            "description": kwargs.get("rebootOption"),
            "userMessage": kwargs.get("rebootOption"),
        },
        "suppressReboots": kwargs.get("suppressReboots"),
        "preDeployment": {
            "description": kwargs.get("preDeployment"),
            "userMessage": kwargs.get("preDeployment"),
        },
        "recurring": kwargs.get("recurring"),
        "recurringDayOfMonth": kwargs.get("recurringDayOfMonth"),
        "recurringLastDayOfMonth": kwargs.get("recurringLastDayOfMonth"),
        "recurringWeekDayOfMonth": kwargs.get("recurringWeekDayOfMonth"),
        "recurringWeekDays": kwargs.get("recurringWeekDays"),
        "scheduleType": scheduleType,
        "startDateTime": kwargs.get("startDateTime"),
        "status": status,
        "timeout": kwargs.get("timeout", -1),
        "timeoutUnit": kwargs.get("timeoutUnit"),
        "downloadRandomizeTime": kwargs.get("downloadRandomizeTime"),
        "downloadRandomizeTimeUnit": kwargs.get("downloadRandomizeTimeUnit"),
        "timezone": kwargs.get("timezone"),
        "timezoneType": kwargs.get("timezoneType"),
        "type": jobType,
        "linkedJobId": kwargs.get("linkedJobId"),
        "linkedJobReferenceCount": kwargs.get("linkedJobReferenceCount"),
    }

    # Get rid of any None values
    payload = remove_none_values(base_payload)
    # Pesky stragglers:
    cleanup = [
        "duringDeployment",
        "notification",
        "postDeployment",
        "rebootCountdown",
        "rebootOption",
        "preDeployment",
    ]
    for field in cleanup:
        if field == "notification":
            # check notificationConfigs, notificationTypes, and notificationEvents:
            for subfield in [
                "notificationConfigs",
                "notificationTypes",
                "notificationEvents",
            ]:
                if not payload[field].get(subfield):
                    payload[field].pop(subfield, None)
            # If notification is empty, remove it:
            if not payload.get(field):
                payload.pop(field, None)
        else:
            if not payload.get(field):
                payload.pop(field, None)

    _jsonbody = payload.copy()
    # URL construction:
    payload = {"placeholder": ""}

    result = manage_jobs(
        auth=auth,
        method="POST",
        _use_singular_in_url=True,
        _jsonbody=_jsonbody,
        **payload,
    )

    if result.status_code not in range(200, 299):
        raise QualysAPIError(result.json())

    j = result.json()
    return j["id"]


@overload
def delete_job(auth: TokenAuth, jobId: str) -> list[dict[str, str]]:
    ...


@overload
def delete_job(
    auth: TokenAuth, jobId: Union[list[str], BaseList[str]]
) -> list[dict[str, str]]:
    ...


def delete_job(
    auth: TokenAuth, jobId: Union[str, Sequence[str]]
) -> list[dict[str, str]]:
    """
    Deletes a job or jobs in Patch Management.

    Args:
        auth (TokenAuth): The authentication object.
        jobId (Union[str, list[str]]): The ID of the job to delete, or a list of job IDs.

    Returns:
        list[dict[str, str]]: The response from the API structured as: [{"id": "jobId", "name": "jobName", "status": "statusMessage"}]
    """

    jsonbody = {"ids": []}

    # URL construction:
    payload = {"placeholder": ""}

    if isinstance(jobId, str):
        jsonbody["ids"].append(jobId)
        result = manage_jobs(auth=auth, method="DELETE", _jsonbody=jsonbody, **payload)
        return result.json()

    elif isinstance(jobId, (list, BaseList)) and all(
        isinstance(job, str) for job in jobId
    ):
        jsonbody.update({"ids": jobId})
        return manage_jobs(
            auth=auth, method="DELETE", _jsonbody=jsonbody, **payload
        ).json()

    else:
        raise ValueError("jobId must be a string or a list/BaseList of strings.")


@overload
def change_job_status(
    auth: TokenAuth, action: Literal["Enabled", "Disabled"], jobId: str
) -> dict:
    ...


@overload
def change_job_status(
    auth: TokenAuth,
    action: Literal["Enabled", "Disabled"],
    jobId: Union[list[str], BaseList[str]],
) -> dict:
    ...


def change_job_status(
    auth: TokenAuth,
    action: Literal["Enabled", "Disabled"],
    jobId: Union[str, list[str], BaseList[str]],
) -> dict:
    """
    Enable or disable a job(s) in Patch Management.

    Args:
        auth (TokenAuth): The authentication object.
        action (Literal['Enabled', 'Disabled']): The status to set the job(s) to.
        jobId (Union[str, list[str]]): The ID of the job to enable/disable, or a list of job IDs.

    Returns:
        dict: The response from the API.
    """

    jsonbody = {"ids": []}

    # URL construction:
    payload = {"placeholder": f"/update/status/{action.title()}"}

    if isinstance(jobId, str):
        jsonbody["ids"].append(jobId)
        result = manage_jobs(auth=auth, method="POST", _jsonbody=jsonbody, **payload)

    elif isinstance(jobId, (list, BaseList)) and all(
        isinstance(job, str) for job in jobId
    ):
        jsonbody.update({"ids": jobId})
        result = manage_jobs(auth=auth, method="POST", _jsonbody=jsonbody, **payload)

    else:
        raise ValueError("jobId must be a string or a list/BaseList of strings.")

    if result.status_code not in range(200, 299):
        raise QualysAPIError(result.json())
    return result.json()
