# Uploading Data to SQL Server

>**Head's Up!:** ```qualyspy.sql``` is currently in development and has been tested using Microsoft SQL Server only. It will be expanded to other databases in the future.

```qualyspy``` supports uploading data it has pulled to a SQL Server instance using various ```upload_*``` functions. Thanks to the Pandas library and qualyspy's ```BaseList``` class, uploading is rather easy.

## Steps to Get Going

### Step 1: Importing Functionality

```py
from qualyspy.sql import *
```

### Step 2: Building the Sqlalchemy Connection

Next, build your connection object. ```qualyspy``` supports username/password auth as well as trusted connections. It also supports specifying a custom driver (default driver is ```"ODBC Driver 17 for SQL Server"```):

```py

# Get a sqlalchemy.Connection using trusted_connection:
cnxn = db_connect(host='10.0.0.1', db='qualysdata', trusted_cnxn=True)

# Get a sqlalchemy.Connection with username/password auth:
cnxn = db_connect(host='10.0.0.1', db='qualysdata', username='Jane', password='SuperSecretPassword!')
```

### Step 3: Fire Away!

And finally, you can use the following supported functions:

>**Head's Up:** More upload functions are coming soon!

Each upload function takes 2 parameters. The first is the ```BaseList``` of data, and the second is the ```sqlalchemy.Connection``` object you built above.

| Function Name | Module  | ```qualyspy``` Function Data Source |
| -- | -- | -- |
| ```upload_ags``` | VMDR | ```vmdr.get_ag_list()```|
| ```upload_kb``` | VMDR | ```vmdr.query_kb()```|
| ```upload_vmdr_hosts``` | VMDR | ```vmdr.get_host_list()```|

## A Friendly Recommendation For Getting Data

When calling any of the data source functions to get the data to upload, it is recommended to make the call as verbose as possible via kwargs. 

For example, using ```vmdr.get_host_list()```, you should make your call look like the following so all data fields are captured:

```py

vmdr_hosts = vmdr.get_host_list
    (
        auth, 
        details='All/AGs', 
        show_asset_id=True, 
        show_tags=True, 
        show_ars=True, 
        show_ars_factors=True, 
        show_trurisk=True, 
        show_trurisk_factors=True, 
        host_metadata='all', 
        show_cloud_tags=True
    )
```