"""
supported_uploads.py - Contains the functions to upload supported API pulls to SQL Server.
"""

from pandas import DataFrame
from sqlalchemy import Connection, types

from .base import upload_data, prepare_dataclass
from ..vmdr.data_classes.lists import BaseList


def upload_vmdr_ags(ags: BaseList, cnxn: Connection) -> int:
    """
    Upload data from vmdr.get_ag_list() to SQL.

    Parameters:
    ags (BaseList): The Asset Group List to upload.
    cnxn (Connection): The Connection object to the SQL database.

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
    return upload_data(df, "AssetGroups", cnxn, dtype=COLS)


def upload_vmdr_kb(kbs: BaseList, cnxn: Connection) -> int:
    """
    Upload data from vmdr.query_kb() to SQL.

    Parameters:
    kbs (BaseList): The KB List to upload.
    cnxn (Connection): The Connection object to the SQL database.

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
    return upload_data(df, "knowledgebase", cnxn, dtype=COLS)


def upload_vmdr_hosts(hosts: BaseList, cnxn: Connection) -> int:
    """
    Upload data from vmdr.get_host_list() to SQL.

    Parameters:
        hosts (BaseList): The Host List to upload.
        cnxn (Connection): The Connection object to the SQL database.

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
        "CLOUD_ACCOUNT_ID": types.BigInteger(),
        "CLOUD_PROVIDER_TAGS": types.String(),
        "ASSET_RISK_SCORE": types.Integer(),
        "TRURISK_SCORE": types.Integer(),
        "TRURISK_SCORE_FACTORS": types.String(),
        "ASSET_CRITICALITY_SCORE": types.Integer(),
    }

    # Remove METADATA and DNS_DATA from the dataclass. They're parsed out already from dataclass initialization.
    df = DataFrame([prepare_dataclass(host) for host in hosts])

    df.drop(columns=["METADATA", "DNS_DATA", "DETECTION_LIST"], inplace=True)

    # Upload the data:
    return upload_data(df, "vmdr_hosts_list", cnxn, dtype=COLS)

def upload_vmdr_ips(ips: BaseList, cnxn: Connection) -> int:
    """
    Upload data from vmdr.get_ip_list() to SQL.
    
    Parameters:
        ips (BaseList): The IP List to upload from vmdr.get_ip_list().
        cnxn (Connection): The Connection object to the SQL database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "IP_OBJ": types.String(),
        "TYPE": types.String(),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(ip) for ip in ips], columns=["IP"])

    # Add the TYPE column, which shows if it is a single IP or a range:
    df["TYPE"] = df["IP"].apply(lambda x: "Single IP" if "/" not in str(x) else "IP Range")

    # Upload the data:
    return upload_data(df, "vmdr_ips", cnxn, dtype=COLS)