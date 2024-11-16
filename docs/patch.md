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
| ```jobId``` | ```str``` | The ID of the job to get results for | ✅ |
| ```jobInstanceId``` | ```str``` | The ID of the job instance to get results for. | ❌ |
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

## ```qualysdk-pm``` CLI tool

The ```qualysdk-pm``` CLI tool is a command-line interface for the PM portion of the SDK. It allows you to quickly pull down results from PM APIs and save them to an XLSX file.

### Usage

```bash
usage: qualysdk-pm [-h] -u USERNAME -p PASSWORD [-P {qg1,qg2,qg3,qg4}] {list_jobs,get_job_results} ...

CLI script to quickly perform Patch Management (PM) operations using qualysdk

positional arguments:
  {list_jobs,get_job_results}
                        Action to perform
    list_jobs           Get a list of PM jobs.
    get_job_results     Get results for a PM job.

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
usage: qualysdk-pm get_job_results [-h] [-o OUTPUT] -j JOB_ID [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output xlsx file to write results to
  -j, --job-id JOB_ID  Specify the job ID to get results for
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```