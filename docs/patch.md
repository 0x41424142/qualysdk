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

## List Jobs API

```list_jobs``` returns a ```BaseList``` of patch management jobs in the user's account that match the given kwargs.

>**Head's Up!:** For the ```filter``` kwarg, see the linked documentation for the possible values: [Windows Jobs](https://docs.qualys.com/en/pm/3.1.0.0/search_tips/ui_jobs_list.htm), [Linux Jobs](https://docs.qualys.com/en/pm/3.1.0.0/search_tips/search_linux_jobs.htm)

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
| ```platform``` | ```Literal['windows', 'linux']``` | The platform of the job | ✅ |
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