# VMDR APIs

VMDR APIs return data on vulnerabilities in your environment as well as from the Qualys KB. It also returns data on assets, IPs/subnets, asset groups, and more.

After running:
```py
from qualysdk.vmdr import *
```
You can use any of the VMDR endpoints currently supported:

## VMDR Endpoints

|API Call| Description |
|--|--|
| ```query_kb``` | Query the Qualys KnowledgeBase (KB) for vulnerabilities.|
| ```get_kb_qvs``` | Query the Qualys KB for CVEs and their associated details/scores.|
| ```get_host_list``` | Query your VMDR host inventory based on kwargs. |
|```get_hld``` | Query your VMDR host inventory with QID detections under the ```VMDRHost.DETECTION_LIST``` attribute.|
| ```get_cve_hld``` | Query your VMDR host inventory with CVE detections under the ```VMDRHost.DETECTION_LIST``` attribute.|
|```get_ip_list```| Get a list of all IPs in your subscription, according to kwarg filters.|
|```add_ips```| Add IP addresses to VMDR.|
|```update_ips```|Update details of IP addresses already in VMDR such as ```tracking_method```, ```owner```, etc.|
|```get_ag_list```| Get a list of all asset groups in your subscription, according to kwarg filters.|
|```add_ag```| Add a new asset group to VMDR.|
|```edit_ag```| Update details of an asset group.|
|```delete_ag```|Remove an asset group from VMDR.|
|```get_scan_list```| Get a list of VMDR scans in your subscription, according to kwarg filters.|
|```pause_scan```| Pause a running scan.|
|```resume_scan```| Resume a paused scan.|
|```cancel_scan```| Cancel a scan.|
|```delete_scan```| Delete a scan out of VMDR.|
|```launch_scan```| Create/launch a new VMDR scan.|
|```fetch_scan```| Pull the results of a VMDR scan as a ```pandas.DataFrame```.|
|```get_scanner_list```| Pull a list of VMDR scanner appliances.|
|```get_static_searchlists```| Pull a list of static search lists, according to the ```ids``` parameter.|
|```get_dynamic_searchlists``` | Pull a list of dynamic search lists, according to kwargs.|
|```get_report_list```| Pull a list of reports.|
|```launch_report```|Generate a new report.|
|```cancel_report```|Cancel an in-progress report.|
|```fetch_report```|Download the results of a report.|
|```delete_report```|Delete a report out of Qualys.|
|```get_scheduled_report_list```|Get a list of scheduled reports.|
|```launch_scheduled_report```|Launch a scheduled report.|
|```get_template_list```|Get a list of report templates.|
|```get_user_list```|Get a list of users in your subscription.|
|```add_user```|Add a new user to your subscription.|
|```edit_user```|Edit a user in your subscription.|
|```get_activity_log```| Pull the activity log for your Qualys subscription.|
| ```purge_hosts``` | Purge hosts from VMDR/Policy Compliance.|

## Host List Detection

```vmdr.get_hld()``` is the main API for extracting vulnerabilities out of the Qualys platform. It is one of the slowest APIs to return data due to Qualys taking a while to gather all the necessary data, but is arguably the most important. Pagination is controlled via the ```page_count``` parameter. By default, this is set to ```"all"```, pulling all pages. You can specify an int to limit pagination, as well as ```truncation_limit``` to specify how many hosts should be returned per page.

This function implements threading to significantly speed up data pulls. The number of threads is controlled by the ```threads``` parameter, which defaults to 5. A ```Queue``` object is created, containing chunks of hostIDs (pulled via ```get_host_list``` with ```details=None```) that the threads pop from. The threads then call the ```hld_backend``` function with the hostIDs they popped from the queue. The user can control how many IDs are in a chunk via the ```chunk_size``` parameter, which defaults to 3000. You should create a combination of ```threads``` and ```chunk_size``` that keeps all threads busy, while respecting your Qualys concurrency limit. There is also the ```chunk_count``` parameter, which controls how many chunks a thread will pull out of the ```Queue``` before it exits.

Some important kwargs this API accepts:

|Kwarg| Possible Values |Description|
|--|--|--|
|```show_tags```| ```False/True```|Boolean on if API output should include Qualys host tags. Accessible under ```<VMDRHost>.TAGS```. Defaults to False.|
|```show_asset_id```| ```False/True```|Boolean on if API output should include Qualys asset IDs. Accessible under ```<VMDRHost>.ASSET_ID```. Defaults to False.|
|```host_metadata```| ```'all','ec2','azure'```|Controls if cloud host details should be returned. It is **highly recommended** to use ```all``` if specified.|
|```show_cloud_tags```| ```False/True```|Boolean on if API output should include cloud provider tags. Accessible under ```<VMDRHost>.CLOUD_TAGS```. Defaults to False.|
|```filter_superseded_qids```|```False/True```|Boolean on if API output should only include non-superseded QIDs. Defaults to False.|
|```show_qds```|```False/True```|Boolean on if API output should include the Qualys Detection Score. Accessible under ```<VMDRHost>.QDS```. Defaults to False.|
|```show_qds_factors```|```False/True```|Boolean on if API output should include the Qualys Detection Score factors, such as EPSS score, CVSS score, malware hashes, and real-time threat indicators (RTIs). Accessible under ```<VMDRHost>.QDS_FACTORS```. Defaults to False.|
|```qids```|```None/QID_numbers```|Filter API output to a specific set of QIDs. Can be a comma-separated string: ```1357,2468,8901```, a range: ```12345-54321```, or a single QID: ```12345```.|
|```ids```|```None/hostIDs```|Filter API output to a specific set of host IDs. Can be a comma-separated string: ```1357,2468,8901```, a range: ```12345-54321```, or a single host ID: ```12345```.|

>**Heads Up!**: For a full breakdown of acceptable kwargs, see Qualys' documentation [here](https://cdn2.qualys.com/docs/qualys-api-vmpc-user-guide.pdf).

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import get_hld

auth = BasicAuth(<username>, <password>, platform='qg1')

# Example pulling all hosts with all details and kwargs
# with default threading and chunking settings:
hosts = get_host_list(
        auth,         
        details='All/AGs', 
        show_asset_id=True, 
        show_tags=True, 
        show_ars=True, 
        show_ars_factors=True, 
        show_trurisk=True, 
        show_trurisk_factors=True, 
        host_metadata='all', 
        show_cloud_tags=True,
)
>>>BaseList[VMDRHost(12345), ...]
```

## VMDR CVE Host List Detection

```vmdr.get_cve_hld()``` is a new version of the above ```get_hld``` function that returns a list of hosts with CVE detections under ```<VMDRHost>.DETECTION_LIST``` instead of QIDs. This function supports most of the same kwargs as ```get_hld``` and is also threaded.

|Kwarg| Possible Values |Description|Required|
|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```page_count```|```Literal['all']``` (default), ```int >= 0```| How many pages to pull. Note that ```page_count``` does not apply if ```truncation_limit``` is set to 0, or not specified.|❌|
|```threads```|```int >= 1```|The number of threads to use for data retrieval. Defaults to 5.|❌|
|```show_asset_id```| ```False/True```|Boolean on if API output should include Qualys asset IDs. Accessible under ```<VMDRHost>.ASSET_ID```. Defaults to False.|❌|
|```include_vuln_type```|```Literal["confirmed", "potential"]```|Filter API output to confirmed or potential vulnerabilities.|❌|
|```show_qvs```|```False/True```|Boolean on if API output should include the Qualys Vulnerability Score.|❌|
|```cve```| ```str```|Filter API output to a specific CVE/CVEs (comma-separated string).|❌|
|```truncation_limit``` | ```int```|Specify how many hosts should be returned per page. If set to 0 or not specified, returns all hosts in one pull.|❌|
|```ids```|```None/hostIDs```|Filter API output to a specific set of host IDs. Can be a comma-separated string: ```1357,2468,8901```, a range: ```12345-54321```, or a single host ID: ```12345```.|❌|
|```id_min```|```int```|Only return hosts with an ID >= ```id_min```.|❌|
|```id_max```|```int```|Only return hosts with an ID <= ```id_max```.|❌|
|```ips```|```str```|Filter API output to a specific set of IP addresses. Can be a comma-separated string: ```10.0.0.1,10.0.0.2```, a range: ```10.0.0.0-10.0.0.255```, or a single IP: ```10.0.0.1```.|❌|
|```ag_ids```|```str```|Filter API output to a specific set of asset group IDs. Can be a comma-separated string: ```1357,2468,8901```, a range: ```12345-54321```, or a single asset group ID: ```12345```.|❌|
|```ag_titles```|```str```|Filter API output to a specific set of asset group titles. Can be a comma-separated string: ```AG1,AG2,AG3```, or a single asset group title: ```AG1```.|❌|
|```vm_scan_since```|```str```|Filter API output to hosts that have been scanned since a specific date. Must be in the format ```YYYY-MM-DD```.|❌|
|```no_vm_scan_since```|```str```|Filter API output to hosts that have not been scanned since a specific date. Must be in the format ```YYYY-MM-DD```.|❌|
|```max_days_since_last_vm_scan```|```int```|Filter API output to hosts that have been scanned within a specific number of days.|❌|
|```vm_processed_after```|```str```|Filter API output to hosts where VM scan results were processed after a specific date. Must be in the format ```YYYY-MM-DD```.|❌|
|```vm_scan_date_before```|```str```|Filter API output to hosts where VM scan results were processed before a specific date. Must be in the format ```YYYY-MM-DD```.|❌|
|```vm_scan_date_after```|```str```|Filter API output to hosts where VM scan results were processed after a specific date. Must be in the format ```YYYY-MM-DD```.|❌|
|```vm_auth_scan_date_before```|```str```|Filter API output to hosts where VM authenticated scan results were processed before a specific date. Must be in the format ```YYYY-MM-DD```.|❌|
|```vm_auth_scan_date_after```|```str```|Filter API output to hosts where VM authenticated scan results were processed after a specific date. Must be in the format ```YYYY-MM-DD```.|❌|
|```status```|```Literal["New", "Active", "Fixed", "Re-Opened"]```| Filter API output to hosts with a specific CVE status. Multiple values can be passed as a comma-separated string: ```"New,Active"```.|❌|
|```compliance_enabled```|```bool```|Filter API output to hosts with compliance tracking enabled.|❌|
|```os_pattern```|```str```|Filter API output to hosts that match a specific OS regex pattern. Pattern must be valid according to the PCRE standard and be URL-encoded.|❌|
|```qids```|```Union[int,str]```| Filter API output to hosts with a specific set of QIDs. Can be a comma-separated string: ```1357,2468,8901```, a range: ```12345-54321```, or a single QID: ```12345```.|❌|
|```include_search_list_titles```|```str```|Filter API output to CVEs that are included in a search list by the list name. Multiple values can be passed as a comma-separated string: ```"Search List 1,Search List 2"```.|❌|
|```exclude_search_list_titles```|```str```|Filter API output to CVEs that are not included in a search list by the list name. Multiple values can be passed as a comma-separated string: ```"Search List 1,Search List 2"```.|❌|
|```include_search_list_ids```|```Union[int, str]```|Filter API output to CVEs that are included in a search list by the list ID. Can be a comma-separated string: ```1357,2468,8901```, a range: ```12345-54321```, or a single search list ID: ```12345```.|❌|
|```exclude_search_list_ids```|```Union[int, str]```|Filter API output to CVEs that are not included in a search list by the list ID. Can be a comma-separated string: ```1357,2468,8901```, a range: ```12345-54321```, or a single search list ID: ```12345```.|❌|
| ```filter_superseded_qids```|```False/True```|Boolean on if API output should only include non-superseded QIDs. Defaults to False.|❌|
|```use_tags```|```False/True```|Boolean on if API output should use tags for filtering. Defaults to False.|❌|
|```tag_set_by```|```Literal["id", "name"]``` = "id"|The type of tag to filter by. Defaults to ID.|❌|
|```tag_include_selector```|```Literal["any", "all"]``` = "any"|Choose if a host must have any or all tags to be included. Defaults to "any".|❌|
|```tag_exclude_selector```|```Literal["any", "all"]``` = "any"|Choose if a host must have any or all tags to be excluded. Defaults to "any".|❌|
|```tag_set_include```|```str```|The tag IDs/names to include. Can be a comma-separated string: ```1357,2468,8901```, or a single tag ID/name: ```1357```.|❌|
|```tag_set_exclude```|```str```|The tag IDs/names to exclude. Can be a comma-separated string: ```1357,2468,8901```, or a single tag ID/name: ```1357```.|❌|
|```show_tags```|```False/True```|Boolean on if API output should include Qualys host tags.|❌|
|```host_metadata```|```Literal["all", "ec2", "azure"]```|Controls if cloud host details should be returned. It is **highly recommended** to use ```all``` if specified.|❌|
|```host_metadata_fields```|```str```|Control which cloud metadata fields are returned. Can be a comma-separated string: ```"field1,field2,field3"```.|❌|
|```show_cloud_tags```|```False/True```|Boolean on if API output should include cloud provider tags.|❌|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import get_cve_hld

auth = BasicAuth(<username>, <password>, platform='qg1')

# Pull open, non-superseded, confirmed CVE detections for all hosts,
# including tags and cloud metadata/tags:

hosts = get_cve_hld(
    auth,
    show_tags=True,
    show_cloud_tags=True,
    filter_superseded_qids=True,
    include_vuln_type='confirmed'
    status='New,Active'
)
>>>BaseList[VMDRHost(12345), ...]

hosts[0].DETECTION_LIST[0]
>>>CVEDetection(
    VULN_CVE='CVE-2023-34058'
    UNIQUE_VULN_ID=1234567890, 
    TYPE='Confirmed', 
    SSL=True, 
    RESULTS='Some vulnerability.', 
    STATUS='Active', 
    FIRST_FOUND_DATETIME=datetime.datetime(2024, 10, 31, 1, 2, 3, tzinfo=datetime.timezone.utc), 
    LAST_FOUND_DATETIME=datetime.datetime(2025, 1, 10, 18, 29, 25, tzinfo=datetime.timezone.utc), 
    TIMES_FOUND=2887, 
    LAST_TEST_DATETIME=datetime.datetime(2025, 1, 10, 18, 29, 25, tzinfo=datetime.timezone.utc), 
    LAST_UPDATE_DATETIME=datetime.datetime(2025, 1, 10, 18, 29, 25, tzinfo=datetime.timezone.utc), 
    IS_IGNORED=True, 
    IS_DISABLED=True, 
    LAST_PROCESSED_DATETIME=datetime.datetime(2025, 1, 10, 18, 29, 25, tzinfo=datetime.timezone.utc), 
    LAST_FIXED_DATETIME=None, 
    ID=9876543210, 
    ASSOCIATED_QID=123456, 
    QID_TITLE='Some QID Title', 
    CVSS=1.2, CVSS_BASE='2.6 (AV:L/AC:H/Au:N/C:P/I:P/A:N)', 
    CVSS_TEMPORAL='1.9 (E:U/RL:OF/RC:C)', 
    CVSS_31=1.9, 
    CVSS_31_BASE='7.8 (AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H)', 
    CVSS_31_TEMPORAL='6.8 (E:U/RL:O/RC:C)', 
    QVS=35
)
```

## VMDR Host List
The ```get_host_list()``` API returns a ```BaseList``` of VMDRHost or VMDRID dataclasses. Pagination is controlled via the ```page_count``` kwarg. By default, this is set to ```"all"```, pulling all pages. By default, this is set to ```"all"```, pulling all pages. You can specify an int to limit pagination, as well as ```truncation_limit``` to specify how many hosts should be returned per page.

This function implements threading to significantly speed up data pulls. The number of threads is controlled by the ```threads``` parameter, which defaults to 5. A ```Queue``` object is created, containing chunks of hostIDs (pulled via ```get_host_list``` with ```details=None```) that the threads pop from. The threads then call the ```get_host_list_backend``` function with the hostIDs they popped from the queue. The user can control how many IDs are in a chunk via the ```chunk_size``` parameter, which defaults to 3000. You should create a combination of ```threads``` and ```chunk_size``` that keeps all threads busy, while respecting your Qualys concurrency limit. There is also the ```chunk_count``` parameter, which controls how many chunks a thread will pull out of the ```Queue``` before it exits.

Using the ```details``` kwarg, the shape of the output can be controlled:

|Details Value|Description|
|--|--|
|```None/"None"```| Return ```list[int]``` of host IDs (or asset IDs if ```show_asset_id=1```).|
|```"Basic"```| Return ```list[dict]``` containing basic host details, such as ID, DNS, IP, OS.|
|```"Basic/AGs"```| Return a ```list[dict]``` containing basic host details, plus asset group information.|
|```"All"```| Return a ```list[dict]``` containing all host details.|
|```"All/AGs"```| Return a ```list[dict]``` containing all host details plus asset group information.

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import get_host_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Pull 4 pages of hosts, with "All/AGs" details & tags, 
# where VM scan results were processed after a specific date:
yesterdays_scanned_assets = get_host_list(
    auth, 
    details="All/AGs",
    show_tags=True,
    vm_processed_after="2024-06-21",
    page_count=4
) 
```

## IP Management

This collection of APIs allows for the management of IP addresses/ranges in VMDR, located under ```qualysdk.vmdr.ips```. The APIs are as follows:

|API Call| Description|
|--|--|
|```get_ip_list```| Get a list of IP addresses or ranges in VMDR.|
|```add_ips```| Add IP addresses or ranges to VMDR.|
|```update_ips```| Change details of IP addresses or ranges from VMDR.|

### Get IP List API

The ```get_ip_list()``` API returns a list of all IP addresses or ranges in VMDR, matching the given kwargs. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```ips```|```str(<ip_address/range>)``` or ```BaseList[str, IPV4Address, IPV4Network, IPV6Address, IPV6Network]```|The IP address or range to search for.|❌|
|```network_id```|```str```|The network ID to search for.|❌ (usually not even enabled in a Qualys subscription)|
|```tracking_method```|```Literal['IP', 'DNS', 'NETBIOS']```| Return IPs/ranges based on the tracking method.|❌|
|```compliance_enabled```|```bool```|Return IPs/ranges based on if compliance tracking is enabled on it.|❌|
|```certview_enabled```|```bool```|Return IPs/ranges based on if CertView tracking is enabled on it.|❌|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr.ips import get_ip_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Get all IP addresses/ranges in VMDR that have CertView tracking enabled:
certview_ips = get_ip_list(auth, certview_enabled=True)

#Get specific IP addresses/ranges:
specific_ips = get_ip_list(auth, ips='1.2.3.4,5.6.7.8,9.10.11.12/24')

#Slice the list of IP addresses/ranges to those that are external:
external_ips = [i for i in get_ip_list(auth) if not i.is_private]
```

### Add IPs API
The ```add_ips()``` API allows for the addition of IP addresses or ranges to VMDR. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```ips```|```str(<ip_address/range>)``` or ```BaseList[str, IPV4Address, IPV4Network, IPV6Address, IPV6Network]```|The IP address or range to add.|✅|
|```tracking_method```|```Literal['IP', 'DNS', 'NETBIOS']```| The tracking method to use for the IP address/range.|❌|
|```enable_pc```|```bool```|Enable Policy Compliance tracking on the IP address/range.|See **Heads Up!** below.|
|```enable_vm```|```bool```|Enable Vulnerability Management tracking on the IP address/range.|See **Heads Up!** below.|
|```enable_sca```|```bool```|Enable Security Configuration Assessment tracking on the IP address/range.|See **Heads Up!** below.|
|```enable_certview```|```bool```|Enable CertView tracking on the IP address/range.|See **Heads Up!** below.|
|```tracking_method```|```Literal['IP', 'DNS', 'NETBIOS']```|The tracking method to use for the IP address/range. Defaults to IP.|❌|
|```owner```|```str```|The owner of the IP address/range.|❌|
|```ud1```|```str```|The user-defined field 1 (comment).|❌|
|```ud2```|```str```|The user-defined field 2 (comment).|❌|
|```ud3```|```str```|The user-defined field 3 (comment).|❌|
|```comment```|```str```|A comment to add to the IP address/range.|❌|
|```ag_title```|```str```|The title of the asset group to add the IP address/range to.|❌|

>**Heads Up!**: At least one of the following must be enabled: ```enable_pc```, ```enable_vm```, ```enable_sca```, or ```enable_certview```, or the API will return an error.

```py
from qualysdk import BasicAuth
from qualysdk.vmdr.ips import add_ips

auth = BasicAuth(<username>, <password>, platform='qg1')

#Add an IP address/range to VMDR with VM tracking enabled:
add_ips(auth, ips='1.2.3.4', enable_vm=True)
```

### Update IPs API
The ```update_ips()``` API allows for the modification of IP addresses or ranges in VMDR. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```ips```|```str(<ip_address/range>)``` or ```BaseList[str, IPV4Address, IPV4Network, IPV6Address, IPV6Network]```|The IP address or range to update.|✅|
|```tracking_method```|```Literal['IP', 'DNS', 'NETBIOS']```| The tracking method to use for the IP address/range.|❌|
|```host_dns```|```str```|The DNS name of the IP address/range.|❌|
|```host_netbios```|```str```|The NetBIOS name of the IP address/range.|❌|
|```owner```|```str```|The owner of the IP address/range.|❌|
|```ud1```|```str```|The user-defined field 1 (comment).|❌|
|```ud2```|```str```|The user-defined field 2 (comment).|❌|
|```ud3```|```str```|The user-defined field 3 (comment).|❌|
|```comment```|```str```|A comment to add to the IP address/range.|❌|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr.ips import update_ips

auth = BasicAuth(<username>, <password>, platform='qg1')

#Update an IP address/range in VMDR with a new DNS name:
update_ips(auth, ips='1.2.3.4', host_dns='new_dns_name')
```

## Asset Group Management
This collection of APIs allows for the management of asset groups (AGs) in VMDR, located under ```qualysdk.vmdr.assetgroups```. The APIs are as follows:

|API Call| Description|
|--|--|
|```get_ag_list```| Get a ```BaseList``` of ```AssetGroup``` objects.|
|```add_ag```| Add an asset group to VMDR.|
|```edit_ag```| Edit an asset group in VMDR.|
|```delete_ag```| Remove an asset group from VMDR.|


### Get Asset Group List API

The ```get_ag_list()``` API returns a list of all AGs in VMDR, matching the given kwargs. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```page_count```|```Literal['all']``` (default), ```int >= 0```| How many pages to pull. Note that ```page_count``` does not apply if ```truncation_limit``` is set to 0, or not specified.|❌|
|```ids```|```str```: '12345', '12345,6789'| Filter to specific AG IDs.|❌|
|```id_min```|```int```| Only return AGs with an ID >= ```id_min```.| ❌|
```id_max```|```int```| Only return AGs with an ID <= ```id_max```.|❌|
|```truncation_limit```| ```int```| Specify how many AGs per page. If set to 0 or not specified, returns all AGs in one pull.| ❌|
|```network_ids```|```str```: '12345', '12345,6789'| Only return AGs with specific network IDs.|❌|
|```unit_id```|```str```: 01234| Only return AGs with a specific unit ID. Only one ID is accepted.|❌|
|```user_id```|```str```| Only return AGs with a specific user assigned. Only one ID is accepted.|❌|
|```title```|```str```: "My Asset Group"| Only return AGs with a specific title. Must be an exact string match.|❌|
|```show_attributes```|```str```: 'ALL', 'ID', 'TITLE', 'ID,TITLE', ```...``` (For full list, check [Qualys documentation](https://cdn2.qualys.com/docs/qualys-api-vmpc-user-guide.pdf), under "Asset Group List" Section.| Only return specific attributes of an AG record. If not specified, basic details are returned (ID, TITLE, ```...```)|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_ag_list

auth = BasicAuth(<username>, <password>, platform='qg1')

ag_list = get_ag_list(auth)
```

### Add Asset Group API
The ```add_ag()``` API allows for the addition of asset groups to VMDR. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```title```|```str```|The title of the asset group.|✅|
|```comments```|```str```|Comments to add to the asset group.|❌|
|```division```|```str```|The division the asset group belongs to.|❌|
|```function```|```str```|The function of the asset group.|❌|
|```business_impact```|```Literal["critical", "high", "medium", "low", "none"]```|The business impact of the asset group.|❌|
|```ips```|```Union[str, BaseList[str, IPV4Address, IPV4Network, IPV6Address, IPV6Network]]```|The IP addresses or ranges to add to the asset group.|❌|
|```appliance_ids```|```Union[str, BaseList[int]]```|The appliance IDs to add to the asset group.|❌|
|```default_appliance_id```|```int```|The default appliance ID for the asset group.|❌|
|```domains```|```Union[str, BaseList[str]]```|The domains to add to the asset group.|❌|
|```dns_names```|```Union[str, BaseList[str]]```|The DNS names to add to the asset group.|❌|
|```netbios_names```|```Union[str, BaseList[str]]```|The NetBIOS names to add to the asset group.|❌|
|```cvss_enviro_cdp```|```Literal["high", "medium-high", "low-medium", "low", "none"]```|The CVSS environmental CDP of the asset group.|❌|
|```cvss_enviro_td```|```Literal["high", "medium", "low", "none"]```|The CVSS environmental TD of the asset group.|❌|
|```cvss_enviro_cr```|```Literal["high", "medium", "low"]```|The CVSS environmental CR of the asset group.|❌|
|```cvss_enviro_ir```|```Literal["high", "medium", "low"]```|The CVSS environmental IR of the asset group.|❌|
|```cvss_enviro_ar```|```Literal["high", "medium", "low"]```|The CVSS environmental AR of the asset group.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import add_ag

auth = BasicAuth(<username>, <password>, platform='qg1')

#Add an asset group to VMDR with a specific title:
add_ag(auth, title='My New Asset Group')
>>>Asset Group Added Successfully.
```

### Edit Asset Group API
The ```edit_ag()``` API allows for the modification of asset groups in VMDR. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[AssetGroup, BaseList[AssetGroup, int, str], str]```|The ID of the asset group to edit.|✅|
|```set_comments```|```str```|The comments to set for the asset group.|❌|
|```set_division```|```str```|The division to set for the asset group.|❌|
|```set_function```|```str```|The function to set for the asset group.|❌|
|```set_location```|```str```|The location to set for the asset group.|❌|
|```set_business_impact```|```Literal["critical", "high", "medium", "low", "none"]```|The business impact to set for the asset group.|❌|
|```add_ips```|```Union[str, BaseList[str, IPV4Address, IPV4Network, IPV6Address, IPV6Network]]```|The IP addresses or ranges to add to the asset group.|❌|
|```remove_ips```|```Union[str, BaseList[str, IPV4Address, IPV4Network, IPV6Address, IPV6Network]]```|The IP addresses or ranges to remove from the asset group.|❌|
|```set_ips```|```Union[str, BaseList[str, IPV4Address, IPV4Network, IPV6Address, IPV6Network]]```|The IP addresses or ranges to set for the asset group.|❌|
|```add_appliance_ids```|```Union[str, BaseList[int]]```|The appliance IDs to add to the asset group.|❌|
|```remove_appliance_ids```|```Union[str, BaseList[int]]```|The appliance IDs to remove from the asset group.|❌|
|```set_appliance_ids```|```Union[str, BaseList[int]]```|The appliance IDs to set for the asset group.|❌|
|```set_default_appliance_id```|```int```|The default appliance ID to set for the asset group.|❌|
|```add_domains```|```Union[str, BaseList[str]]```|The domains to add to the asset group.|❌|
|```remove_domains```|```Union[str, BaseList[str]]```|The domains to remove from the asset group.|❌|
|```set_domains```|```Union[str, BaseList[str]]```|The domains to set for the asset group.|❌|
|```add_dns_names```|```Union[str, BaseList[str]]```|The DNS names to add to the asset group.|❌|
|```remove_dns_names```|```Union[str, BaseList[str]]```|The DNS names to remove from the asset group.|❌|
|```set_dns_names```|```Union[str, BaseList[str]]```|The DNS names to set for the asset group.|❌|
|```add_netbios_names```|```Union[str, BaseList[str]]```|The NetBIOS names to add to the asset group.|❌|
|```remove_netbios_names```|```Union[str, BaseList[str]]```|The NetBIOS names to remove from the asset group.|❌|
|```set_netbios_names```|```Union[str, BaseList[str]]```|The NetBIOS names to set for the asset group.|❌|
|```set_title```|```str```|The title to set for the asset group.|❌|
|```set_cvss_enviro_cdp```|```Literal["high", "medium-high", "low-medium", "low", "none"]```|The CVSS environmental CDP to set for the asset group.|❌|
|```set_cvss_enviro_td```|```Literal["high", "medium", "low", "none"]```|The CVSS environmental TD to set for the asset group.|❌|
|```set_cvss_enviro_cr```|```Literal["high", "medium", "low"]```|The CVSS environmental CR to set for the asset group.|❌|
|```set_cvss_enviro_ir```|```Literal["high", "medium", "low"]```|The CVSS environmental IR to set for the asset group.|❌|
|```set_cvss_enviro_ar```|```Literal["high", "medium", "low"]```|The CVSS environmental AR to set for the asset group.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import edit_ag

auth = BasicAuth(<username>, <password>, platform='qg1')

#Edit an asset group in VMDR with a new title:
edit_ag(auth, id=12345, set_title='My New Asset Group Title')
>>>Asset Group Updated Successfully.
```


### Delete Asset Group API
The ```delete_ag()``` API allows for the deletion of asset groups in VMDR. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[AssetGroup, BaseList[AssetGroup, int, str], str]```|The ID of the asset group to delete.|✅|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import delete_ag

auth = BasicAuth(<username>, <password>, platform='qg1')

#Delete an asset group in VMDR:
delete_ag(auth, id=12345)
>>>Asset Group Deleted Successfully.
```

## VM Scan Management
This collection of APIs allows for the management of VM scans in VMDR, located under ```qualysdk.vmdr.vmscans```. 

>**Heads up!**: When VM scans change status, it will take a few minutes before interaction can continue. This is due to Qualys needing to update the scan status in their backend. Use ```get_scan_list()``` (described below) with a specific scan reference to check the status of a scan.

The APIs are as follows:

|API Call| Description|
|--|--|
|```get_scan_list```| Get a ```BaseList``` of ```VMScan``` objects.|
|```pause_scan```| Pause a currently-running VM scan.|
|```cancel_scan```| Cancel a currently-running VM scan.|
|```resume_scan```| Resume a paused VM scan.|
|```delete_scan```| Delete a VM scan.|
|```launch_scan```| Launch/create a VM scan.|
|```fetch_scan```| Fetch the results of a VM scan.|

### VMScan Dataclass

The ```VMScan``` dataclass is used to store the various fields that the VMDR VM Scan APIs return. Attributes are as follows:

|Attribute|Type|Description|
|--|--|--|
|```REF```|```str```|Reference string for the scan. Formatted as module/ID.|
|```TYPE```|```Literal["On-Demand","API","Scheduled]```|How the scan is ran.|
|```TITLE```|```str```|The scan name.|
|```USER_LOGIN```|```str```|The Qualys account that created/owns the scan.|
|```LAUNCH_DATETIME```|```datetime.datetime```|The date and time the scan was launched.|
|```DURATION```|```datetime.timedelta```|The duration of the scan.|
|```PROCESSING_PRIORTIY```|```str```|The processing priority of the scan. Includes an int followed by a description of the priority level, such as: ```0 - No Priority```.|
|```PROCESSED```|```bool```|If the scan results have been processed.|
|```STATUS```|```dict```|Status metadata points of the scan. Includes ```state```, which is saved into the ```STATE``` attribute.|
|```STATE```|```str```|The state of the scan.|
|```TARGET```|```Union[str, BaseList[str], BaseList[ipaddress.IPv4Address, ipaddress.IPv4Network]]```|The target IPs for the scan.|
|```OPTION_PROFILE```|```dict```|The option profile metadata for the scan.|
|```ASSET_GROUP_TITLE_LIST```|```BaseList[str]```|The asset group titles covered by the scan.|

### Get Scan List API

The ```get_scan_list()``` API returns a list of all VM scans in VMDR, matching the given kwargs. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```scan_ref```|```str```|The reference string of the scan to search for. Formatted like: ```scan/123455677```|❌|
|```state```|```Literal["Running", "Paused", "Cancelled", "Finished", "Error", "Queued", "Loading"]```|Filter by the state of the scan.|❌|
|```processed```|```bool```|Filter by if the scan results have been processed.|❌|
|```type```|```Literal["On-Demand","API","Scheduled]```|Filter by how the scan is set up.|❌|
|```user_login```|```str```|Filter by the Qualys account that created/owns the scan.|❌|
|```launched_after_datetime```|```str```|Filter by scans launched after a specific datetime. Formatted as: ```2007-07-01``` or ```2007-01-25T23:12:00Z```|❌|
|```launched_before_datetime```|```str```|Filter by scans launched before a specific datetime. Formatted as: ```2007-07-01``` or ```2007-01-25T23:12:00Z```|❌|
|```scan_type```|```Literal["certview", "ec2certview"]```|Only return certview scans, or EC2 certview scans.|❌|
|```client_id```|```Union[str,int]```|Filter by the client ID of the scan. This must be enabled in the Qualys subscription.|❌|
|```client_name```|```str```|Filter by the client name of the scan. This must be enabled in the Qualys subscription.|❌|
|```show_ags```|```bool```|Include asset group titles in the scan list.|❌|
|```show_op```|```bool```|Include option profile metadata in the scan list.|❌|
|```show_status```|```bool```|Include status metadata in the scan list. Defaults to ```True```.|❌|
|```show_last```|```bool```|Only show the last run of each scan. Defaults to ```False```.|❌|
|```ignore_target```|```bool```|Ignore the target IPs of the scan. Defaults to ```False```.|❌|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import get_scan_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Get all VM scans in VMDR, with all details, that have a type of Scheduled:
scheduled_scans = get_scan_list(auth, type='Scheduled', show_ags=True, show_op=True)
>>>BaseList[VMScan(REF='scan/123456789', TYPE='Scheduled', TITLE='My Scheduled Scan', ...), ...]
```


### Pause Scan API

The ```pause_scan()``` API lets you pause a currently-running VM scan in VMDR. Results are returned as a string, which is the response message from Qualys. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```scan_ref```|```str```|The reference string of the scan to pause. Formatted like: ```scan/123455677```|✅|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import pause_scan

auth = BasicAuth(<username>, <password>, platform='qg1')

result = pause_scan(auth, scan_ref='scan/123456789')
>>>Pausing scan
```

### Resume Scan API
The ```resume_scan()``` API lets you resume a paused VM scan in VMDR. Results are returned as a string, which is the response message from Qualys. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```scan_ref```|```str```|The reference string of the scan to resume. Formatted like: ```scan/123455677```|✅|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import resume_scan

auth = BasicAuth(<username>, <password>, platform='qg1')

result = resume_scan(auth, scan_ref='scan/123456789')
>>>Resuming scan
```

### Cancel Scan API
The ```cancel_scan()``` API lets you cancel a VM scan in VMDR. Results are returned as string, which is the response message from Qualys. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```scan_ref```|```str```|The reference string of the scan to cancel. Formatted like: ```scan/123455677```|✅|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import cancel_scan

auth = BasicAuth(<username>, <password>, platform='qg1')

result = cancel_scan(auth, scan_ref='scan/123456789')
>>>Cancelling scan
```

### Delete Scan API
The ```delete_scan()``` API lets you delete a VM scan in VMDR. Results are returned as a string, which is the response message from Qualys. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```scan_ref```|```str```|The reference string of the scan to delete. Formatted like: ```scan/123455677```|✅|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import delete_scan

auth = BasicAuth(<username>, <password>, platform='qg1')

result = delete_scan(auth, scan_ref='scan/123456789')
>>>Deleted scan
```

### Fetch Scan Results API
The ```fetch_scan()``` API lets you download the results of a VM scan. Results are returned as a ```pandas.DataFrame```. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```scan_ref```|```str```|The reference string of the scan to fetch. Formatted like: ```scan/123455677```|✅|
|```ips```|```str```| Only include results for specific IPs. Accepts a comma-separated string of IPs.|❌|
|```mode```|```Literal["brief", "extended"]```|The level of detail to include in the results. Defaults to ```brief```|❌|
|```client_id```|```Union[str,int]```|Filter by the client ID of the scan. This must be enabled in the Qualys subscription.|❌|
|```client_name```|```str```|Filter by the client name of the scan. This must be enabled in the Qualys subscription.|❌|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import fetch_scan

auth = BasicAuth(<username>, <password>, platform='qg1')

result = fetch_scan(auth, scan_ref='scan/123456789')
>>> pandas.DataFrame
```

### Launch Scan API
```launch_scan()``` is used to create and launch a new VM scan in VMDR. A ```VMScan``` object is returned containing the details of the scan once it is created via a ```get_scan_list()``` call with the ```scan_ref``` kwarg set to the newly-created scan reference. You can launch EC2 scans with the ```ec2_instance_ids```, ```ec2_endpoint```, and ```connector_name``` params. Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```runtime_http_header```|```str```|The value for the ```Qualys.Scan``` HTTP header to use for the scan.|❌|
|```scan_title```|```str```|The title of the scan.|❌|
|```option_id```|```int```|The option profile ID to use for the scan.|⚠️ (Must be specified if ```option_title``` is not specified)|
|```option_title```|```str```|The option profile title to use for the scan.|⚠️ (Must be specified if ```option_id``` is not specified)|
|```ip```|```Union[str, BaseList[str]```|The target IPs for the scan.|⚠️ (Must be specified if one of the following are not specified: ```asset_group_ids```, ```asset_groups```, ```fqdn```)|
|```asset_group_ids```|```Union[str, BaseList[str]```|The asset group IDs to use for the scan.|⚠️ (Must be specified if one of the following are not specified: ```ip```, ```asset_groups```, ```fqdn```)|
|```asset_groups```|```Union[str, BaseList[str]```|The asset group titles to use for the scan.|⚠️ (Must be specified if one of the following are not specified: ```ip```, ```asset_group_ids```, ```fqdn```)|
|```fqdn```|```Union[str, BaseList[str]```|The FQDNs to use for the scan.|⚠️ (Must be specified if one of the following are not specified: ```ip```, ```asset_group_ids```, ```asset_groups```, ```asset_groups```)|
|```iscanner_appliance_id```|```int```|The internal scanner appliance ID to use for the scan.|❌|
|```iscanner_name```|```str```|The internal scanner appliance name to use for the scan.|❌|
|```ec2_instance_ids```|```Union[str, BaseList[str]```|The EC2 instance IDs of your external scanners.|❌|
|```exclude_ip_per_scan```|```str, BaseList[str]```|The IPs to exclude from the scan.|❌|
|```default_scanner```|```bool```|Use the default scanner for the scan.|❌|
|```scanners_in_ag```|```bool```|Use the scanners in the asset group for the scan.|❌|
|```target_from```|```Literal["assets", "tags"]```| Choose to target assets based on the assets themselves or based on their tag list.|❌|
|```use_ip_nt_range_tags_include```|```bool```|Use the IP/NT range tags to include in the scan.|❌|
|```use_ip_nt_range_tags_exclude```|```bool```|Use the IP/NT range tags to exclude from the scan.|❌|
|```use_ip_nt_range_tags_include```|```bool```|Use the IP/NT range tags to include in the scan.|❌|
|```tag_selector_include```|```Literal["any", "all"]```| Choose if all tags must match for an asset or any tag can match.|❌|
|```tag_selector_exclude```|```Literal["any", "all"]```| Choose if all tags must match for an asset or any tag can match.|❌|
|```tag_set_by```|```Literal["id", "name"]```| Choose to search for tags by tag ID or tag name.|❌|
|```tag_set_include```|```Union[str, BaseList[str]```|The tags to include in the scan.|❌|
|```tag_set_exclude```|```Union[str, BaseList[str]```|The tags to exclude from the scan.|❌|
|```ip_network_id```|```str```|The IP network ID to use for the scan. Must be enabled in the Qualys subscription.|❌|
|```client_id```|```int```|The client ID to use for the scan. Only valid for consultant subscriptions.|❌|
|```client_name```|```str```|The client name to use for the scan. Only valid for consultant subscriptions.|❌|
|```connector_name```|```str```|The connector name for EC2 scans.|⚠️ Required for EC2 scans.|
|```ec2_endpoint```|```str```| The EC2 region code or VPC ID zone.|⚠️ Required for EC2 scans.|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import launch_scan

auth = BasicAuth(<username>, <password>, platform='qg1')

#Launch a new VM scan in VMDR with a specific title and option profile, targeting 2 specific IPs:
result = launch_scan(auth, scan_title='My New Scan', option_id=12345, ip='10.0.0.1,10.0.0.2', iscanner_name='internal_scanner_name')
>>>"New vm scan launched with REF: scan/123456789.12345"
result
>>>VMScan(REF='scan/123456789.12345', TYPE='API', TITLE='My New Scan', ...)
```

## VMDR Scanner Appliance Management

This collection of APIs allows for the management of scanner appliances in VMDR, located under ```qualysdk.vmdr.scanner_appliances```. 

### Scanner Appliance List API

The ```get_scanner_list``` API lets you pull a list of scanner appliances currently in VMDR, according to kwargs. 

>**Heads Up!**: While ```get_scanner_list``` currently does work, It is not finalized. Currently, some attributes under a ```ScannerAppliance``` dataclass are raw API output dictionaries/lists of dictionaries. This will be updated to use custom dataclasses soon.

Acceptable params are:

|Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```output_mode```| ```Literal["brief", "full"]```| Show some or all details of scanner appliances. Defaults to brief.|❌|
|```scan_detail```|```bool```| If ```True```, output includes scan details for scans that are currently running on an appliance.|❌|
|```show_tags```|```bool```| Show tag information for each scanner appliance in the output.|⚠️ Requires ```output_mode``` to be ```True``` to be able to be used.|
|```include_cloud_info```|```bool```| Show cloud provider information for a scanner appliance/. |⚠️ Requires ```output_mode``` to be ```True``` to be able to be used.|
|```busy```|```bool```| Filter output to scanners that are currently running scans.|❌|
|```scan_ref```|```str```| Filter output to scanners that are running a specific scan reference ID.|❌|
|```name```|```str```| Filter output to scanners with a specific name. Substring searching is supported. For example, if ```name=scanner```, and you have a scanner called ```main_scanner``` and one called ```backup_scanner```, both will be included.|❌|
|```ids```|```Union[str, int]```| Filter output to scanners with specific IDs. Can be a comma-separated string for multiple IDs.|❌|
|```type```|```Literal["physical", "virtual", "containerized", "offline"]```| Filter output to a specific type of scanner appliance.|❌|
|```platform_provider```|```Literal["ec2", "ec2_compat", "gce", "azure", "vCenter"]```| Filter output to scanners that are hosted on a specific provider.|❌|

```py
from qualysdk import BasicAuth
from qualysdk.vmdr import get_scanner_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Get all scanners, with all details, that are currently busy:
busy_scanners = get_scanner_list(
    auth, 
    busy=True, 
    output_mode="full", 
    scan_detail=True, 
    show_tags=True,
    include_cloud_info=True,
)
busy_scanners[0]
>>>ScannerAppliance(ID=12345, NAME="My Scanner", ...)
```

## Search List Management

Search lists help to filter QIDs in a subscription by specific QIDs, option profiles, etc. There are two types: static, and dynamic. Static search lists are a defined set of QIDs, while dynamic search lists update on their own based on vulnerability criteria. Currently, static search lists are implemented in their own dataclass, while dynamic search list support is coming soon.

### Get Static Search Lists API

```get_static_searchlists``` Lets you pull a list of static search lists in your subscription. It accepts a single parameter, ```ids``` and returns a ```BaseList``` of ```StaticSearchList``` objects. Inside a ```StaticSearchList```, the QIDs are stored in a ```BaseList``` of ```KBEntry``` objects.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```ids```|```str```| A comma-separated string of static search lists IDs to return.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_static_searchlists

auth = BasicAuth(<username>, <password>, platform='qg1')

#Get all search lists:
search_lists = get_static_searchlists(auth)
>>>[StaticSearchList(ID=12345, TITLE="My search list", QIDS=[KBEntry(12345, ...)], ...)]
```

### Get Dynamic Search Lists API

```get_dynamic_searchlists``` Lets you pull a list of static search lists in your subscription. It accepts a single parameter, ```ids``` and returns a ```BaseList``` of ```DynamicSearchList``` objects. 

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```ids```|```str```| A comma-separated string of dynamic search lists IDs to return.|❌|
|```show_qids```|```bool```| If ```True```, include the QIDs in the output.|❌|
|```show_option_profiles```|```bool```| If ```True```, include the option profiles in the output.|❌|
|```show_distribution_groups```|```bool```| If ```True```, include the distribution groups in the output.|❌|
|```show_report_templates```|```bool```| If ```True```, include the report templates in the output.|❌|
|```show_remediation_policies```|```bool```| If ```True```, include the remediation policies in the output.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_dynamic_searchlists

auth = BasicAuth(<username>, <password>, platform='qg1')

#Get all dynamic search lists:
dynamic_search_lists = get_dynamic_searchlists(auth)
>>>[DynamicSearchList(ID=12345, TITLE="My dynamic search list", ...)]
```

## VMDR Report Management

This collection of APIs lets you work with various types of reporting in VMDR.

The APIs are as follows:

|API Call| Description|
|--|--|
|```get_report_list```| Get a ```BaseList``` of ```VMDRReport``` objects.|
|```launch_report```|Create/Kick off new report generation.|
|```fetch_report```|Download the results of a report.|
|```cancel_report```|Cancel an in-progress report.|
|```delete_report```|Delete a report out of Qualys.|

### VMDRReport Dataclass

>**Head's Up!**: To allow for comparisons, the ```SIZE``` attribute of a ```VMDRReport``` is normalized to a float representation in megabytes. Raw Qualys API data returns this like: ```"5.01 KB"```. Should you ever create a ```VMDRReport``` object manually, specify the size as a string like the API output does.

The ```VMDRReport``` dataclass is used to represent a single report generated in VMDR. Attributes are as follows:

|Attribute|Type|Description|
|--|--|--|
|```ID```|```int```|The ID number for the report.|
|```TITLE```|```str```|The friendly name of the report.|
|```TYPE```|```str```|What type of data the report is for.|
|```USER_LOGIN```|```str```|The username that launched the report.|
|```LAUNCH_DATETIME```|```datetime.datetime```|When the report was kicked off.|
|```OUTPUT_FORMAT```|```str```|The file format the report is in.|
|```SIZE```|```float```|The file size of the report, in megabytes.|
|```STATUS```|```dict```|Raw API output for what ```STATE``` (see below) the report is in.|
|```STATE```|```str```|The state the report is in.|
|```EXPIRATION_DATETIME```|```datetime.datetime```|When the report expires.|

### VMDRScheduledReport Dataclass

The ```VMDRScheduledReport``` dataclass represents a scheduled report in VMDR. Attributes are as follows:

|Attribute|Type|Description|
|--|--|--|
|```ID```|```int```|The ID number for the report.|
|```TITLE```|```str```|The friendly name of the report.|
|```OUTPUT_FORMAT```|```str```|The file format the report is in.|
|```TEMPLATE_TITLE```|```str```|The template the report follows.|
|```ACTIVE```|```bool```|Whether the report is active or not.|
|```SCHEDULE```|```dict```|The schedule the report follows.|
|```START_DATE_UTC```|```datetime.datetime```|When the report started.|
|```START_HOUR```|```int```|The hour the report starts as an integer.|
|```START_MINUTE```|```int```|The minute the report starts as an integer.|
|```TIME_ZONE```|```dict```|Time zone information for the report. Gets parsed out to below fields.|
|```TIME_ZONE_CODE```|```str```|Time zone code for the report, such as ```"US-CT"```.|
|```TIME_ZONE_DETAILS```|```str```|Details for the time zone, such as GMT offset.|
|```DST_SELECTED```|```bool```|Boolean for if daylight savings time is enabled for the report.|

### VMDR Report List API

This API lets you pull a list of reports in your subscription, according to kwarg filters. Returns a ```BaseList``` of ```VMDRReport``` objects.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[int, str]```| A specific report ID to pull.|❌|
|```state```|```str```|Filter output to reports in a specific state.|❌|
|```user_login```|```str```|Filter output to reports launched by a specific user.|❌|
|```expires_before_datetime```|```str```|Filter output to reports that will expire before this datetime.|❌|
|```client_id```|```Union[int, str]```|Filter output to reports for a specific client ID. ⚠️ ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!|❌|
|```client_name```|```str```|Filter output to reports for a specific client name. ⚠️ ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_static_searchlists

auth = BasicAuth(<username>, <password>, platform='qg1')

#Get all reports launched by Alice:
alice_reports = get_report_list(auth, user_login='Alice')
>>>[VMDRReport(ID=01234567, TITLE="Alice's Scan", USER_LOGIN='alice_123',  OUTPUT_FORMAT='PDF', SIZE=10.42, ...), ...]
```

### Scheduled Reports List API

This API lets you pull a list of scheduled reports in VMDR, according to kwarg filters. Returns a ```BaseList``` of ```VMDRReport``` objects.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[int, str]```| A specific report ID to pull.|❌|
|```is_active```|```True/False```|Filter output to just active (```True```) or inactive (```False```) reports.|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_scheduled_report_list

auth = BasicAuth(<username>, <password>, platform='qg1')

#Get all active scheduled reports:
alice_reports = get_scheduled_report_list(auth, is_active=True)
>>>[VMDRScheduledReport(ID=17023223, TITLE='My Scheduled Report', ACTIVE=True, SCHEDULE={'WEEKLY': {'@frequency_weeks': '1', '@weekdays': '1'}}, ...), ...]
```

### Launch Report API

This API lets you launch or "kick off" a new report in VMDR. There are a few types of reports - see ```report_type``` below. Returns the report ID as an integer.

Acceptable kwargs are:

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```template_id```|```Union[int, str]``` |The template that the report will follow. Use ```get_report_template_list()``` To select one.|✅|
|```report_title```|```str```|The name to give to the report. ```⚠️ IF YOU REQUEST A PCI COMPLIANCE REPORT, THE TITLE IS AUTO-GENERATED BY QUALYS!```|❌|
```output_format```| FOR MAP REPORT: <br> ```pdf, html, mht, xml, csv```<br>FOR SCAN REPORT:<br>```pdf, html mht, xml, csv, docx```<br>FOR REMEDIATION REPORT:<br>```pdf, html, mht, csv```<br>FOR COMPLIANCE (NON-PCI) REPORT:<br>```pdf, html, mht```<br>FOR PCI COMPLIANCE REPORT:<br>```pdf, html```<br>FOR PATCH REPORT:<br>```pdf, online, xml, csv```<br>FOR COMPLIANCY POLICY REPORT:<br>```pdf, html, mht, xml, csv```|The format that the report will be generated in.|❌|
|```hide_header```|```True/False```| ⚠️ SDK auto-sets this to ```True```!|❌|
|```pdf_password```|```str```|If ```output_format==pdf```, file will be encrypted with this password. Note that this is required for ```recipient_group/recipient_group_id```. <br>⚠️ REQUREMENTS:<br>1.```8<=N<=32``` characters<br>2. Must contain alpha and numeric characters<br>3.Cannot match your Qualys account's password<br>4.Must follow any other password restrictions in ```Users->Setup->Security```|❌|
|```recipient_group```|```str```: ```"groupOne,GroupTwo"```|A comma-separated string of group that the PDF will be shared with. ⚠️ CANNOT BE IN THE SAME REQUEST WITH ```recipient_group_id```|❌|
|```recipient_group_id```|```str```|A comma-separated string of group IDs to share the PDF with. ⚠️ CANNOT BE IN THE SAME REQUEST WITH ```recipient_group```| ❌|
|```report_type```|```Literal["Map", "Scan", "Patch", "Remediation", "Compliance", "Policy"]```|Shape the report to a specific type.|❌|
|```domain```|```str```| Target domain for the report.|⚠️ REQUIRED FOR MAP REPORT|
|```ip_restriction```|Comma-separated string of IP addresses to include in a map report.|⚠️ REQUIRED FOR MAP REPORT WHEN ```domain=='None'```|
|report_refs|```str```|Comma-separated string of reference IDs.|⚠️ REQUIRED FOR MAP REPORT, MANUAL SCAN REPORT, PCI COMPLIANCE REPORT|
|```asset_group_ids```|```str```|Override asset group IDs defined in the report template with these IDs.|❌|
```ips_network_id```|```Union[int, str]```|Restrict the report to specific network IDs. ⚠️ MUST BE ENABLED IN THE QUALYS SUBSCRIPTION|❌|
|```ips```|```str```|Comma-separated string of IP addresses to include, overwriting the report template.|❌|
|```assignee_type```|```Literal["User", "All"]```|Specify if tickets assigned to the requesting user, or all tickets will be included in the report. Defaults to ```"User"```.|❌|
|```policy_id```|```Union[int, str]```|The specific policy to run the report on.|❌|
|```host_id```|```str```|In policy report output, show results for a single host. |⚠️ REQUIRED WHEN ```instance_string``` IS SPECIFIED.|
|```instance_string```|```str```|Specifies a single instance on a host machine.|⚠️ REQUIRED WHEN ```host_id``` IS SPECIFIED.|

**Head's Up!:** You can also use asset tags when creating a vulnerability or compliance report.

Acceptable kwargs for using tags are:

Parameter| Possible Values |Description|
|--|--|--|
|```use_tags```|```True/False```|Include/use asset tags. Defaults to ```False```.|
|```tag_include_selector```|```Literal["all", "any"]```| Include assets that match either any of the included tags, or all of them. Defaults to ```any```.|
|```tag_exclude_selector```|```Literal["all", "any"]```| Don't include assets that match either any of the included tags, or all of them. Defaults to ```any```.|
|```tag_set_by```|```Literal["id", "name"]```|Choose if you will include tags by their IDs or their names. Defaults to ```id```.
|```tag_set_include```|```str```|Comma-separated string of either tag IDs or names to include in the report.|
|```tag_set_exclude```|```str```|Comma-separated string of either tag IDs or names to exclude in the report.|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import launch_report

auth = BasicAuth(<username>, <password>, platform='qg1')

new_report_id = launch_report(auth)
>>>12345678
```

### Launch Scheduled Report API

This API lets you start an otherwise scheduled report. Returns the status message from Qualys as a string.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[int, str]``` |The ID number of the in-progress report to cancel.|✅|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import launch_scheduled_report

auth = BasicAuth(<username>, <password>, platform='qg1')

result = launch_scheduled_report(auth, id=012345678)
>>>Report launched
```

### Cancel Running Report API

This API cancels a report that is currently in progress. It returns a string with the Qualys response.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[int, str]``` |The ID number of the in-progress report to cancel.|✅|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import cancel_report

auth = BasicAuth(<username>, <password>, platform='qg1')

result = cancel_report(auth)
>>>Report cancelled
```

### Fetch Report Results API

This API lets you download the results of a report. The ```write_out``` parameter controls if the data is written to the ```<qualysdk_dir>/vmdr/output``` directory. By default, ```write_out``` is ```False```. If the report is in XML or CSV format, the data will be returned in a pandas DataFrame. Otherwise, ```write_out``` is set to ```True``` automatically, and results are written to disk. The output directory is created if it does not already exist.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[int, str]``` |The ID number of the in-progress report to cancel.|✅|
|```write_out```|```True/False```|Choose if you want the data written to disk in the ```output``` directory. Automatically set to ```True``` if the report format is not XML or CSV.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import fetch_report

auth = BasicAuth(<username>, <password>, platform='qg1')

# XML report:
report_data = fetch_report(auth, id=12345678)
>>>Detected XML format. Returning DataFrame.
                                                  ASSET_DATA_REPORT
HEADER               {'COMPANY': 'My Company', 'GENER...
RISK_SCORE_PER_HOST  {'HOSTS': [{'IP_ADDRESS': '10.0.0.1', 'TOT...
HOST_LIST            {'HOST': [{'IP': '10.0.0.2', 'TRACKING_METH...
GLOSSARY             {'VULN_DETAILS_LIST': {'VULN_DETAILS': [{'@id'...

#PDF report, automatically gets written to disk:
fetch_report(auth, id=92345678)
>>>Detected PDF format. Writing to <qualysdk_dir>/vmdr/output/<report_id>.pdf
Wrote report to <qualysdk_dir>/vmdr/output/<report_id>.pdf
```

### Delete Report API

This API deletes a report out of Qualys. It returns a string with the Qualys response.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```id```|```Union[int, str]``` |The ID number of the report to delete.|✅|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import delete_report

auth = BasicAuth(<username>, <password>, platform='qg1')

result = delete_report(auth)
>>>Report deleted
```

### List Report Templates API

This API lets you pull a list of all VMDR report templates in your account. Useful for when using ```launch_report``` and you need a value for ```template_id```. Returns a ```BaseList``` of ```ReportTemplate``` objects.

This API takes no parameters other than the ```BasicAuth``` object.

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_template_list

auth = BasicAuth(<username>, <password>, platform='qg1')

templates = get_template_list(auth)
>>>[ReportTemplate(ID=12345678, TYPE="Auto", ...)]
```

## User Management

This collection of APIs lets you work with user accounts in VMDR.

The APIs are as follows:

|API Call| Description|
|--|--|
|```get_user_list```| Get a ```BaseList``` of ```User``` objects.|
|```edit_user```|Edit a user account.|
|```add_user```|Add a new user account.|

### User Dataclass

The ```User``` dataclass is used to represent a single user account in VMDR. Attributes are as follows:

|Attribute|Type|Description|
|--|--|--|
|```USER_LOGIN```|```str```|The username of the user.|
|```USER_ID```|```int```|The ID number of the user.|
|```EXTERNAL_ID```|```str```|The external ID of the user.|
|```CONTACT_INFO```|```dict```|Contact information. Gets parsed out to below 14 fields.|
|```FIRSTNAME```|```str```|The first name of the user.|
|```LASTNAME```|```str```|The last name of the user.|
|```TITLE```|```str```|The title of the user.|
|```PHONE```|```str```|The phone number of the user.|
|```COUNTRY```|```str```|The country of the user.|
|```STATE```|```str```|The state of the user.|
|```CITY```|```str```|The city of the user.|
|```ZIP_CODE```|```str```|The ZIP code of the user.|
|```FAX```|```str```|The fax number of the user.|
|```EMAIL```|```str```|The email address of the user.|
|```COMPANY```|```str```|The company of the user.|
|```ADDRESS1```|```str```|The first line of the user's address.|
|```ADDRESS2```|```str```|The second line of the user's address.|
|```TIME_ZONE_CODE```|```str```|The time zone code of the user.|
|```USER_STATUS```|```str```|The status of the user.|
|```CREATION_DATE```|```datetime.datetime```|The date the user was created.|
|```USER_ROLE```|```dict```|The role of the user.|
|```LAST_LOGIN_DATE```|```datetime.datetime```|The last time the user logged in.|
|```BUSINESS_UNIT```|```str```|The business unit of the user.|
|```UNIT_MANAGER_POC```|```str```|The unit manager point of contact.|
|```MANAGER_POC```|```str```|The manager point of contact.|
|```UI_INTERFACE_STYLE```|```str```|The UI interface style of the user.|
|```PERMISSIONS```|```dict```|The permissions of the user. Gets parsed out to below 5 fields.|
|```CREATE_OPTION_PROFILES```|```bool```|If the user can create option profiles.|
|```PURGE_INFO```|```bool```|If the user can purge info.|
|```ADD_ASSETS```|```bool```|If the user can add assets.|
|```EDIT_REMEDIATION_POLICY```|```bool```|If the user can edit remediation policies.|
|```EDIT_AUTH_RECORDS```|```bool```|If the user can edit authentication records.|
|```CREATE_OPTION_PROFILES```|```bool```|If the user can create option profiles.|
|```NOTIFICATIONS```|```dict```|The notifications of the user. Gets parsed out to below 3 fields.|
|```LATEST_VULN```|```str```|How often the user gets vulnerability notifications.|
|```MAP```|```str```|How often the user gets map notifications.|
|```SCAN```|```str```|How often the user gets scan notifications.|
|```DAILY_TICKETS```|```int```|If the user gets daily ticket updates.|

### Get User List API

This API lets you pull a list of user accounts in your subscription, according to kwarg filters. Returns a ```BaseList``` of ```User``` objects.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```external_id_contains```|```str```|Filter output to users with a specific external ID pattern.|❌|
|```external_id_assigned```|```True/False```|Filter output to users with an external ID assigned.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import get_user_list

auth = BasicAuth(<username>, <password>, platform='qg1')

users = get_user_list(auth)
>>>[User(USER_ID=12345, USER_LOGIN='alice_123', ...), ...]
```

### Create User API

This API lets you create a new user account in VMDR. It returns a string with the Qualys response, or if the ```send_email``` kwarg is ```False```, the username and password of the new user.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```user_role```|```Literal["manager", "unit_manager", "scanner", "reader", "contact", "administrator"]```|The role of the user.|✅|
|```business_unit```|```Union[Literal["Unassigned"], str]```|The business unit of the user.|✅|
|```first_name```|```str```|The first name of the user.|✅|
|```last_name```|```str```|The last name of the user.|✅|
|```title```|```str```|The title of the user.|✅|
|```phone```|```str```|The phone number of the user.|✅|
|```email```|```str```|The email address of the user.|✅|
|```address1```|```str```|The first line of the user's address.|✅|
|```city```|```str```|The city of the user.|✅|
|```state```|```str```|The state of the user. Must be the full state name, such as ```"Maryland"``` or ```"Pennsylvania"```.|✅|
|```country```|```str```|The country of the user. Must be the full country name, such as ```"United States of America"```.|✅|
|```send_email```|```True/False```|If ```True```, an email will be sent to the user with their login information. If ```False```, the username and password will be returned in the response. Defaults to ```True```.|❌|
|```asset_groups```|```str```|A comma-separated string of asset groups to assign to the user.|❌|
|```fax```|```str```|The fax number of the user - because fax is still very widely used nowadays. 😉|❌|
|```address2```|```str```|The second line of the user's address.|❌|
|```zip_code```|```str```|The ZIP code of the user.|❌|
|```external_id```|```str```|The external ID of the user.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import add_user

auth = BasicAuth(<username>, <password>, platform='qg1')

# Add a new user to VMDR and send them an email:
result = add_user(auth, user_role='manager', business_unit='Unassigned', first_name='Alice', last_name='Smith', title='Manager', phone='555-555-5555', ...)
>>>User alice_123 created successfully.

# Add a new user to VMDR and return their username and password:
result = add_user(auth, user_role='manager', business_unit='Unassigned', first_name='Alice', last_name='Smith', title='Manager', phone='555-555-5555', ..., send_email=False)
>>>User alice_123 created. User:Pass is: alice_123, Password: 12345
```

### Edit User API

This API lets you edit an existing user account in VMDR. It returns a string with the Qualys response. Certain fields can not be edited. If you try to edit one of these, the SDK will raise a ```QualysAPIError``` Exception. You can also clear/"wipe" certain fields by specifiying an empty string in the kwarg.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
|```login```|```str```|The username of the user to edit.|✅|
|```asset_groups```|```str```|A comma-separated string of asset groups to assign to the user.|❌|
|```first_name```|```str```|The first name of the user.|❌|
|```last_name```|```str```|The last name of the user.|❌|
|```title```|```str```|The title of the user.|❌|
|```phone```|```str```|The phone number of the user.|❌|
|```fax```|```str```|The fax number of the user.|❌|
|```email```|```str```|The email address of the user.|❌|
|```address1```|```str```|The first line of the user's address.|❌|
|```address2```|```str```|The second line of the user's address.|❌|
|```city```|```str```|The city of the user.|❌|
|```state```|```str```|The state of the user. Must be the full state name, such as ```"Maryland"``` or ```"Pennsylvania"```.|❌|
|```country```|```str```|The country of the user. Must be the full country name, such as ```"United States of America"```.|❌|
|```zip_code```|```str```|The ZIP code of the user.|❌|
|```external_id```|```str```|The external ID of the user.|❌|

```py
from qualysdk.auth import BasicAuth
from qualysdk.vmdr import edit_user

auth = BasicAuth(<username>, <password>, platform='qg1')

# Edit Alice's phone number:
result = edit_user(auth, login='alice_123', phone='555-555-5555')
>>>User alice_123 has been successfully updated.

# Clear Alice's phone number:
result = edit_user(auth, login='alice_123', phone='')
>>>User alice_123 has been successfully updated.
```

## Querying the KB
The Qualys KnowledgeBase (KB) is a collection of vulnerabilities that Qualys has identified. You can query the KB using the ```query_kb()``` function:

>**Heads Up!**: When calling ```query_kb()```, the function returns a regular list of ```KBEntry``` objects.

```py
from qualysdk import BasicAuth, vmdr

with BasicAuth(<username>, <password>, platform='qg1') as auth:
    #Full KB pull:
    kb_query = vmdr.query_kb(auth)

    #or use kwargs to filter, 
    # for example QIDs published for a specific week:
    kb_query = vmdr.query_kb(auth, published_after='2024-06-21', published_before='2024-06-28')

    #Want to search the list of 
    # KBEntries based on some criteria?
    in_scope_qids = [entry for entry in kb_query if entry.QID in range(1000, 2000)]
    len(in_scope_qids)
>>>400
```

### Query CVE's Qualys Vulnerability Scores

```get_kb_qvs``` lets you query Qualys for QVS, EPSS, and CVSS scores for a comma-separated string of CVE IDs. Output also includes supporting details such as known threat actors, malware names/hashes, trending QIDs associated with the CVE, and more.

By default, returns all CVEs with QVS data.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
| ```cve``` | ```Union[str, list[str]]``` | A comma-separated string or list of strings of CVE IDs to query. | ❌ |
| ```details``` | ```Literal['Basic', 'All']``` | The level of detail to return. Defaults to ```Basic```, which only includes CVE ID, QVS score, and last changed/published dates.| ❌ |
| ```qvs_last_modified_before``` | ```str``` | Filter output to CVEs with a QVS score last modified before this date. Formatted like ```YYYY-MM-DD[THH:MM:SSZ]``` | ❌ |
| ```qvs_last_modified_after``` | ```str``` | Filter output to CVEs with a QVS score last modified after this date. Formatted like ```YYYY-MM-DD[THH:MM:SSZ]``` | ❌ |
| ```qvs_min``` | ```int``` | Filter output to CVEs with a QVS score greater than or equal to this value. | ❌ |
| ```qvs_max``` | ```int``` | Filter output to CVEs with a QVS score less than or equal to this value. | ❌ |
| ```nvd_published_before``` | ```str``` | Filter output to CVEs with an NVD score published before this date. Formatted like ```YYYY-MM-DD[THH:MM:SSZ]``` | ❌ |
| ```nvd_published_after``` | ```str``` | Filter output to CVEs with an NVD score published after this date. Formatted like ```YYYY-MM-DD[THH:MM:SSZ]``` | ❌ |


```py
from qualysdk import BasicAuth, vmdr

with BasicAuth(<username>, <password>, platform='qg1') as auth:
    cves = 'CVE-2021-44228'
    result = vmdr.get_kb_qvs(auth, cve=cves, details='All')
>>>[KBQVS(id='CVE-2021-44228', qvs=95, ...), ...]

# Get all CVEs:
with BasicAuth(<username>, <password>, platform='qg1') as auth:
    result = vmdr.get_kb_qvs(auth)
>>>[
    KBQVS(id='CVE-2021-44228', qvs=95, ...), 
    KBQVS(id='CVE-2021-40438', qvs=90, ...),  
    KBQVS(id='CVE-2021-40439', qvs=95, ...),  
    ...
]

# Pass a list of CVEs:
with BasicAuth(<username>, <password>, platform='qg1') as auth:
    cves = ['CVE-2021-44228', 'CVE-2021-40438', 'CVE-2021-40439']
    result = vmdr.get_kb_qvs(auth, cve=cves)
>>>[
    KBQVS(id='CVE-2021-44228', qvs=95, ...), 
    KBQVS(id='CVE-2021-40438', qvs=90, ...),  
    KBQVS(id='CVE-2021-40439', qvs=95, ...),  
    ...
]
```

## Get User Activity Log

```get_activity_log``` lets you pull a list of user activity logs in your subscription. Returns a ```BaseList``` of ```ActivityLog``` objects.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
| ```page_count``` | ```Union[int, 'all'] = 'all'``` | The number of pages to return. Defaults to ```'all'```. | ❌ |
| ```user_action``` | ```str``` | Filter output to logs with a specific user action, such as ```"login"``` or ```"launch"```. | ❌ |
| ```action_details``` | ```str``` | Filter output to logs with specific action details. | ❌ |
| ```username``` | ```str``` | Filter output to logs for a specific username. | ❌ |
| ```since_datetime``` | ```str``` | Filter output to logs since this datetime. Formatted like ```YYYY-MM-DD HH:ii:ss``` | ❌ |
| ```until_datetime``` | ```str``` | Filter output to logs until this datetime. Formatted like ```YYYY-MM-DD HH:ii:ss``` | ❌ |
| ```user_role``` | ```str``` | Filter output to logs for a specific user role. | ❌ |
| ```truncation_limit``` | ```int``` | Limit the number of log entries per page returned. | ❌ |

```py
from qualysdk import BasicAuth, vmdr

with BasicAuth(<username>, <password>, platform='qg4') as auth:
    # Get 3 pages of manager user details since 2024-06-01:
    activity_log = vmdr.get_activity_log(
        auth, 
        page_count=3
        user_role='Manager',
        since_datetime='2024-06-01 00:00:00'    
    )
>>>[ActivityLog(User_Name='alice_123', User_Role='Manager', Action='login', Details='Logged in', ...), ...]
```

## Purge Hosts API

```purge_hosts``` lets you purge hosts out of VMDR/PC. Returns a string with the Qualys response.

Depending on the requesting account's permissions, the scope of assets that can be purged is as follows:

| User Role | Can Purge Vuln Data | Can Purge Compliance Data |
|--|--|--|
| Manager | ✅ | ✅ |
| Auditor | ❌ | ✅ |
| Unit Manager, Scanner, Reader | ❌ (⚠️ Can be enabled if ```"Purge host information/history"``` is given as a permission) | ❌ (⚠️ Can be enabled if ```"Purge host information/history"``` is given as a permission) |


>**Heads Up!**: Scan results are not purged when you purge a host. Only the host and host data are purged.

Parameter| Possible Values |Description|Required|
|--|--|--|--|
|```auth```|```qualysdk.auth.BasicAuth```|The authentication object.|✅|
| ```data_scope``` | ```Literal['vm','pc', 'vm,pc'] = 'vm,pc'``` | Limit scope of purge, or specify ```vm,pc```/```pc,vm``` (the default) to delete both. | ❌ |
| ```ids``` |```str``` | A comma-separated string of host IDs to purge. | ❌ |
| ```ips``` | ```str``` | A comma-separated string of IP addresses to purge. | ❌ |
| ```ag_ids``` | ```str``` | A comma-separated string of asset group IDs to purge. | ❌ |
| ```ag_titles``` | ```str``` | A comma-separated string of asset group titles to purge. | ❌ |
| ```network_ids``` | ```str``` | A comma-separated string of network IDs to purge. ⚠️ REQUIRES NETWORK SUPPORT FEATURE ON SUBSCRIPTION | ❌ |
| ```no_vm_scan_since``` | ```str``` | Purge hosts that have not been scanned since this date. Formatted like ```YYYYMM-DD[THH:MM:SSZ]``` | ❌ |
| ```no_compliance_scan_since``` | ```str``` | Purge hosts that have not been scanned for compliance since this date. Formatted like ```YYYYMM-DD[THH:MM:SSZ]``` | ❌ |
| ```compliance_enabled``` | ```bool``` | Purge hosts activated for policy compliance. | ❌ |
| ```os_pattern``` | ```str``` | Purge hosts with a specific URL-encoded, PCRE OS regex pattern. | ❌ |

```py
from qualysdk import BasicAuth, vmdr

with BasicAuth(<username>, <password>, platform='qg4') as auth:
    # Purge hosts with IDs 12345 and 67890:
    result = vmdr.purge_hosts(auth, ids='12345,67890')
>>>Hosts Queued for Purging
```


## Special Dataclasses for VMDR

There are quite a few special dataclasses that are used in the VMDR module, as well as a ```BaseList``` class that is used to store these dataclasses and add some easier string functionality.

For example, for KB entries, there is the ```KBEntry``` class which holds the various fields that the Qualys KB API returns. Inside a ```KBEntry``` object there are custom classes for things like ```ThreatIntel``` and ```Software```. Other examples include the ```VMDRHost``` class, which holds the various fields that the VMDR Host List API returns, and the ```Detection``` class, which holds the various fields that the VMDR Host List Detection API returns under a ```VMDRHost```.
```py
... #Prior KB pull

#Get the ThreatIntel attribute of the a KBEntry object, which is a custom dataclass:
kb_entry.THREAT_INTELLIGENCE
>>>BaseList([ThreatIntel(ID=4, TEXT='High_Lateral_Movement')])

#Or perhaps you want all the CVEs in a CVEList as a comma-separated string:
str(kb_entry.CVEList)
>>>'CVE-2024-1234, CVE-2024-5678, ...'
```

### KB Dataclasses
|Class| Attributes |
|--|--|
| ```VendorReference``` | ID, URL|
| ```ThreatIntel```| ID, TEXT|
| ```Software``` | PRODUCT, VENDOR |
|```CVEID```| ID, URL |
|```Compliance``` | _TYPE, SECTION, DESCRIPTION |
| ```Bugtraq``` | ID, URL |
