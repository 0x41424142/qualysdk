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

> NOTE: To get all users, set `user_id` to `1` and `user_id_operator` to `'GREATER'`.

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

## Update User Roles and Tags

`update_user` updates a user's roles and tags by their admin ID. This is useful for managing user permissions and organization within the Qualys platform.

>Head's up! This API appears to be rather finicky with the user-provided values. You may notice that despite returning a `SUCCESS` response, the changes may not be applied as expected. If you encounter issues, try making changes across multiple API calls instead of all at once. For example, first add roles, then add tags, and finally remove roles or tags in separate calls.

|Parameter| Possible Values |Description| Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth``` | Authentication object | ✅ |
| ```user_id``` | ```int``` | The ID of the user to update. | ✅ |
| ```add_role_ids``` | ```list[int]``` | A list of role IDs to add to the user. | ❌ |
| ```add_role_names``` | ```list[str]``` | A list of role names to add to the user. | ❌ |
| ```remove_role_ids``` | ```list[int]``` | A list of role IDs to remove from the user. | ❌ |
| ```remove_role_names``` | ```list[str]``` | A list of role names to remove from the user. | ❌ |
| ```add_tag_ids``` | ```list[int]``` | A list of tag IDs to add to the user. | ❌ |
| ```add_tag_names``` | ```list[str]``` | A list of tag names to add to the user. | ❌ |
| ```remove_tag_ids``` | ```list[int]``` | A list of tag IDs to remove from the user. | ❌ |
| ```remove_tag_names``` | ```list[str]``` | A list of tag names to remove from the user. | ❌ |

<p style="color:red;font-size: 20px;"><b><u>Note that at least one of the add or remove parameters must be provided!</u></b></p>

```py
from qualysdk.auth import BasicAuth
from qualysdk.admin import update_user, search_users

auth = BasicAuth(<username>, <password>, platform='qg1')

#First, lets search for the user we want to update:
user = search_users(auth, username='jdoe')
>>>User(
    id=12345678,
    username='jdoe',
    ...
)

# Now we can update the user by their ID:
update_user(
    auth=auth,
    user_id=user.id,
    add_role_names=['New Role'],
    add_tag_names=['New Tag'],
    remove_role_names=['Old Role'],
    remove_tag_names=['Old Tag']
)
>>>SUCCESS

