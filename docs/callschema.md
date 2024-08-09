# The CALL_SCHEMA Dictionary
>**TL;DR**: The ```CALL_SCHEMA``` is ***VERY*** important! 

CALL_SCHEMA is a backend ```frozendict``` dictionary that the package automatically uses to correctly set up the underlying ```qualysdk.base.call_api()``` function. ```call_api``` in turn then sets up the appropriate ```requests.Request()``` call using an endpoint's schema.

The schema stores information such as what HTTP methods the endpoint accepts, the authentication type the endpoint expects, its path, acceptable kwargs when calling an API (and whether a kwarg should be sent as a URL parameter, in a POST form, or using the requests' library's ```json=``` feature), what Qualys URL structure to use (gateway vs. qualysapi), and more.

The schema also allows all API calls to raise an exception if the user passes in a kwarg that is not valid for an endpoint.

There are also some values that do not influence program behavior, but are "good-to-knows" for users. See below.

## Querying the CALL_SCHEMA
If you want to take a look at what an endpoint (or what an entire module's collection of endpoints!) expects, you can do so programmatically:
>**Pro Tip!**: use ```schema_query(...pretty=True)``` to return a beautified string of the query results.

```py
from qualysdk import schema_query

#Get one specific endpoint's schema:
print(schema_query(module='gav', endpoint='query_assets'))
>>>{'endpoint': '/am/v1/assets/host/filter/list', 'method': ['POST'], 'valid_params': ['filter', 'excludeFields', 'includeFields', 'lastModifiedDate', 'lastSeenAssetId', 'pageSize'], 'valid_POST_data': [], 'use_requests_json_data': False, 'return_type': 'json', 'pagination': True, 'auth_type': 'token'}

#Get an entire module's worth of endpoint schemas, 
# which includes the module-level url_type:
print(schema_query(module='gav', pretty=True))
>>>{
    "url_type": "gateway", #Used by call_api() to determine which URL format to use.
    "count_assets": {
        "endpoint": "/am/v1/assets/host/count",
        "method": [
            "POST"
        ],
        "valid_params": [
            "filter",
            "lastSeenAssetId",
            "lastModifiedDate"
        ],
        "valid_POST_data": [],
        "use_requests_json_data": false,
        "return_type": "json",
        "pagination": false,
        "auth_type": "token"
    },
    "get_all_assets": {
	    ...
	}
}
```

