# Certificate View APIs

Certificate View APIs return data on certificates in the subscription.

After running:
```py
from qualysdk.cert import *
```
You can use any of the endpoints currently supported:

## Certificate View Endpoints

|API Call| Description |
|--|--|
| ```list_certs``` | Lists all certificates in the subscription that match given kwargs. |


## List Certificates API

```list_certs``` returns a list of certificates in the subscription that match the given kwargs.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.TokenAuth``` | Authentication object | ✅ |
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | Number of pages to pull | ❌ |
| ```certId``` | ```str``` | The ID of a certificate to return | ❌ |
| ```certId_operator``` | ```Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"] = "IS_NOT_EMPTY"``` | The operator to use for the certId | ❌ |
| ```hash``` | ```str``` | The hash of a certificate to return | ❌ |
| ```hash_operator``` | ```Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"] = "IS_NOT_EMPTY"``` | The operator to use for the hash | ❌ |
| ```validFromDate``` | ```str``` | The date the certificate is valid from | ❌ |
| ```validFromDate_operator``` | ```Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"] = "GREATER"``` | The operator to use for the validFromDate | ❌ |
| ```wasUrl``` | ```str``` | The URL of the site the certificate lives on, according to the WAS module | ❌ |
| ```wasUrl_operator``` | ```Literal["IN", "LESSER", "IS_EMPTY", "GREATER", "GREATER_THAN_EQUAL", "IS_NOT_EMPTY", "EQUALS", "NOT_EQUALS", "LESS_THAN_EQUAL", "CONTAINS"] = "IS_NOT_EMPTY"``` | The operator to use for the wasUrl | ❌ |
| ```certificateType``` | ```Literal["Leaf", "Intermediate", "Root"]``` | The type of certificate | ❌ |
| ```pageSize``` | ```int > 0 (default=10)``` | The number of certificates to return per page | ❌ |

```py
from qualysdk.auth import TokenAuth
from qualysdk.cert import list_certs

auth = TokenAuth(<username>, <password>, platform='qg1')

# Get all certificates:
certs = list_certs(auth)

# Get all certificates that match a given piece of a hash
# and are valid afer a certain date:
certs = list_certs(auth, hash='1234', hash_operator='CONTAINS', validFromDate='2024-01-01')
>>>[
    Certificate(
        id=12345678, 
        certhash='111222333444...', 
        keySize=2048, 
        serialNumber='12345...', 
        validToDate=datetime.datetime(2030, 1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        ...
    ),
    ...
]
```