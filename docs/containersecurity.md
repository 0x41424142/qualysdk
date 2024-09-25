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