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
    password=<password>, 
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
| ```upload_vmdr_cve_hld``` | VMDR | ```vmdr.get_cve_hld()```| ```vmdr_cve_hld_host_list``` for hosts and ```vmdr_cve_hld_detections``` for detections |
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
| ```upload_totalcloud_azure_vm``` | TotalCloud | ```totalcloud.get_inventory(provider='azure', resourceType='vm')``` | ```totalcloud_azure_vm_inventory``` |
| ```upload_totalcloud_azure_webapp``` | TotalCloud | ```totalcloud.get_inventory(provider='azure', resourceType='web app')``` | ```totalcloud_azure_webapp_inventory``` |
| ```upload_totalcloud_azure_storageaccount``` | TotalCloud | ```totalcloud.get_inventory(provider='azure', resourceType='storage account')``` | ```totalcloud_azure_storageaccount_inventory``` |
| ```upload_cs_containers``` | Container Security | ```cs.list_containers()``` | ```cs_containers``` |
| ```upload_cs_software``` | Container Security | ```cs.get_software_on_container()``` | ```cs_software``` |
| ```upload_cs_vulns``` | Container Security | ```cs.get_container_vulns()``` | ```cs_vulns``` |
| ```upload_was_webapps``` | WAS | ```was.get_webapps()``` or ```was.get_webapps_verbose()``` (```get_webapps_verbose()``` is recommended!) | ```was_webapps``` |
| ```upload_was_authentication_records``` | WAS | ```was.get_authentication_records()``` or ```was.get_authentication_records_verbose()``` (```get_webapps_verbose()``` is recommended!) | ```was_authentication_records``` |
| ```upload_was_findings``` | WAS | ```was.get_findings()``` or ```was.get_findings_verbose()``` (```get_findings_verbose()``` is recommended!) | ```was_findings``` |
| ```upload_was_scans``` | WAS | ```was.get_scans()``` or ```was.get_scans_verbose()``` (```get_scans_verbose()``` is recommended!) | ```was_scans``` |
| ```upload_pm_jobs``` | Patch Management | ```pm.list_jobs()``` | ```pm_jobs``` |
| ```upload_pm_job_results``` | Patch Management | ```pm.get_job_results()``` | ```pm_job_results_jobResults``` for job summaries and ```pm_job_results_assets``` for assets (key = jobResults.id -> assets.jobId)|
| ```upload_pm_job_runs``` | Patch Management | ```pm.get_job_runs()``` | ```pm_job_runs``` |
| ```upload_pm_cves``` | Patch Management | ```pm.lookup_cves()``` | ```pm_cves_for_qids``` |
| ```upload_pm_patches``` | Patch Management | ```pm.get_patches()``` | ```pm_patches``` |
| ```upload_pm_assets``` | Patch Management | ```pm.get_assets()``` | ```pm_assets``` |
| ```upload_pm_assetids_to_uuids``` | Patch Management | ```pm.lookup_host_uuids()``` | ```pm_assetids_to_uuids``` |
| ```upload_pm_patch_catalog``` | Patch Management | ```pm.get_patch_catalog()``` | ```pm_patch_catalog``` |
| ```upload_pm_linux_packages``` | Patch Management | ```pm.get_packages_in_linux_patch()``` | ```pm_linux_packages``` |
| ```upload_pm_windows_products``` | Patch Management | ```pm.get_products_in_windows_patch()``` | ```pm_windows_products``` |
| ```upload_pm_product_vuln_counts``` | Patch Management | ```pm.count_product_vulns()``` | ```pm_product_vuln_counts``` |
| ```upload_cert_certs``` | Certificate View | ```cert.list_certs()``` | ```cert_certs``` for certificates and ```cert_assets``` for assets (key = certs.id -> assets.certId) |
| ```upload_tagging_tags``` | Tagging | ```tagging.get_tags()``` | ```tagging_tags``` |

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

## The `upload_json` Function

`upload_json` allows you to upload data that is serializable to JSON to a SQL database. Any nested dictionaries or lists will be uploaded as JSON strings, allowing for more normalization to be done in the database. This is useful for data that is not easily represented in a flat table format, such as complex nested structures or large lists of items such as tags and vulnerability lists. Fields that are parsed out by the SDK inside their respective dataclasses will still be parsed out and uploaded as separate columns in the table.

```py
from qualysdk.sql import upload_json, db_connect

# Get a connection to the DB
cnxn = db_connect(
    db="my_test.db",
    db_type="sqlite",
)

# pull a few records from the Host List Detection API
vmdr_hosts = vmdr.get_hld(
    BasicAuth(<username>, <password>),
    show_asset_id=True,
    show_tags=True,
    show_cloud_tags=True,
    host_metadata="all",
    page_count=1,
    chunk_count=1,
    threads=1,
)

# NOTE: you MUST run <BaseList>.to_serializable_list() 
# on the data before uploading it to the DB
vmdr_hosts = vmdr_hosts.to_serializable_list()


# Upload the data to the DB
upload_json(vmdr_hosts, cnxn, table_name="vmdr_hld_with_json")
>>> Uploaded 12345 records to vmdr_hld
```