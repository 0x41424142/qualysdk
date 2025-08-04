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

`get_user_details` retrieves the details of a user or users by their admin user ID. These details include the users email, name, username, roles, scopes, and tags.

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

## Search Users by ID, Username, or Role Name

`search_users` searches for users in the Qualys platform by their admin ID, username, or role name. This is useful for finding users based on specific criteria so their roles and scopes can be updated.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```user_id``` | ```Union[int, str]``` | The ID of the user to search for. | ❌ |
| ```user_id_operator``` | ```Literal['EQUALS', 'GREATER', 'LESSER']``` | The operator to use when searching by user ID. Defaults to 'EQUALS'. | ❌ |
| ```username``` | ```str``` | The username of the user to search for. Search for multiple users by providing a comma-separated string or a list of strings. | ❌ |
| ```username_operator``` | ```Literal['CONTAINS', 'IN', 'EQUALS', 'NOT EQUALS', 'GREATER', 'LESSER', 'NONE', 'IS EMPTY']``` | The operator to use when searching by username. Defaults to 'EQUALS'. | ❌ |
| ```role_name``` | ```str``` | The name of the role to search for. Can be a single string, comma-separated string or a list of strings. | ❌ |

```py
from qualysdk.auth import BasicAuth
from qualysdk.admin import search_users

auth = BasicAuth(<username>, <password>, platform='qg1')

# Search for a user by ID:
user = search_users(auth, user_id=12345678)
>>>User(
    id=12345678,
    username='jdoe',
    firstName='John',
    ...,
)

# Search for users by username:
users = search_users(auth, username='jdoe')
>>>[
    User(
        id=12345678,
        username='jdoe',
        firstName='John',
        ...,
    ),
    User(
        id=87654321,
        username='jdoe2',
        firstName='Jane',
        ...,
    )
]

# Search for users that have a specific role:
users = search_users(auth, role_name='Role1')
>>>[
    User(
        id=87654321,
        username='jane',
        firstName='Jane',
        roleList=[
            AdminDataPoint(id=2, name='Role1'),
        ],
        ...
    ),
    User(
        id=12345678,
        username='jdoe',
        firstName='John',
        roleList=[
            AdminDataPoint(id=1, name='Role1'),
        ],
        ...
    )
]
```