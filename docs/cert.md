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

## ```qualysdk-cert``` CLI tool

The ```qualysdk-cert``` CLI tool is a command-line interface for the Certificate View portion of the SDK. It allows you to quickly pull down results from Certificate View APIs and save them to an XLSX file.

### Usage

```bash
usage: qualysdk-cert [-h] -u USERNAME -p PASSWORD [-P {qg1,qg2,qg3,qg4,eu1,eu2,eu3,in1,ca1,ae1,uk1,au1,ksa1}] [-oU api_url gateway_url qualysguard_url] {list_certs} ...

CLI script to quickly perform Certificate View (CERT) operations using qualysdk

positional arguments:
  {list_certs}          Action to perform
    list_certs          Get a list of certificates according to kwargs.

options:
  -h, --help            show this help message and exit
  -u, --username USERNAME
                        Qualys username
  -p, --password PASSWORD
                        Qualys password
  -P, --platform {qg1,qg2,qg3,qg4,eu1,eu2,eu3,in1,ca1,ae1,uk1,au1,ksa1}
                        Qualys platform
  -oU, --override_urls api_url gateway_url qualysguard_url
                        Override platform URLs with a custom URL set formatted like ... --override_urls https://custom-api-url https://custom-gateway-url https://custom-qualysguard-url
```

### List Certificates

```bash
usage: qualysdk-cert list_certs [-h] [-o OUTPUT] [--kwarg key value]

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output xlsx file to write results to
  --kwarg key value    Specify a keyword argument to pass to the action. Can be used multiple times
```