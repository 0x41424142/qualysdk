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
```

## ```qualysdk-rbac``` CLI tool

The ```qualysdk-rbac``` CLI tool is a command-line interface for the RBAC (Role-Based Access Control) portion of the SDK. It allows you to quickly search users tags, scopes/roles, and update them as needed. You can optionally save the results to a file in JSON format.

### Usage

```bash
usage: qualysdk-rbac [-h] -u USERNAME -p PASSWORD [-P {qg1,qg2,qg3,qg4}] {get_user_details,search_users,update_user} ...

CLI script to quickly perform user permissions operations in the administration module using qualysdk.

positional arguments:
  {get_user_details,search_users,update_user}
                        Action to perform
    get_user_details    Get the details of a specific user from the Qualys administration module.
    search_users        Search for users in the admin module.
    update_user         Update an existing user's tags/scope.

options:
  -h, --help            show this help message and exit
  -u, --username USERNAME
                        Qualys username
  -p, --password PASSWORD
                        Qualys password
  -P, --platform {qg1,qg2,qg3,qg4}
                        Qualys platform
```

### Get User Details

```bash
usage: qualysdk-rbac get_user_details [-h] [-o OUTPUT] user_id

positional arguments:
  user_id              The administration ID of the user to retrieve details for

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output (json) file to write results to
```

### Search Users

```bash
usage: qualysdk-rbac search_users [-h] [-r ROLE] [-i USER_ID] [--id-operator {EQUALS,GREATER,LESSER}] [-qU QUALYS_USERNAME] [-a] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -r, --role ROLE       The role of the user(s) to search for
  -i, --user-id USER_ID
                        The user ID to search for
  --id-operator {EQUALS,GREATER,LESSER}
                        The operator to use for the user ID search
  -qU, --qualys-username QUALYS_USERNAME
                        The username to search for
  -a, --all             If set, will return all active users. Shorthand for `--user-id=1` & --id-operator='GREATER'.
  -o, --output OUTPUT   Output (json) file to write results to
```

## Update User

```bash
usage: qualysdk-rbac update_user [-h] [--add-tag-ids ADD_TAG_IDS [ADD_TAG_IDS ...]] [--add-tag-names ADD_TAG_NAMES [ADD_TAG_NAMES ...]] [--add-role-ids ADD_ROLE_IDS [ADD_ROLE_IDS ...]]
                                 [--add-role-names ADD_ROLE_NAMES [ADD_ROLE_NAMES ...]] [--remove-tag-ids REMOVE_TAG_IDS [REMOVE_TAG_IDS ...]]
                                 [--remove-tag-names REMOVE_TAG_NAMES [REMOVE_TAG_NAMES ...]] [--remove-role-ids REMOVE_ROLE_IDS [REMOVE_ROLE_IDS ...]]
                                 [--remove-role-names REMOVE_ROLE_NAMES [REMOVE_ROLE_NAMES ...]]
                                 user_id

positional arguments:
  user_id               ID of the user to update

options:
  -h, --help            show this help message and exit
  --add-tag-ids ADD_TAG_IDS [ADD_TAG_IDS ...]
                        List of tag IDs to add to the user. Use like: --add-tag-ids 123 456 789
  --add-tag-names ADD_TAG_NAMES [ADD_TAG_NAMES ...]
                        List of tag names to add to the user. Use like: --add-tag-names tag1 tag2 tag3
  --add-role-ids ADD_ROLE_IDS [ADD_ROLE_IDS ...]
                        List of role IDs to add to the user. Use like: --add-role-ids 123 456 789
  --add-role-names ADD_ROLE_NAMES [ADD_ROLE_NAMES ...]
                        List of role names to add to the user. Use like: --add-role-names role1 role2 role3
  --remove-tag-ids REMOVE_TAG_IDS [REMOVE_TAG_IDS ...]
                        List of tag IDs to remove from the user. Use like: --remove-tag-ids 123 456 789
  --remove-tag-names REMOVE_TAG_NAMES [REMOVE_TAG_NAMES ...]
                        List of tag names to remove from the user. Use like: --remove-tag-names tag1 tag2 tag3
  --remove-role-ids REMOVE_ROLE_IDS [REMOVE_ROLE_IDS ...]
                        List of role IDs to remove from the user. Use like: --remove-role-ids 123 456 789
  --remove-role-names REMOVE_ROLE_NAMES [REMOVE_ROLE_NAMES ...]
                        List of role names to remove from the user. Use like: --remove-role-names role1 role2 role3
```
