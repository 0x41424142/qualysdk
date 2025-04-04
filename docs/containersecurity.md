# Container Security APIs

Container security APIs return data on containers, images, registries, and more in your subscription, as well as manage them.

After running:
```py
from qualysdk.cs import *
```
You can use any of the endpoints currently supported:

## Container Security Endpoints

|API Call| Description |
|--|--|
| ```list_containers``` | Lists all containers in the subscription that match given kwargs. |
| ```get_container_details``` | Returns detailed information about a single container instance. |
| ```get_software_on_container``` | Returns a list of software installed on a container - vulnerability counts by severity, software name, version, and more. |
| ```get_container_vuln_count``` | Returns a `dict` of vulnerability counts by severity for a container. |


## List Containers API

```list_containers``` returns a list of containers in the subscription that match the given kwargs. This method uses the ```/containers/list``` endpoint to fetch all containers in the subscription, overcoming the limit that the ```/containers``` endpoint has.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```filter``` | ```str``` | Filter string using [Qualys container security QQL](https://docs.qualys.com/en/cs/1.33.0/search/language.htm) | ❌ |
| ```paginationQuery``` | ```str``` | Pagination query string. The SDK handles this argument automatically | ❌ |
| ```limit``` | ```int``` | Number of records to return per page | ❌ |

```py
from qualysdk import TokenAuth
from qualysdk.cs import list_containers

auth = TokenAuth(<username>, <password>, platform='qg1')
# Get 4 pages of running containers:
containers = list_containers(auth, page_count=4, filter='state:`RUNNING`')
>>>[Container(imageId=12345, ...), ...]
```

## Get Container Details API

```get_container_details``` returns detailed information about a single container instance, specified by the ```containerSha``` argument. For containers pulled with qualysdk, the ```containerSha``` is accessible via the ```Container.sha``` dataclass attribute.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```containerSha``` | ```str``` | Sha hash of a container | ✅ |

```py
from qualysdk import TokenAuth
from qualysdk.cs import get_container_details, list_containers

auth = TokenAuth(<username>, <password>)
# Get a BaseList of containers:
containers = list_containers(auth, page_count=1)
# Get the details of the first container:
details = get_container_details(auth, containers[0].sha)
```

## Get Software on Container API

```get_software_on_container``` returns a list of software installed on a container, specified by the ```containerSha``` argument. For containers pulled with qualysdk, the ```containerSha``` is accessible via the ```Container.sha``` dataclass attribute.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```containerSha``` | ```str``` | Sha hash of a container | ✅ |
| ```filter``` | ```str``` | Filter string using [Qualys container security QQL](https://docs.qualys.com/en/cs/1.33.0/search/language.htm) | ❌ |
| ```sort``` | ```str``` | Sort string using [Qualys container security QQL](https://docs.qualys.com/en/cs/1.33.0/search/language.htm) | ❌ |
| ```isDrift``` | ```bool``` | Whether to include drifted software | ❌ |
| ```

```py
from qualysdk import TokenAuth
from qualysdk.cs import get_software_on_container, list_containers

auth = TokenAuth(<username>, <password>)
# Get a BaseList of containers:
containers = list_containers(auth, page_count=1)
# Get the software on the first container:
software = get_software_on_container(auth, containers[0].sha)
>>>[
    csSoftware(
        name='nginx',
        version='1.21.6',
        scanType='DYNAMIC',
        packagePath=None,
        fixVersion=None,
        vulnerabilities_severity5Count=1,
        vulnerabilities_severity4Count=2,
        vulnerabilities_severity3Count=3,
        vulnerabilities_severity2Count=4,
        vulnerabilities_severity1Count=5,
        containerSha='sha256:1234567890abcdef...',
    ),
    ...
]
```

## Get Container Vulnerability Count API

```get_container_vuln_count``` returns a dict of vulnerability counts by severity for a container, specified by the ```containerSha``` argument. For containers pulled with qualysdk, the ```containerSha``` is accessible via the ```Container.sha``` dataclass attribute.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```containerSha``` | ```str``` | Sha hash of a container | ✅ |

```py
from qualysdk import TokenAuth
from qualysdk.cs import get_container_vuln_count, list_containers
auth = TokenAuth(<username>, <password>)
# Get a BaseList of containers:
containers = list_containers(auth, page_count=1)
# Get the vulnerability count for the first container:
vuln_count = get_container_vuln_count(auth, containers[0].sha)
>>>{
    'severity5Count': 1,
    'severity4Count': 2,
    'severity3Count': 3,
    'severity2Count': 4,
    'severity1Count': 5,
}
```
