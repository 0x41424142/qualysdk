"""
vmdr.py - Contains the functions to upload supported VMDR API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.dialects.mssql import DATETIME2

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_vmdr_ags(
    ags: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_assetgroups",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_ag_list() to SQL.

    Args:
        ags (BaseList): The Asset Group List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_assetgroups'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "OWNER_ID": types.Integer(),
        "OWNER_USER_ID": types.Integer(),
        "UNIT_ID": types.Integer(),
        "LAST_UPDATE": types.DateTime(),
        "NETWORK_ID": types.Integer(),
        "IP_SET": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "BUSINESS_IMPACT": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DEFAULT_APPLIANCE_ID": types.Integer(),
        "APPLIANCE_IDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DNS_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "NETBIOS_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "HOST_IDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ASSIGNED_USER_IDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ASSIGNED_UNIT_IDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "OWNER_USER_NAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_ENVIRO_CDP": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_ENVIRO_TD": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_ENVIRO_CR": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_ENVIRO_IR": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_ENVIRO_AR": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "EC2_IDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "COMMENTS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DOMAIN_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_GROUP_NAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_INSTANCE_STATE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_INSTANCE_TYPE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_IS_SPOT_INSTANCE": types.Boolean(),
        "CLOUD_ARCHITECTURE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_REGION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_IMAGE_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_AMI_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_PUBLIC_HOSTNAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_PUBLIC_IPV4": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_ACCOUNT_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    df = DataFrame([prepare_dataclass(ag) for ag in ags])

    # Upload the data:
    return upload_data(
        df, table_name, cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_vmdr_kb(
    kbs: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_knowledgebase",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.query_kb() to SQL.

    Args:
        kbs (BaseList): The KB List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_knowledgebase'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "QID": types.Integer(),
        "VULN_TYPE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "SEVERITY_LEVEL": types.Integer(),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "CATEGORY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LAST_SERVICE_MODIFICATION_DATETIME": types.DateTime(),
        "PUBLISHED_DATETIME": types.DateTime(),
        "CODE_MODIFIED_DATETIME": types.DateTime(),
        "BUGTRAQ_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PATCHABLE": types.Boolean(),
        "SOFTWARE_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "VENDOR_REFERENCE_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVE_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DIAGNOSIS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "SOLUTION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CONSEQUENCE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CORRELATION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "CVSS_V3": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PCI_REASONS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PCI_FLAG": types.Boolean(),
        "THREAT_INTELLIGENCE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "SUPPORTED_MODULES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DISCOVERY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "IS_DISABLED": types.Boolean(),
        "CHANGE_LOG": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "COMPLIANCE_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TECHNOLOGY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LAST_CUSTOMIZATION": types.DateTime(),
        "SOLUTION_COMMENT": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PATCH_PUBLISHED_DATE": types.DateTime().with_variant(DATETIME2, "mssql"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(kb) for kb in kbs])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_hosts(
    hosts: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_hosts_list",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_host_list() to SQL.

    Args:
        hosts (BaseList): The Host List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_hosts_list'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.

    """

    COLS = {
        "ID": types.Integer(),
        "ASSET_ID": types.Integer(),
        "IP": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "IPV6": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "TRACKING_METHOD": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DNS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "NETBIOS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "OS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "QG_HOSTID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LAST_BOOT": types.DateTime(),
        "LAST_SCAN_DATETIME": types.DateTime(),
        "SERIAL_NUMBER": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "HARDWARE_UUID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "FIRST_FOUND_DATE": types.DateTime(),
        "LAST_ACTIVITY": types.DateTime(),
        "LAST_ACTIVITY_DATE": types.DateTime(),
        "AGENT_STATUS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_AGENT_RUNNING_ON": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TAGS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "LAST_VULN_SCAN_DATETIME": types.DateTime(),
        "LAST_VULN_SCAN_DATE": types.DateTime(),
        "LAST_VM_SCANNED_DATE": types.DateTime(),
        "LAST_VM_AUTH_SCANNED_DURATION": types.Integer(),
        "LAST_VM_SCANNED_DURATION": types.Integer(),
        "LAST_VM_AUTH_SCANNED_DATE": types.DateTime(),
        "LAST_COMPLIANCE_SCAN_DATETIME": types.DateTime(),
        "LAST_PC_SCANNED_DATE": types.DateTime(),
        "ASSET_GROUP_IDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "USER_DEF": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "OWNER": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "CLOUD_PROVIDER": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_SERVICE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_RESOURCE_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "EC2_INSTANCE_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_GROUP_NAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_INSTANCE_STATE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_INSTANCE_TYPE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_IS_SPOT_INSTANCE": types.Boolean(),
        "CLOUD_ARCHITECTURE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_REGION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_IMAGE_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_AMI_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_PUBLIC_HOSTNAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_PUBLIC_IPV4": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_ACCOUNT_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CLOUD_PROVIDER_TAGS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ASSET_RISK_SCORE": types.Integer(),
        "TRURISK_SCORE": types.Integer(),
        "TRURISK_SCORE_FACTORS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ASSET_CRITICALITY_SCORE": types.Integer(),
    }

    # Remove METADATA and DNS_DATA from the dataclass. They're parsed out already from dataclass initialization.
    df = DataFrame([prepare_dataclass(host) for host in hosts])

    df.drop(columns=["METADATA", "DNS_DATA", "DETECTION_LIST"], inplace=True)

    # Upload the data, with table depdening on if it is a Host List Detail pull or not:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_ips(
    ips: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_ips",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_ip_list() to SQL.

    Args:
        ips (BaseList): The IP List to upload from vmdr.get_ip_list().
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "IP": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "TYPE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([str(ip) for ip in ips], columns=["IP"])

    # Add the TYPE column, which shows if it is a single IP or a range:
    df["TYPE"] = df["IP"].apply(lambda x: "Single IP" if "/" not in x else "IP Range")

    # Upload the data:
    return upload_data(
        df, table_name, cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_vmdr_hld(
    hld: BaseList,
    cnxn: Connection,
    vulns_table_name: str = "vmdr_hld_detections",
    hosts_table_name: str = "vmdr_hld_hosts_list",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_hld() to SQL.

    Args:
        hld (BaseList): The Host List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        vulns_table_name (str): The name of the table to upload the detections to. Defaults to 'vmdr_hld_detections'.
        hosts_table_name (str): The name of the table to upload the hosts to. Defaults to 'vmdr_hld_hosts_list'.

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
    # so we can use it here to upload the hosts.
    hosts_uploaded = upload_vmdr_hosts(
        hld, cnxn, hosts_table_name, override_import_dt=override_import_dt
    )
    print(
        f"Uploaded {hosts_uploaded} hosts to {hosts_table_name}. Moving to detections..."
    )

    COLS = {
        "UNIQUE_VULN_ID": types.BigInteger(),
        "QID": types.BigInteger(),
        "TYPE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "SEVERITY": types.Integer(),
        "STATUS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "SSL": types.Boolean(),
        "RESULTS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "FIRST_FOUND_DATETIME": types.DateTime(),
        "LAST_FOUND_DATETIME": types.DateTime(),
        "QDS": types.Integer(),
        "QDS_FACTORS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TIMES_FOUND": types.Integer(),
        "LAST_TEST_DATETIME": types.DateTime(),
        "LAST_UPDATE_DATETIME": types.DateTime(),
        "IS_IGNORED": types.Boolean(),
        "IS_DISABLED": types.Boolean(),
        "LAST_PROCESSED_DATETIME": types.DateTime(),
        "LAST_FIXED_DATETIME": types.DateTime(),
        "PORT": types.Integer(),
        "PROTOCOL": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "FQDN": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Create a copy of the detections list so we do not modify the original:
    detections = BaseList(detections)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(detection) for detection in detections])

    # Set QDS to an integer:
    df["QDS"] = df["QDS"].apply(lambda x: int(x) if x else None)

    # Upload the data:
    return upload_data(
        df,
        vulns_table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_scanners(
    scanners: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_scanners",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_scanner_list() to SQL.

    Args:
        scanners (BaseList): The Scanner List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_scanners'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "NAME": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "SOFTWARE_VERSION": types.Float(),
        "RUNNING_SCAN_COUNT": types.Integer(),
        "STATUS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "UUID": types.Uuid(),
        "RUNNING_SLICES_COUNT": types.Integer(),
        "MODEL_NUMBER": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TYPE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "SERIAL_NUMBER": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ACTIVATION_CODE": types.BigInteger(),
        "INTERFACE_SETTINGS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PROXY_SETTINGS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict.
        "IS_CLOUD_DEPLOYED": types.Boolean(),
        "CLOUD_INFO": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict. DROP THIS! INFO IS IN BELOW FIELDS:
        "PLATFORM_PROVIDER": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "AMI_ID": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "ACCOUNT_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_REGION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_AVAIBILITY_ZONE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_ZONE_TYPE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_VPC_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_SUBNET_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_ADDRESS_PRIVATE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "INSTANCE_ADDRESS_PUBLIC": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "HOSTNAME_PRIVATE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "SECURITY_GROUPS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "API_PROXY_SETTINGS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "VLANS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict.
        "STATIC_ROUTES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict.
        "ML_LATEST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ML_VERSION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "VULNSIGS_LATEST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "VULNSIGS_VERSION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ASSET_GROUP_COUNT": types.Integer(),
        "ASSET_GROUP_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "LAST_UPDATED_DATE": types.DateTime(),
        "POLLING_INTERVAL": types.Integer(),
        "USER_LOGIN": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "HEARTBEATS_MISSED": types.Integer(),
        "SS_CONNECTIION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "SS_LAST_CONNECTED": types.DateTime(),
        "USER_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
        "UPDATED": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "COMMENTS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "MAX_CAPACITY_UNITS": types.Float(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(scanner) for scanner in scanners])

    # Drop the CLOUD_INFO and EC2_INFO columns:
    df.drop(columns=["CLOUD_INFO"], inplace=True)

    # Upload the data:
    return upload_data(
        df, table_name, cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_vmdr_static_search_lists(
    searchlists: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_static_searchlists",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_static_searchlists() to SQL.

    Args:
        searchlists (BaseList): The Search List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "GLOBAL": types.Boolean(),
        "OWNER": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "CREATED": types.DateTime(),
        "MODIFIED": types.DateTime(),
        "MODIFIED_BY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "QIDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "OPTION_PROFILES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
        "REPORT_TEMPLATES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
        "REMEDIATION_POLICIES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
        "DISTRIBUTION_GROUPS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
        "COMMENTS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(searchlist) for searchlist in searchlists])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_dynamic_search_lists(
    searchlists: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_dynamic_searchlists",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_dynamic_searchlists() to SQL.

    Args:
        searchlists (BaseList): The Search List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_dynamic_searchlists'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "GLOBAL": types.Boolean(),
        "OWNER": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "CREATED": types.DateTime(),
        "MODIFIED": types.DateTime(),
        "MODIFIED_BY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "QIDS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "CRITERIA": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "OPTION_PROFILES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "REPORT_TEMPLATES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "REMEDIATION_POLICIES": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "DISTRIBUTION_GROUPS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "COMMENTS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(searchlist) for searchlist in searchlists])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_users(
    users: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_users",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_user_list() to SQL.

    Args:
        users (BaseList): The user list to upload.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "USER_LOGIN": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "USER_ID": types.Integer(),
        "EXTERNAL_ID": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "FIRSTNAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LASTNAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "PHONE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "FAX": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "EMAIL": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "COMPANY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ADDRESS1": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ADDRESS2": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CITY": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "COUNTRY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "STATE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "ZIP_CODE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TIME_ZONE_CODE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "USER_STATUS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CREATION_DATE": types.DateTime(),
        "USER_ROLE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "BUSINESS_UNIT": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "MANAGER_POC": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "UI_INTERFACE_STYLE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CREATE_OPTION_PROFILES": types.Boolean(),
        "PURGE_INFO": types.Boolean(),
        "ADD_ASSETS": types.Boolean(),
        "EDIT_REMEDIATION_POLICY": types.Boolean(),
        "EDIT_AUTH_RECORDS": types.Boolean(),
        "LATEST_VULN": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DAILY_TICKETS": types.Boolean(),
        "ASSET_GROUP_TITLE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "LAST_LOGIN_DATE": types.DateTime(),
        "UNIT_MANAGER_POC": types.Float(),
        "MAP": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "SCAN": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(user) for user in users])

    # Drop contact_info, assigned_asset_groups,
    # permissions, notifications:
    df.drop(
        columns=[
            "CONTACT_INFO",
            "ASSIGNED_ASSET_GROUPS",
            "PERMISSIONS",
            "NOTIFICATIONS",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_scan_list(
    scans: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_scans",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_scan_list() to SQL.

    Args:
        scans (BaseList): The Scan List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_scans'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "REF": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "TYPE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "USER_LOGIN": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LAUNCH_DATETIME": types.DateTime(),
        "DURATION": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PROCESSING_PRIORITY": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PROCESSED": types.Boolean(),
        "STATE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "TARGET": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "OPTION_PROFILE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
        "ASSET_GROUP_TITLE_LIST": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(scan) for scan in scans])

    # Drop the STATUS column, as it is parsed out into STATE:
    df.drop(columns=["STATUS"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_report_list(
    reports: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_reports",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_report_list() to SQL.

    Args:
        reports (BaseList): The Report List of VMDRReports to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "TYPE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "USER_LOGIN": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LAUNCH_DATETIME": types.DateTime(),
        "OUTPUT_FORMAT": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "SIZE": types.Float(),
        "STATUS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "EXPIRATION_DATETIME": types.DateTime(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(report) for report in reports])

    # Drop the STATUS column, as it is parsed out into STATE:
    df.drop(columns=["STATUS"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_scheduled_report_list(
    reports: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_scheduled_reports",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_scheduled_report_list() to SQL.

    Args:
        reports (BaseList): The Report List of VMDRScheduledReports to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_scheduled_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "OUTPUT_FORMAT": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TEMPLATE_TITLE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ACTIVE": types.Boolean(),
        "SCHEDULE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # dict
        "START_DATE_UTC": types.DateTime(),
        "START_HOUR": types.Integer(),
        "START_MINUTE": types.Integer(),
        "TIME_ZONE_CODE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TIME_ZONE_DETAILS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "DST_SELECTED": types.Boolean(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(report) for report in reports])

    # Drop TIME_ZONE column, as it is parsed out into TIME_ZONE_CODE and TIME_ZONE_DETAILS:
    df.drop(columns=["TIME_ZONE"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_template_list(
    templates: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_templates",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_template_list() to SQL.

    Args:
        templates (BaseList): The Report List of VMDRTemplates to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_templates'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "ID": types.Integer(),
        "TYPE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "TEMPLATE_TYPE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TITLE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "LOGIN": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "FIRSTNAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LASTNAME": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "LAST_UPDATE": types.DateTime(),
        "GLOBAL": types.Boolean(),
    }

    def prepare_template(template) -> dict:
        """
        Helper function to use instead of prepare_dataclass
        to handle the USER attribute.

        df.drop is not necessary due to del data['USER'] here.

        Args:
            template (ReportTemplate): The template to prepare.

        Returns:
            dict: The template prepared for upload.
        """
        data = template.to_dict()
        data["LOGIN"] = template.USER.get("LOGIN")
        data["FIRSTNAME"] = template.USER.get("FIRSTNAME")
        data["LASTNAME"] = template.USER.get("LASTNAME")
        del data["USER"]

        return data

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_template(template) for template in templates])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_kb_qvs(
    qvs: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_kb_qvs",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_kb_qvs() to SQL.

    Args:
        qvs (BaseList): The KBQVS List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_kb_qvs'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "idType": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "qvs": types.Integer(),
        "qvsLastChangedDate": types.DateTime(),
        "nvdPublishedDate": types.DateTime(),
        "cvss": types.Float(),
        "cvssVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cvssString": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "epss": types.Float(),
        "threatActors": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "exploitMaturity": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "trending": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "mitigationControls": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "malwareName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "malwareHash": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "rti": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    df = DataFrame([prepare_dataclass(qv) for qv in qvs])

    df.drop(columns=["contributingFactors", "base"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_activity_log(
    activity_log: BaseList,
    cnxn: Connection,
    table_name: str = "vmdr_activity_log",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_activity_log() to SQL.

    Args:
        activity_log (BaseList): The Activity Log to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_activity_log'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "Date": types.DateTime(),
        "Action": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "Module": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "Details": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "User_Name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "User_Role": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "User_IP": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(log) for log in activity_log])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_vmdr_cve_hld(
    hld: BaseList,
    cnxn: Connection,
    vulns_table_name: str = "vmdr_cve_hld_detections",
    hosts_table_name: str = "vmdr_cve_hld_host_list",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from vmdr.get_cve_hld() to SQL.

    Args:
        hld (BaseList): The Host List to upload.
        cnxn (Connection): The Connection object to the SQL database.
        vulns_table_name (str): The name of the table to upload the detections to. Defaults to 'vmdr_cve_hld_detections'.
        hosts_table_name (str): The name of the table to upload the hosts to. Defaults to 'vmdr_cve_hld_host_list'.

    Returns:
        int: The number of rows uploaded.

    """

    """
    Get_cve_hld and get_host_list technically return the same data. get_cve_hld just
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
    # so we can use it here to upload the hosts.
    hosts_uploaded = upload_vmdr_hosts(
        hld, cnxn, hosts_table_name, override_import_dt=override_import_dt
    )
    print(
        f"Uploaded {hosts_uploaded} hosts to {hosts_table_name}. Moving to detections..."
    )

    COLS = {
        "UNIQUE_VULN_ID": types.BigInteger(),
        "VULN_CVE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ASSOCIATED_QID": types.BigInteger(),
        "QID_TITLE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "TYPE": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "SSL": types.Boolean(),
        "RESULTS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "STATUS": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "FQDN": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "CVSS": types.Float(),
        "CVSS_BASE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_TEMPORAL": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_31": types.Float(),
        "CVSS_31_BASE": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "CVSS_31_TEMPORAL": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "QVS": types.Integer(),
        "PORT": types.Integer(),
        "PROTOCOL": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "FIRST_FOUND_DATETIME": types.DateTime(),
        "LAST_FOUND_DATETIME": types.DateTime(),
        "TIMES_FOUND": types.Integer(),
        "LAST_TEST_DATETIME": types.DateTime(),
        "LAST_UPDATE_DATETIME": types.DateTime(),
        "LAST_PROCESSED_DATETIME": types.DateTime(),
        "LAST_FIXED_DATETIME": types.DateTime(),
        "ID": types.Integer(),
        "IS_IGNORED": types.Boolean(),
        "IS_DISABLED": types.Boolean(),
    }

    # Create a copy of the detections list so we do not modify the original:
    detections = BaseList(detections)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(detection) for detection in detections])

    # Upload the data:
    return upload_data(
        df,
        vulns_table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )
