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

