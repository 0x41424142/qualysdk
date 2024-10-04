# Uploading Data to a SQL Database

```qualysdk``` supports uploading data it has pulled to a SQL Database using various ```upload_<module>_*``` functions. Thanks to the [Pandas library](https://pandas.pydata.org) and qualysdk's ```BaseList``` class, uploading is rather easy. ```qualysdk``` automatically will create the table for you if it does not exist, and will append data to the table if it does exist. The ```import_datetime``` field is also added to each table to track when the data was uploaded.

## Supported Databases

- SQL Server (```db_type='mssql'```)
- Postgresql (```db_type='postgresql'```)
- MySQL/MariaDB (```db_type='mysql'```)
- SQLite3 (```db_type='sqlite'```)

## Steps to Get Going

### Step 1: Importing Functionality

```py
from qualysdk.sql import *
```

### Step 2: Building the SQLAlchemy Connection

Next, build your connection object. ```qualysdk``` supports username/password auth as well as trusted connections for SQL Server. You can specify the type of DB you are connecting to (default is ```"mssql"```) via ```db_type```:

```py

# Get a sqlalchemy.Connection using trusted_connection to SQL Server.
# since db_type defaults to "mssql", you can omit it.
cnxn = db_connect(
    host='10.0.0.1', 
    db='qualysdata', 
    trusted_cnxn=True, 
    port=1433
)

# Get a sqlalchemy.Connection with username/password 
# auth to a Postgresql DB:
cnxn = db_connect(
    host='10.0.0.1', 
    db='qualysdata', 
    username='Jane', 
    password='SuperSecretPassword!', 
    db_type='postgresql', 
    port=5432
)
```

Note that you are required to call ```.close()``` on the connection object when you are done with it to close the connection to the DB.

```py

cnxn = db_connect(host='10.0.0.1', db='qualysdata', trusted_cnxn=True)

# Do some stuff with the connection
...

cnxn.close()
```

For connections to a SQLite3 database, you can use the following:

```py
cnxn = db_connect(
    db_type='sqlite',
    db='C:\\path\\to\\your\\sqlite.db' #Windows
)
```

### Step 3: Fire Away!

And finally, you can use the following supported functions:

>**Head's Up:** More upload functions are coming soon!

Each upload function takes 2 positional parameters. The first is the ```BaseList``` of data, and the second is the ```sqlalchemy.Connection``` object you built above. 

Functions also take an optional ```override_import_dt``` parameter that will set the resulting SQL table's ```import_datetime``` field to the value you specify. ```override_import_dt``` is a ```datetime.datetime``` object.

The final optional parameter is ```table_name```. If you want to specify a custom table name, you can do so with this parameter. Default table names are listed below. The one exception to this is ```vmdr.get_hld()```, which accepts ```vuln_table_name``` and ```hosts_table_name``` as optional parameters to specify the table names for the detections and hosts, respectively.


| Function Name | Module  | ```qualysdk``` Function Data Source | Default SQL Table Name |
| -- | -- | -- | -- |
| ```upload_vmdr_ags``` | VMDR | ```vmdr.get_ag_list()```| ```vmdr_assetgroups``` |
| ```upload_vmdr_kb``` | VMDR | ```vmdr.query_kb()```| ```vmdr_knowledgebase``` |
| ```upload_vmdr_kb_qvs``` | VMDR | ```vmdr.get_kb_qvs()```| ```vmdr_kb_qvs``` |
| ```upload_vmdr_hosts``` | VMDR | ```vmdr.get_host_list()```| ```vmdr_hosts_list``` |
| ```upload_vmdr_hld``` | VMDR | ```vmdr.get_hld()```| ```vmdr_hld_hosts_list``` for hosts and ```vmdr_hld_detections``` for detections |
| ```upload_vmdr_ips``` | VMDR | ```vmdr.get_ip_list()```| ```vmdr_ips``` |
| ```upload_vmdr_scanners``` | VMDR | ```vmdr.get_scanner_list()```| ```vmdr_scanners``` |
| ```upload_vmdr_static_search_lists``` | VMDR | ```vmdr.get_static_searchlists()```| ```vmdr_static_searchlists``` |
| ```upload_vmdr_dynamic_search_lists``` | VMDR | ```vmdr.get_dynamic_searchlists()```| ```vmdr_dynamic_searchlists``` |
| ```upload_vmdr_users``` | VMDR | ```vmdr.get_user_list()```| ```vmdr_users``` |
| ```upload_vmdr_scan_list``` | VMDR | ```vmdr.get_scan_list()```| ```vmdr_scans``` |
| ```upload_vmdr_report_list``` | VMDR | ```vmdr.get_report_list()```| ```vmdr_reports``` |
| ```upload_vmdr_scheduled_report_list``` | VMDR | ```vmdr.get_scheduled_report_list()```| ```vmdr_scheduled_reports``` |
| ```upload_vmdr_template_list``` | VMDR | ```vmdr.get_template_list()```| ```vmdr_report_templates``` |
| ```upload_vmdr_activity_log``` | VMDR | ```vmdr.get_activity_log()```| ```vmdr_activity_log``` |
| ```upload_gav_hosts``` | GAV | ```gav.get_all_assets()``` or ```gav.query_assets()``` | ```gav_hosts``` |
| ```upload_cloud_agents``` | Cloud Agent | ```cloud_agent.list_agents()``` | ```cloud_agent_agents``` |
| ```upload_totalcloud_aws_connectors``` | TotalCloud | ```totalcloud.get_connectors()``` | ```totalcloud_aws_connectors``` |
| ```upload_totalcloud_azure_connectors``` | TotalCloud | ```totalcloud.get_connectors()``` | ```totalcloud_azure_connectors``` |
| ```upload_totalcloud_control_metadata``` | TotalCloud | ```totalcloud.get_control_metadata()``` | ```totalcloud_control_metadata``` |
| ```upload_totalcloud_aws_s3``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='s3')``` | ```totalcloud_aws_s3_inventory``` |
| ```upload_totalcloud_aws_ec2``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='ec2')``` | ```totalcloud_aws_ec2_inventory``` |
| ```upload_totalcloud_aws_acl``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='acl')``` | ```totalcloud_aws_acl_inventory``` |
| ```upload_totalcloud_aws_rds``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='rds')``` | ```totalcloud_aws_rds_inventory``` |
| ```upload_totalcloud_aws_iamuser``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='iamuser')``` | ```totalcloud_aws_iamuser_inventory``` |
| ```upload_totalcloud_aws_vpc``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='vpc')``` | ```totalcloud_aws_vpc_inventory``` |
| ```upload_totalcloud_aws_securitygroup``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='sg')``` | ```totalcloud_aws_securitygroup_inventory``` |
| ```upload_totalcloud_aws_lambda``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='lambda')``` | ```totalcloud_aws_lambda_inventory``` |
| ```upload_totalcloud_aws_subnet``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='subnet')``` | ```totalcloud_aws_subnet_inventory``` |
| ```upload_totalcloud_aws_internetgateway``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='internet gateway')``` | ```totalcloud_aws_internetgateway_inventory``` |
| ```upload_totalcloud_aws_loadbalancer``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='load balancer')``` | ```totalcloud_aws_loadbalancer_inventory``` |
| ```upload_totalcloud_aws_routetable``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='route table')``` | ```totalcloud_aws_routetable_inventory``` |
| ```upload_totalcloud_aws_ebsvolume``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='ebs volume')``` | ```totalcloud_aws_ebsvolume_inventory``` |
| ```upload_totalcloud_aws_autoscalinggroup``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='auto scaling group')``` | ```totalcloud_aws_autoscalinggroup_inventory``` |
| ```upload_totalcloud_aws_ekscluster``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='eks cluster')``` | ```totalcloud_aws_ekscluster_inventory``` |
| ```upload_totalcloud_aws_eksnodegroup``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='eks nodegroup')``` | ```totalcloud_aws_eksnodegroup_inventory``` |
| ```upload_totalcloud_aws_fargateprofile``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='eks fargate profile')``` | ```totalcloud_aws_fargateprofile_inventory``` |
| ```upload_totalcloud_aws_vpcendpoint``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='vpc endpoint')``` | ```totalcloud_aws_vpcendpoint_inventory``` |
| ```upload_totalcloud_aws_vpcendpointservice``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='vpc endpoint service')``` | ```totalcloud_aws_vpcendpointservice_inventory``` |
| ```upload_totalcloud_aws_iamgroup``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='iam group')``` | ```totalcloud_aws_iamgroup_inventory``` |
| ```upload_totalcloud_aws_iampolicy``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='iam policy')``` | ```totalcloud_aws_iampolicy_inventory``` |
| ```upload_totalcloud_aws_iamrole``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='iam role')``` | ```totalcloud_aws_iamrole_inventory``` |
| ```upload_totalcloud_aws_sagemakernotebook``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='sagemaker notebook')``` | ```totalcloud_aws_sagemakernotebook_inventory``` |
| ```upload_totalcloud_aws_cloudfrontdistribution``` | TotalCloud | ```totalcloud.get_inventory(provider='aws', resourceType='cloudfront distribution')``` | ```totalcloud_aws_cloudfrontdistribution_inventory``` |
| ```upload_totalcloud_remediation_activities``` | TotalCloud | ```totalcloud.get_remediation_activities()``` | ```totalcloud_remediation_activities``` |
| ```upload_cs_containers``` | Container Security | ```cs.list_containers()``` | ```cs_containers``` |
| ```upload_was_webapps``` | WAS | ```was.get_webapps()``` or ```was.get_webapps_verbose()``` (```get_webapps_verbose()``` is recommended!) | ```was_webapps``` |

```py
from qualysdk.sql import *

# Get a connection to the DB
cnxn = db_connect(host='10.0.0.1', db='qualysdata', trusted_cnxn=True)

# Upload a previous vmdr.get_host_list() call to the DB, with override_import_dt set
# to 10-25-2023 12:00:00
dt = datetime.datetime(2023, 10, 25, 12, 0, 0)
uploaded = upload_vmdr_hosts(vmdr_hosts, cnxn, override_import_dt=dt)
>>>Uploaded 12345 records to vmdr_hosts_list
```

## A Friendly Recommendation For Getting Data

When calling any of the data source functions to get the data to upload, it is recommended to make the call as verbose as possible via kwargs, or if the function supports it, using the ```all_details``` parameter.

For example, using ```vmdr.get_host_list()```, you should make your call look like the following so all data fields are captured:

```py

vmdr_hosts = vmdr.get_host_list(
        auth, 
        all_details=True,
    )
```

For other calls, such as ```vmdr.get_hld()```, you should make your call look like the following:

```py
hosts_with_detections = vmdr.get_hld(
    auth,
    show_asset_id=True,
    show_tags=True,
    show_cloud_tags=True,
    host_metadata='all',
    show_qds=True,
    show_qds_factors=True,
)
```