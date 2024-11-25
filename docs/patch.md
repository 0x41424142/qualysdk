# Patch Management APIs

PM APIs return data on patches, asset patch status/compliance, and patch jobs.

>**Head's Up!:** Qualys does not support MacOS for the patch management API.

After running:
```py
from qualysdk.pm import *
```

You can use any of the endpoints currently supported:

## PM Endpoints

|API Call| Description |
|--|--|
| ```list_jobs``` | Returns jobs that match given kwargs. |
| ```get_job_results``` | Returns a summary of a job. |
| ```get_job_runs``` | Returns a list of runs of a job. |
| ```create_job```| Creates a new job. |

## List Jobs API

```list_jobs``` returns a ```BaseList``` of patch management jobs in the user's account that match the given kwargs. if ```platform='all'```, it uses threading to speed up the process.

>**Head's Up!:** For the ```filter``` kwarg, see the linked documentation for the possible values: [Windows Jobs](https://docs.qualys.com/en/pm/3.1.0.0/search_tips/ui_jobs_list.htm), [Linux Jobs](https://docs.qualys.com/en/pm/3.1.0.0/search_tips/search_linux_jobs.htm)

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
| ```platform``` | ```Literal['all', 'windows', 'linux']='all'``` | The platform of the job | ❌ |
| ```page_count``` | ```Union[int, "all"] = "all"``` | The number of pages to return | ❌ |
| ```filter``` | ```str``` | The QQL filter to search for jobs | ❌ |
| ```attributes``` | ```str``` | The attributes to return in the response as a comma-separated string | ❌ |
| ```coauthorJob``` | ```bool=False``` | Only include jobs where the user is a coauthor | ❌ |
| ```ownedJob``` | ```bool=False``` | Only include jobs where the user is the sole owner | ❌ |
| ```pageSize``` | ```int=10``` | The number of jobs to return per page | ❌ |

```py
from qualysdk.auth import TokenAuth
from qualysdk.pm import list_jobs

auth = TokenAuth(<username>, <password>, platform='qg1')

# Get all Windows jobs:
win_jobs = list_jobs(auth, 'windows')
>>>[
    PMJob(
        name="My Job", 
        id="<job_guid>", 
        platform="Windows", 
        ...
    ), 
    ...
]
```

## Get Job Results API

```get_job_results``` returns the results of a patch management job.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
| ```jobId``` | ```Union[str, BaseList[PMJob, str]]``` | The ID(s) of the job to get results for. If a ```BaseList``` of ```PMJob``` objects is passed, the function will use threading. | ✅ |
| ```jobInstanceId``` | ```str``` | The ID of the job instance to get results for. Should not be used with threading. | ❌ |
| ```pageSize``` | ```int=10``` | The number of results to return per page | ❌ |
| ```sort``` | ```str``` | The field to sort the results by | ❌ |

```py
from qualysdk.auth import TokenAuth
from qualysdk.pm import get_job_results, list_jobs

auth = TokenAuth(<username>, <password>, platform='qg1')

# Get some job:
job = list_jobs(auth, 'linux')[0]

# Get the results summary for the job:
results = get_job_results(auth, job.id)
>>>JobResultSummary(
    id='11111111-2222-3333-4444-555555555555', 
    name='My Job', 
    assetCount=1, 
    patchCount=1, 
    createdBy=<username>, 
    createdOn=datetime.datetime(2020, 1, 2, 3, 12, 30, 777000), 
    assets=[
        PMAssetJobView(
            id='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
            name='Patch Asset', 
            operatingSystem='Red Hat Enterprise Linux 9.5',
            ...
        )
    ]
)

# Threading example:
jobs = list_jobs(auth)
results = get_job_results(auth, jobs)
```

## Get Job Runs API

```get_job_runs``` returns a list of runs of a patch management job.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
| ```jobId``` | ```str``` | The ID(s) of the job to get runs for | ✅ |

```py

from qualysdk.auth import TokenAuth
from qualysdk.pm import get_job_runs, list_jobs

auth = TokenAuth(<username>, <password>, platform='qg1')

# Get some job:
job = list_jobs(auth, 'linux')[0]

# Get the runs for the job:
runs = get_job_runs(auth, job.id)
>>>[
    PMRun(
        jobInstanceId=1, 
        jobId='11111111-2222-3333-4444-555555555555',
        scheduledDateTime=datetime.datetime(2020, 1, 1, 15, 32, 18, tzinfo=datetime.timezone.utc), 
        timezoneType='SPECIFIC_TZ'
    )
]
```

## Create Job API

```create_job``` creates a new patch management job.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
| ```name``` | ```str``` | The name of the job | ✅ |
| ```platform``` | ```Literal["Windows", "Linux"]``` | The platform of the job | ✅ |
| ```jobType``` | ```Literal["Install", "Rollback"]``` | The type of job to create. ```Rollback``` is Windows-only. | ✅ |
| ```scheduleType``` | ```Literal["On-demand", "Once", "Daily", "Weekly", "Monthly"]``` | The type of schedule to use | ✅ |
|```approvedPatches```|```List[str]```|An explicit list of patche GUIDs to add to the job|❌|
| ```assetIds``` | ```List[str]``` | The IDs of the assets to target | ❌ |
| ```assetTagIds``` | ```List[str]``` | The IDs of the asset tags to target | ❌ |
| ```filterType``` | ```Literal["all", "any"] = "any"``` | The type of filter to use | ❌ |
| ```exclusionTagIds``` | ```List[str]``` | The IDs of the asset tags to exclude | ❌ |
| ```exclusionAssetIds``` | ```List[str]``` | The IDs of the assets to exclude | ❌ |
| ```description``` | ```str``` | The description of the job | ❌ |
| ```coAuthorUserIds``` | ```List[str]``` | The IDs of the co-authors to add to the job | ❌ |
| ```exclusionFilterType``` | ```Literal["all", "any"] = "any"``` | The type of exclusion filter to use | ❌ |
| ```startDateTime``` | ```str``` | The start date and time of the job | ❌ for ```On-demand```, ✅ for others |
| ```recurring``` | ```bool=False``` | Whether the job is recurring | ❌ |
| ```dayOfMonth``` | ```int, 0 <= x <= 31``` | The day of the month to run the job | ❌ |
| ```matchAllTagIds``` | ```list[str]``` | The IDs of the asset tags to match | ❌ |
| ```recurringLastDayOfMonth``` | ```bool=False``` | Whether the job runs on the last day of the month | ❌ |
| ```monthlyRecurringType``` | ```Literal[0, 1, "0", "1"]``` | If 1, run on Patch Tuesday | ❌ |
| ```patchTuesdayPlusXDays``` | ```int, -27 <= x <= 27``` | The number of days before or after Patch Tuesday to run the job | ❌ |
| ```recurringDayOfMonth``` | ```int, 1 <= x <= 5``` | Run the job on a specific weekday of the month | ❌ |
| ```recurringWeekDayOfMonth``` | ```int, 0 <= x <= 6``` | The day of the week to run the job | ❌ |
| ```recurringWeekDays``` | ```str``` like ```"0,0,0,0,0,0,0"```| Similar to cron. Replace a 0 with a 1 to run on that day. str[0] = Sunday | ❌ |
| ```dynamicQQLType``` | ```Literal[0,1,2]``` | 0 = Do not use QQL, 1 = use patch QQL, 2 = use vulnerability QQL | ❌ |
| ```isDynamicPatchesQQL``` | ```bool=False``` | Whether to use dynamic patches QQL | ❌ |
| ```dynamicPatchesQQL``` | ```str``` | The QQL to use for dynamic patches | ❌ |
| ```continueOnPatchFailure``` | ```bool=True``` | (Linux only) Whether to continue the job if a patch fails | ❌ |
| ```preDeployment``` | ```str``` | Specify a message to display before deployment starts | ❌ |
| ```duringDeployment``` | ```str``` | Specify a message to display during deployment | ❌ |
| ```postDeployment``` | ```str``` | Specify a message to display after deployment | ❌ |
| ```onComplete``` | ```str``` | Specify a message to display when the job completes | ❌ |
| ```rebootCountdown``` | ```str``` | Specify a message to display before a reboot | ❌ |
| ```rebootOption``` | ```str``` | Specify a message for after a reboot | ❌ |
| ```suppressReboots``` | ```bool=False``` | Allow users to suppress reboots | ❌ |
| ```minimizeWindow``` | ```bool=False``` | Allow users to minimize the deployment window | ❌ |
| ```status``` | ```Literal["Disabled", "Enabled"] = "Disabled"``` | The status of the job | ❌ |
| ```timeout``` | ```int 1 <= x <= 168``` for hours, ```int 1 <= x <= 10080``` for minutes | The timeout for the job in hours or minutes (specified by timeoutUnit) | ❌ |
| ```timeoutUnit``` | Literal["HOURS", "MINUTES"] | The unit of the timeout | ❌ |
| ```timezoneType``` | ```Literal["AGENT_TZ", "SPECIFIC_TZ"]``` | The timezone type to use | ❌ |
| ```timezone``` | ```str``` | The (timezone)[https://docs.qualys.com/en/pm/api/deployment_job_resource/time_zones.htm] to use. For example: ```"America/New_York"``` | ❌ |
| ```opportunisticDownloads``` | ```bool=False``` | Whether to use opportunistic downloads. Only available for Windows | ❌ |
| ```linkedJobId``` | ```str``` | The ID of the job to link to | ❌ |
| ```notificationType``` | ```bool``` | If true, email notifications are sent | ❌ |
| ```notificationConfigRecipientEmail``` | ```str``` | The email to send notifications to | ❌ |
| ```notificationConfigCompletedPercentage``` | ```int 1 <= x <= 100``` | The percentage of completion to send notifications at | ❌ |
| ```notificationEvents``` | ```bool``` | If true, send notifications when ```onJobStart``` or ```onJobComplete``` are triggered | ❌ |
| ```downloadRandomizeTime``` | ```str``` | Provide the job randomize time in hours or minutes. Max is 2 hours or 120 minutes and must be less than the timeout/timeoutUnit | ❌ |
| ```downloadRandomizeTimeUnit``` | ```Literal["HOURS", "MINUTES"]``` | The unit of the randomize time | ❌ |
| ```additionalDynamicQQLType``` | ```Literal[1,2]``` | 1 = Use patch QQL, 2 = Use vulnerability QQL | ❌ |


### Example 1 with GAV Query


```py
from qualysdk.auth import TokenAuth
from qualysdk.pm import create_job
from qualysdk.gav import query_assets

# There are a few ways to pass in certain assets. If you have
# very particular assets in mind, you can make a GAV API
# call to get the agentIds of the assets you want to target:

windows_assets = query_assets(
  auth, 
  filter="operatingSystem.category: `Windows / Server`",
  includeFields="agentId",  
)

# PM uses GUIDs for almost everything, so we need 
# to extract the GUIDs from the assets:
windows_assets_ids = [asset.agentId for asset in windows_assets]

auth = TokenAuth(<username>, <password>, platform='qg1')

# Create a new job for Windows servers. Let's
# focus on critical patches only:
job = create_job(
    auth, 
    platform='Windows', 
    jobType='Install', 
    scheduleType='On-demand', 
    assetIds=windows_assets_ids,
    name='My Job',
    dynamicPatchesQQL="vendorSeverity:`Critical`",
    dynamicQQLType=1,
    isDynamicPatchesQQL=True,
    status="Enabled", # Immediately enable the job. By default, the job is disabled!
)
>>>"Job 11111111-2222-3333-4444-555555555555 (My Job) created successfully."
```

### Example 2 with Tag GUIDs

```py
from qualysdk.auth import TokenAuth
from qualysdk.pm import create_job

# Using PM tag GUIDs is a bit more cumbersome since
# Qualys does not provide an easy way to look up tag GUIDs, 
# but this method is much more flexible since new assets are
# picked up automatically by the job:

auth = TokenAuth(<username>, <password>, platform='qg1')

# Create a new job for Windows servers. Let's
# assume we have a tag for all Windows servers
# with GUID 22222222-3333-4444-5555-666666666666:

job = create_job(
    auth, 
    platform='Windows', 
    jobType='Install', 
    scheduleType='On-demand', 
    assetTagIds=['22222222-3333-4444-5555-666666666666'],
    name='My Job',
    dynamicPatchesQQL="vendorSeverity:`Critical`",
    dynamicQQLType=1,
    isDynamicPatchesQQL=True,
    status="Enabled", # Immediately enable the job. By default, the job is disabled!
)
>>>"Job 11111111-2222-3333-4444-555555555555 (My Job) created successfully."
```

## ```qualysdk-pm``` CLI tool

The ```qualysdk-pm``` CLI tool is a command-line interface for the PM portion of the SDK. It allows you to quickly pull down results from PM APIs and save them to an XLSX file.

### Usage

```bash
usage: qualysdk-pm [-h] -u USERNAME -p PASSWORD [-P {qg1,qg2,qg3,qg4}] {list_jobs,get_job_results,get_job_runs} ...
CLI script to quickly perform Patch Management (PM) operations using qualysdk

positional arguments:
  {list_jobs,get_job_results,get_job_runs}
                        Action to perform
    list_jobs           Get a list of PM jobs.
    get_job_results     Get results for a PM job.
    get_job_runs        Get runs for a PM job.

options:
  -h, --help            show this help message and exit
  -u, --username USERNAME
                        Qualys username
  -p, --password PASSWORD
                        Qualys password
  -P, --platform {qg1,qg2,qg3,qg4}
                        Qualys platform
```

### List Jobs

```bash
usage: qualysdk-pm list_jobs [-h] [-o OUTPUT] [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output xlsx file to write results to
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```

### Get Job Results

```bash
usage: qualysdk-pm get_job_results [-h] [-o OUTPUT] -j JOB_ID [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output xlsx file to write results to
  -j, --job-id JOB_ID  Specify the job ID to get results for. Can be used multiple times
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```

### Get Job Runs

```bash
usage: qualysdk-pm get_job_runs [-h] [-o OUTPUT] -j JOB_ID [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output xlsx file to write results to
  -j, --job-id JOB_ID  Specify the job ID to get runs for
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```