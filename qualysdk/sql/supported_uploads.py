"""
supported_uploads.py - Contains the functions to upload supported API pulls to SQL Server.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types

from .base import upload_data, prepare_dataclass
from ..vmdr.data_classes.lists import BaseList


def upload_vmdr_ags(
    ags: BaseList, cnxn: Connection, override_import_dt: datetime = None
) -> int:
    """
    Upload data from vmdr.get_ag_list() to SQL.

    Parameters:
    ags (BaseList): The Asset Group List to upload.
    cnxn (Connection): The Connection object to the SQL database.
    override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
    int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TITLE": types.String(),
        "OWNER_ID": types.Integer(),
        "OWNER_USER_ID": types.Integer(),
        "UNIT_ID": types.Integer(),
        "LAST_UPDATE": types.DateTime(),
        "NETWORK_ID": types.Integer(),
        "IP_SET": types.String(),
        "BUSINESS_IMPACT": types.String(),
        "DEFAULT_APPLIANCE_ID": types.Integer(),
        "APPLIANCE_IDS": types.String(),
        "DNS_LIST": types.String(),
        "NETBIOS_LIST": types.String(),
        "HOST_IDS": types.String(),
        "ASSIGNED_USER_IDS": types.String(),
        "ASSIGNED_UNIT_IDS": types.String(),
        "OWNER_USER_NAME": types.String(),
        "CVSS_ENVIRO_CDP": types.String(),
        "CVSS_ENVIRO_TD": types.String(),
        "CVSS_ENVIRO_CR": types.String(),
        "CVSS_ENVIRO_IR": types.String(),
        "CVSS_ENVIRO_AR": types.String(),
        "EC2_IDS": types.String(),
        "COMMENTS": types.String(),
        "DOMAIN_LIST": types.String(),
        "CLOUD_GROUP_NAME": types.String(),
        "CLOUD_INSTANCE_STATE": types.String(),
        "CLOUD_INSTANCE_TYPE": types.String(),
        "CLOUD_IS_SPOT_INSTANCE": types.Boolean(),
        "CLOUD_ARCHITECTURE": types.String(),
        "CLOUD_REGION": types.String(),
        "CLOUD_IMAGE_ID": types.String(),
        "CLOUD_AMI_ID": types.String(),
        "CLOUD_PUBLIC_HOSTNAME": types.String(),
        "CLOUD_PUBLIC_IPV4": types.String(),
        "CLOUD_ACCOUNT_ID": types.String(),
    }

    df = DataFrame([prepare_dataclass(ag) for ag in ags])

    # Upload the data:
    return upload_data(
        df, "vmdr_assetgroups", cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_vmdr_kb(
    kbs: BaseList, cnxn: Connection, override_import_dt: datetime = None
) -> int:
    """
    Upload data from vmdr.query_kb() to SQL.

    Parameters:
    kbs (BaseList): The KB List to upload.
    cnxn (Connection): The Connection object to the SQL database.
    override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
    int: The number of rows uploaded.
    """

    COLS = {
        "QID": types.Integer(),
        "VULN_TYPE": types.String(),
        "SEVERITY_LEVEL": types.Integer(),
        "TITLE": types.String(),
        "CATEGORY": types.String(),
        "LAST_SERVICE_MODIFICATION_DATETIME": types.DateTime(),
        "PUBLISHED_DATETIME": types.DateTime(),
        "CODE_MODIFIED_DATETIME": types.DateTime(),
        "BUGTRAQ_LIST": types.String(),
        "PATCHABLE": types.Boolean(),
        "SOFTWARE_LIST": types.String(),
        "VENDOR_REFERENCE_LIST": types.String(),
        "CVE_LIST": types.String(),
        "DIAGNOSIS": types.String(),
        "SOLUTION": types.String(),
        "CONSEQUENCE": types.String(),
        "CORRELATION": types.String(),
        "CVSS": types.String(),
        "CVSS_V3": types.String(),
        "PCI_REASONS": types.String(),
        "PCI_FLAG": types.Boolean(),
        "THREAT_INTELLIGENCE": types.String(),
        "SUPPORTED_MODULES": types.String(),
        "DISCOVERY": types.String(),
        "IS_DISABLED": types.Boolean(),
        "CHANGE_LOG": types.String(),
        "COMPLIANCE_LIST": types.String(),
        "TECHNOLOGY": types.String(),
        "LAST_CUSTOMIZATION": types.DateTime(),
        "SOLUTION_COMMENT": types.String(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(kb) for kb in kbs])

    # Upload the data:
    return upload_data(
        df,
        "vmdr_knowledgebase",
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_hosts(
    hosts: BaseList,
    cnxn: Connection,
    is_hld: bool = False,
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_host_list() to SQL.

    Parameters:
        hosts (BaseList): The Host List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        is_hld (bool): If the data is from a Host List Detail pull. You can ignore this.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.

    """

    COLS = {
        "ID": types.Integer(),
        "ASSET_ID": types.Integer(),
        "IP": types.String(),
        "IPV6": types.String(),
        "TRACKING_METHOD": types.String(),
        "DNS": types.String(),
        "NETBIOS": types.String(),
        "OS": types.String(),
        "QG_HOSTID": types.String(),
        "LAST_BOOT": types.DateTime(),
        "LAST_SCAN_DATETIME": types.DateTime(),
        "SERIAL_NUMBER": types.String(),
        "HARDWARE_UUID": types.String(),
        "FIRST_FOUND_DATE": types.DateTime(),
        "LAST_ACTIVITY": types.DateTime(),
        "LAST_ACTIVITY_DATE": types.DateTime(),
        "AGENT_STATUS": types.String(),
        "CLOUD_AGENT_RUNNING_ON": types.String(),
        "TAGS": types.String(),
        "LAST_VULN_SCAN_DATETIME": types.DateTime(),
        "LAST_VULN_SCAN_DATE": types.DateTime(),
        "LAST_VM_SCANNED_DATE": types.DateTime(),
        "LAST_VM_AUTH_SCANNED_DURATION": types.Integer(),
        "LAST_VM_SCANNED_DURATION": types.Integer(),
        "LAST_VM_AUTH_SCANNED_DATE": types.DateTime(),
        "LAST_COMPLIANCE_SCAN_DATETIME": types.DateTime(),
        "LAST_PC_SCANNED_DATE": types.DateTime(),
        "ASSET_GROUP_IDS": types.String(),
        "USER_DEF": types.String(),
        "OWNER": types.String(),
        "CLOUD_PROVIDER": types.String(),
        "CLOUD_SERVICE": types.String(),
        "CLOUD_RESOURCE_ID": types.String(),
        "EC2_INSTANCE_ID": types.String(),
        "CLOUD_GROUP_NAME": types.String(),
        "CLOUD_INSTANCE_STATE": types.String(),
        "CLOUD_INSTANCE_TYPE": types.String(),
        "CLOUD_IS_SPOT_INSTANCE": types.Boolean(),
        "CLOUD_ARCHITECTURE": types.String(),
        "CLOUD_REGION": types.String(),
        "CLOUD_IMAGE_ID": types.String(),
        "CLOUD_AMI_ID": types.String(),
        "CLOUD_PUBLIC_HOSTNAME": types.String(),
        "CLOUD_PUBLIC_IPV4": types.String(),
        "CLOUD_ACCOUNT_ID": types.String(),
        "CLOUD_PROVIDER_TAGS": types.String(),
        "ASSET_RISK_SCORE": types.Integer(),
        "TRURISK_SCORE": types.Integer(),
        "TRURISK_SCORE_FACTORS": types.String(),
        "ASSET_CRITICALITY_SCORE": types.Integer(),
    }

    # Remove METADATA and DNS_DATA from the dataclass. They're parsed out already from dataclass initialization.
    df = DataFrame([prepare_dataclass(host) for host in hosts])

    df.drop(columns=["METADATA", "DNS_DATA", "DETECTION_LIST"], inplace=True)

    # Upload the data, with table depdening on if it is a Host List Detail pull or not:
    return upload_data(
        df,
        "vmdr_hosts_list" if not is_hld else "vmdr_hld_hosts_list",
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_ips(
    ips: BaseList, cnxn: Connection, override_import_dt: datetime = None
) -> int:
    """
    Upload data from vmdr.get_ip_list() to SQL.

    Parameters:
        ips (BaseList): The IP List to upload from vmdr.get_ip_list().
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "IP": types.String(),
        "TYPE": types.String(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([str(ip) for ip in ips], columns=["IP"])

    # Add the TYPE column, which shows if it is a single IP or a range:
    df["TYPE"] = df["IP"].apply(lambda x: "Single IP" if "/" not in x else "IP Range")

    # Upload the data:
    return upload_data(
        df, "vmdr_ips", cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_vmdr_hld(
    hld: BaseList, cnxn: Connection, override_import_dt: datetime = None
) -> int:
    """
    Upload data from vmdr.get_hld() to SQL.

    Parameters:
        hld (BaseList): The Host List to upload.
        cnxn (Connection): The Connection object to the SQL database.

    Returns:
        int: The number of rows uploaded.

    """

    """
    Get_hld and get_host_list technically return the same data. get_hld just
    includes the DETECTION_LIST attribute. We can use the same upload function
    for the host part, and then snip off the DETECTION_LIST attribute to upload
    to a detections table.
    """

    # Isolate the detection lists. Since the Detection objects themselves
    # have an ID attribute, we can use that to link them back to the host.
    detections = BaseList()
    for host in hld:
        if host.DETECTION_LIST:
            for detection in host.DETECTION_LIST:
                detections.append(detection)

    # upload_vmdr_hosts automatically ignores the DETECTION_LIST attribute,
    # so we can use it here with the is_hld flag set to True to put the hosts
    # in a different table than get_host_list.
    hosts_uploaded = upload_vmdr_hosts(hld, cnxn, is_hld=True)
    print(
        f"Uploaded {hosts_uploaded} hosts to vmdr_hld_hosts_list. Moving to detections..."
    )

    COLS = {
        "UNIQUE_VULN_ID": types.BigInteger(),
        "QID": types.BigInteger(),
        "TYPE": types.String(),
        "SEVERITY": types.Integer(),
        "STATUS": types.String(),
        "SSL": types.Boolean(),
        "RESULTS": types.String(),
        "FIRST_FOUND_DATETIME": types.DateTime(),
        "LAST_FOUND_DATETIME": types.DateTime(),
        "QDS": types.Integer(),
        "QDS_FACTORS": types.String(),
        "TIMES_FOUND": types.Integer(),
        "LAST_TEST_DATETIME": types.DateTime(),
        "LAST_UPDATE_DATETIME": types.DateTime(),
        "IS_IGNORED": types.Boolean(),
        "IS_DISABLED": types.Boolean(),
        "LAST_PROCESSED_DATETIME": types.DateTime(),
        "LAST_FIXED_DATETIME": types.DateTime(),
        "PORT": types.Integer(),
        "PROTOCOL": types.String(),
        "FQDN": types.String(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(detection) for detection in detections])

    # Set QDS to an integer:
    df["QDS"] = df["QDS"].apply(lambda x: int(x) if x else None)

    # Upload the data:
    return upload_data(
        df,
        "vmdr_hld_detections",
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_scanners(
    scanners: BaseList, cnxn: Connection, override_import_dt: datetime = None
) -> int:
    """
    Upload data from vmdr.get_scanner_list() to SQL.

    Parameters:
        scanners (BaseList): The Scanner List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "NAME": types.String(),
        "SOFTWARE_VERSION": types.Float(),
        "RUNNING_SCAN_COUNT": types.Integer(),
        "STATUS": types.String(),
        "UUID": types.Uuid(),
        "RUNNING_SLICES_COUNT": types.Integer(),
        "MODEL_NUMBER": types.String(),
        "TYPE": types.String(),
        "SERIAL_NUMBER": types.String(),
        "ACTIVATION_CODE": types.BigInteger(),
        "INTERFACE_SETTINGS": types.String(),
        "PROXY_SETTINGS": types.String(),  # dict.
        "IS_CLOUD_DEPLOYED": types.Boolean(),
        "CLOUD_INFO": types.String(),  # dict. DROP THIS! INFO IS IN BELOW FIELDS:
        "PLATFORM_PROVIDER": types.String(),
        "INSTANCE_ID": types.String(),
        "AMI_ID": types.String(),
        "ACCOUNT_ID": types.String(),
        "INSTANCE_REGION": types.String(),
        "INSTANCE_AVAIBILITY_ZONE": types.String(),
        "INSTANCE_ZONE_TYPE": types.String(),
        "INSTANCE_VPC_ID": types.String(),
        "INSTANCE_SUBNET_ID": types.String(),
        "INSTANCE_ADDRESS_PRIVATE": types.String(),
        "INSTANCE_ADDRESS_PUBLIC": types.String(),
        "HOSTNAME_PRIVATE": types.String(),
        "SECURITY_GROUPS": types.String(),
        "API_PROXY_SETTINGS": types.String(),
        "VLANS": types.String(),  # dict.
        "STATIC_ROUTES": types.String(),  # dict.
        "ML_LATEST": types.String(),
        "ML_VERSION": types.String(),
        "VULNSIGS_LATEST": types.String(),
        "VULNSIGS_VERSION": types.String(),
        "ASSET_GROUP_COUNT": types.Integer(),
        "ASSET_GROUP_LIST": types.String(),  # BaseList
        "LAST_UPDATED_DATE": types.DateTime(),
        "POLLING_INTERVAL": types.Integer(),
        "USER_LOGIN": types.String(),
        "HEARTBEATS_MISSED": types.Integer(),
        "SS_CONNECTIION": types.String(),
        "SS_LAST_CONNECTED": types.DateTime(),
        "USER_LIST": types.String(),  # dict
        "UPDATED": types.String(),
        "COMMENTS": types.String(),
        "MAX_CAPACITY_UNITS": types.Float(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(scanner) for scanner in scanners])

    # Drop the CLOUD_INFO and EC2_INFO columns:
    df.drop(columns=["CLOUD_INFO"], inplace=True)

    # Upload the data:
    return upload_data(
        df, "vmdr_scanners", cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_static_searchlists(
    searchlists: BaseList, cnxn: Connection, override_import_dt: datetime = None
) -> int:
    """
    Upload data from vmdr.get_static_searchlists() to SQL.

    Parameters:
        searchlists (BaseList): The Search List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TITLE": types.String(),
        "GLOBAL": types.Boolean(),
        "OWNER": types.String(),
        "CREATED": types.DateTime(),
        "MODIFIED": types.DateTime(),
        "MODIFIED_BY": types.String(),
        "QIDS": types.String(),  # BaseList
        "OPTION_PROFILES": types.String(),  # dict
        "REPORT_TEMPLATES": types.String(),  # dict
        "REMEDIATION_POLICIES": types.String(),  # dict
        "DISTRIBUTION_GROUPS": types.String(),  # dict
        "COMMENTS": types.String(),  # dict
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(searchlist) for searchlist in searchlists])

    # Upload the data:
    return upload_data(
        df,
        "vmdr_static_searchlists",
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )
