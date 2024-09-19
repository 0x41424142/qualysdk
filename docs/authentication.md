# Auth Classes

```qualysdk``` supports both HTTP Basic Authentication (used mainly for VMDR-based calls) as well as JWT Authentication. 

>**Pro Tip**: Both ```BasicAuth``` and ```TokenAuth``` can be used as **context managers**!

>**Heads Up!**: By default, auth classes assume your Qualys subscription is on the ```qg3``` platform. If this is not the case, simply pass ```platform='qg<n>'``` where n is 1-4 when creating the object.

When calling an API endpoint, just pass your ```TokenAuth``` or ```BasicAuth``` object and the tool will handle the rest (or yell at you if you pass the wrong type, shown below):

```py
#Example of using the wrong auth type
from qualysdk.auth import BasicAuth
from qualysdk.gav import count_assets #GAV expects JWT auth

with BasicAuth(<username>,<password>, platform='qg1') as auth:
    count = count_assets(auth, filter='operatingSystem.category1:`Linux`')
    ...

>>>qualysdk.exceptions.Exceptions.AuthTypeMismatchError: Auth type mismatch. Expected token but got basic.
 ```

Both authentication objects also support automatic rate limit respecting. The SDK will warn you as you get close to an API endpoint's limit and automatically sleep until the limit is lifted, continuing the call afterwards (See below for an example with ```TokenAuth```)

## ```TokenAuth```-specific Notes

Qualys configures JWT tokens to expire 4 hours after they are created. When you make an API call using a ```TokenAuth``` object, ```qualysdk``` will automatically check if the token is expired and refresh it if necessary before making the call. This is especially useful if ```qualysdk``` throttles itself due to hitting your subscription's rate limit, where after sleeping for a variable amount of time (determined by the ```X-RateLimit-ToWait-Sec``` header) it will try the call again:

```py
# Example of being rate limited and qualysdk refreshing the token automatically:
>>>Warning: This endpoint will accept 2 more calls before rate limiting you. qualysdk will automatically sleep once remaining calls hits 0.

...

>>>WARNING: You have reached the rate limit for this endpoint. qualysdk will automatically sleep for <int> seconds and try again at approximately <datetime stamp>.

...
# After throttle is lifted:
>>>Token is 4+ hours old. Refreshing token...
```

## Other Notes on Auth Classes
 
Both ```BasicAuth``` and ```TokenAuth``` also have ```from_dict``` class methods, which allows for the creation of these objects from dictionaries:

```py
from qualysdk.auth import BasicAuth
auth = BasicAuth.from_dict({'username':<username>, 'password':<password>})
```

You can also create an object using a JSON string using ```from_json_string```:

```py
from qualysdk.auth import BasicAuth
auth = BasicAuth.from_json_string('{"username":<username>, "password":<password>}')
```

You can also export using ```to_json_string```. If ```pretty=True```, the string will be pretty formatted:

```py
from qualysdk.auth import BasicAuth
auth = BasicAuth.from_dict({'username':<username>, 'password':<password>})

#No formatting:
auth.to_json_string()
>>>'{"username": <username>, "password": <password>, "token": null, "auth_type": "basic", "platform": <platform>}'
#With formatting:
auth.to_json_string(pretty=True)
>>>{
    "username": <username>,
    "password": <password>,
    "token": null,
    "auth_type": "basic",
    "platform": <platform>
}
```

## Auth Class Hierarchy

The ```qualysdk.auth``` module has a class hierarchy that looks like this:

```mermaid
graph
A[qualysdk.auth.base.BaseAuthentication]-->B(qualysdk.auth.basic.BasicAuth)
B --> C(qualysdk.auth.token.TokenAuth)
```

## Checking Your Subscription's Rate Limit

Both ```BasicAuth``` and ```TokenAuth``` objects allow you to check your subscription's configured rate limits on the fly. To do this, call the ```get_ratelimit()``` method:

```py
from qualysdk import TokenAuth

auth = TokenAuth(<username>, <password>, platform='qg1')
auth.get_ratelimit()
>>>{'X-RateLimit-Limit': 1000, 'X-Concurrency-Limit-Limit': 10}
```
