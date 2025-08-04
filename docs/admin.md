# Administration APIs

Administration APIs return data on user management and other administrative tasks within your environment.

After running:
```py
from qualysdk.admin import *
```
You can use any of the Administration endpoints currently supported:

## Administration Endpoints

### Administration RBAC Endpoints

|API Call| Description |
|--|--|
| ```get_user_details``` | Query the administration details of a user or users by their admin user ID. |
| ```search_users``` | Search for users in the Qualys platform by ID, username, or role name. |
| ```update_user``` | Update a user's roles/scopes and tags by admin ID. |

### Administration Logs Endpoints

TODO

## Get Administration User Details

`get_user_details` Retrieves the details of a user or users by their admin user ID. These details include the users email, name, username, roles, scopes, and tags.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```user_id``` | ```Union[int, str, list[int], list[str]]``` | The ID(s) of the user(s) to retrieve details for. Can be a single ID, a list of IDs, or a list of IDs. | ✅ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.admin import get_user_details

auth = BasicAuth(<username>, <password>, platform='qg1')
# Get details for a single user by ID:
user = get_user_details(auth, user_id=12345678)
>>>User(
    id=12345678,
    username='jdoe',
    firstName='John',
    lastName='Doe',
    emailAddress='jdoe@example.com',
    title='Software Engineer',
    scopeTags=[
        AdminDataPoint(id=1, name='Production'),
        AdminDataPoint(id=2, name='Development'),
    ],
    roleList=[
        AdminDataPoint(id=1, name='Role1'),
        AdminDataPoint(id=2, name='Role2'),
    ]
)

# Get details for multiple users by ID:
users = get_user_details(auth, user_id=[12345678, 87654321])
>>>[
    User(
        id=12345678,
        username='jdoe',
        firstName='John',
        lastName='Doe',
        ...
    ),
    User(
        ...
    )
]
```
