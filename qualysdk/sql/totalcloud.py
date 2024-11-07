"""
totalcloud.py - Contains the functions to upload supported GAV API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList

BASE_AWS_FIELDS = {
    "resourceId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    "connectorUuids": types.String().with_variant(
        TEXT(charset="utf8"), "mysql", "mariadb"
    ),  # BaseList
    "created": types.DateTime(),
    "cloudAccountId": types.BigInteger(),
    "additionalDetails": types.String().with_variant(
        TEXT(charset="utf8"), "mysql", "mariadb"
    ),
    "uuid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    "connectorUuid": types.String().with_variant(
        TEXT(charset="utf8"), "mysql", "mariadb"
    ),
    "createdOn": types.DateTime(),
    "tags": types.String().with_variant(
        TEXT(charset="utf8"), "mysql", "mariadb"
    ),  # BaseList
    "remediationEnabled": types.Boolean(),
    "lastUpdated": types.DateTime(),
    "cloudType": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    "region": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    "resourceType": types.String().with_variant(
        TEXT(charset="utf8"), "mysql", "mariadb"
    ),
    "accountAlias": types.String().with_variant(
        TEXT(charset="utf8"), "mysql", "mariadb"
    ),
    "controlsFailed": types.Integer(),
    "qualysTags": types.String().with_variant(
        TEXT(charset="utf8"), "mysql", "mariadb"
    ),  # BaseList
}


def upload_totalcloud_aws_connectors(
    connectors: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_connectors",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_connectors(provider='aws') to SQL.

    Args:
        connectors (BaseList): The BaseList of Connectors to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "provider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "totalAssets": types.Integer(),
        "lastSyncedOn": types.DateTime(),
        "nextSyncedOn": types.DateTime(),
        "remediationEnabled": types.Boolean(),
        "qualysTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isGovCloud": types.Boolean(),
        "isChinaRegion": types.Boolean(),
        "awsAccountId": types.BigInteger(),
        "accountAlias": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isDisabled": types.Boolean(),
        "pollingFrequency": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "error": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "baseAccountId": types.BigInteger(),
        "externalId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "portalConnectorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isPortalConnector": types.Boolean(),
        "groups": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(connector) for connector in connectors])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_azure_connectors(
    connectors: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_azure_connectors",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_connectors(provider='azure') to SQL.

    Args:
        connectors (BaseList): The BaseList of Connectors to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "provider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "totalAssets": types.Integer(),
        "lastSyncedOn": types.DateTime(),
        "nextSyncedOn": types.DateTime(),
        "remediationEnabled": types.Boolean(),
        "qualysTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isGovCloud": types.Boolean(),
        "isChinaRegion": types.Boolean(),
        "accountAlias": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isDisabled": types.Boolean(),
        "pollingFrequency": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "error": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "externalId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "portalConnectorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isPortalConnector": types.Boolean(),
        "subscriptionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "tenantId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "applicationId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subscriptionName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "directoryId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "groups": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(connector) for connector in connectors])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_gcp_connectors(
    connectors: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_gcp_connectors",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_connectors(provider='gcp') to SQL.

    Args:
        connectors (BaseList): The BaseList of Connectors to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "provider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "totalAssets": types.Integer(),
        "lastSyncedOn": types.DateTime(),
        "nextSyncedOn": types.DateTime(),
        "remediationEnabled": types.Boolean(),
        "qualysTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isGovCloud": types.Boolean(),
        "isChinaRegion": types.Boolean(),
        "accountAlias": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isDisabled": types.Boolean(),
        "pollingFrequency": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "error": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "externalId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "portalConnectorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isPortalConnector": types.Boolean(),
        "groups": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "projectId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(connector) for connector in connectors])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_control_metadata(
    controls: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_control_metadata",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_metadata() to SQL.

    Args:
        controls (BaseList): The BaseList of Controls to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "cid": types.BigInteger(),
        "controlName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "created": types.DateTime(),
        "modified": types.DateTime(),
        "controlType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "provider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isCustomizable": types.Boolean(),
        "serviceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "criticality": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "evaluation_description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "evaluation_passMessage": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "evaluation_failMessage": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "evaluation_criteria": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "specification": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rationale": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "manualRemediation": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "references": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "buildTimeRemediation": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "resourceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "remediationEnabled": types.Boolean(),
        "policyNames": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "executionType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "workflowBased": types.Boolean(),
        "templateType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(control) for control in controls])

    # Drop the evaluation column:
    df.drop(columns=["evaluation"], inplace=True)

    # Upload the data:

    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_ec2(
    ec2s: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_ec2_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='VM') to SQL.

    Args:
        ec2s (BaseList): The BaseList of EC2s to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "subnetId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "arsScore": types.Integer(),
        "availabilityZone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "instanceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "instanceState": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "networkInterfaceAddresses": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "vulnerabilityStats_severity_1": types.Integer(),
        "vulnerabilityStats_severity_2": types.Integer(),
        "vulnerabilityStats_severity_3": types.Integer(),
        "vulnerabilityStats_severity_4": types.Integer(),
        "vulnerabilityStats_severity_5": types.Integer(),
        "vulnerabilityStats_typeDetected_Confirmed": types.Integer(),
        "vulnerabilityStats_typeDetected_Potential": types.Integer(),
        "vulnerabilityStats_typeDetected_Informational": types.Integer(),
        "vulnerabilityStats_typeDetected_totalVulnerability": types.Integer(),
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "events": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "iamInstanceProfileRoleDetails_profileName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "iamInstanceProfileRoleDetails_profileArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "iamInstanceProfileRoleDetails_roleArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "iamInstanceProfileRoleDetails_roleName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "imageId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "publicIpAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "instanceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ipAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "publicDnsName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "instanceStatus": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "iamInstanceProfile_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "iamInstanceProfile_id": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "iamInstanceProfile_arn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "privateIpAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "launchTime": types.DateTime(),
        "classifications": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "spotInstanceRequestId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "elasticIpAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "secondaryPrivateIpAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "securityGroups": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "privateDnsName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "criticalityScore": types.Integer(),
        "vulnerabilities": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(ec2) for ec2 in ec2s])

    # Drop vulnerabilityStats, iamInstanceProfileRoleDetails, iamInstanceProfile columns:
    df.drop(
        columns=[
            "vulnerabilityStats",
            "iamInstanceProfileRoleDetails",
            "iamInstanceProfile",
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


def upload_totalcloud_aws_s3(
    buckets: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_s3_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='S3') to SQL.

    Args:
        buckets (BaseList): The BaseList of S3 Buckets to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "bucketName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "bucketCreationDateStr": types.DateTime(),
        "s3GrantList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "ownerName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "bucketPolicy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "bucketOwnerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(bucket) for bucket in buckets])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_acl(
    acls: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_acl_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='acl') to SQL.

    Args:
        acls (BaseList): The BaseList of ACLs to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "associations": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "ipPermissionEgressList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "ipPermissionList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "isDefault": types.Boolean(),
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "networkAclId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(acl) for acl in acls])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_rds(
    rds: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_rds_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='rds') to SQL.

    Args:
        rds (BaseList): The BaseList of RDSs to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "subnetId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subnetGroup_dbSubnetGroupStatus": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subnetGroup_dbSubnetGroupName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subnetGroup_dbSubnetVpcId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subnetGroup_subnetList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "subnetGroup_dbsubnetGroupArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dbName": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "availabilityZone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "securityGroupId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dbClusterIdentifier": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "caCertificateIdentifier": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "engineVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "masterUsername": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dbInstanceIdentifier": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dbSecurityGroupList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "backupRetentionPeriod": types.Integer(),
        "kmsKeyId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "latestRestorableTime": types.DateTime(),
        "dbInstancePort": types.Integer(),
        "enhancedMonitoringEnabled": types.Boolean(),
        "dbiResourceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "preferredBackupWindow": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "endpoint_hostedZoneId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "endpoint_address": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "endpoint_port": types.Integer(),
        "engine": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "publiclyAccessible": types.Boolean(),
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "instanceCreatedTime": types.DateTime(),
        "multiAZ": types.Boolean(),
        "instanceClass": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "encrypted": types.Boolean(),
        "iamDatabaseAuthenticationEnabled": types.Boolean(),
        "licenseModel": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "preferredMaintenanceWindow": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "storageType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(rd) for rd in rds])

    # Drop the subnetGroup, endpoint columns:
    df.drop(columns=["subnetGroup", "endpoint"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_iamuser(
    iam_users: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_iamuser_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='iamuser') to SQL.

    Args:
        iam_users (BaseList): The BaseList of IAM Users to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "userPolicies": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "userAttachedPolicies": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "userDto_accessKey1Active": types.Boolean(),
        "userDto_accessKey2Active": types.Boolean(),
        "userDto_cert1LastRotated": types.DateTime(),
        "userDto_cert2LastRotated": types.DateTime(),
        "userDto_cert1Active": types.Boolean(),
        "userDto_cert2Active": types.Boolean(),
        "userDto_accessKey1LastRotated": types.DateTime(),
        "userDto_accessKey2LastRotated": types.DateTime(),
        "userDto_accesKey1LastUsedService": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userDto_accessKey2LastUsedService": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userDto_path": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userDto_accessKeys": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "userDto_passwordLastUsed": types.DateTime(),
        "userDto_passwordNextRotation": types.DateTime(),
        "userDto_accessKey1LastUsedRegion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userDto_accessKey2LastUsedRegion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userDto_arn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userDto_userCreationTime": types.DateTime(),
        "userDto_mfaActive": types.Boolean(),
        "userDto_passwordEnabled": types.Boolean(),
        "userDto_accessKey1LastUsed": types.DateTime(),
        "userDto_accessKey2LastUsed": types.DateTime(),
        "userDto_userId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userDto_createdDate": types.DateTime(),
        "userDto_passwordLastChanged": types.DateTime(),
        "userDto_username": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "userGroups": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "classifications": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "userInlinePolicies": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "user": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(iam_user) for iam_user in iam_users])

    # Drop the userDto column:
    df.drop(columns=["userDto"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_vpc(
    vpcs: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_vpc_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='vpc') to SQL.

    Args:
        vpcs (BaseList): The BaseList of VPCs to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "instanceTenancy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cidrBlock": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isDefault": types.Boolean(),
        "ipv6CidrBlockAssociationSet": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(vpc) for vpc in vpcs])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_securitygroup(
    security_groups: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_securitygroup_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='sg') to SQL.

    Args:
        security_groups (BaseList): The BaseList of Security Groups to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "groupId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vulnerable": types.Boolean(),
        "ipPermissionList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "ipPermissionEgressList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "groupName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [prepare_dataclass(security_group) for security_group in security_groups]
    )

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_lambda(
    lambdas: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_lambda_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='lambda') to SQL.

    Args:
        lambdas (BaseList): The BaseList of Lambdas to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "functionName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "associations": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "handler": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rawFunctionPolicy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "masterArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "aliases": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "assumeRolePolicyDocument": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "kmsKeyArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "tracingConfig": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "inlinePolicies": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "codeSize": types.Integer(),
        "timeout": types.Integer(),
        "codeSha256": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "roleArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "layers": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "functionArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "functionVersions": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "runtime": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "functionUrlConfigs": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "revisionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "classifications": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "managedPolicies": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "memorySize": types.Integer(),
        "eventSourceMappings": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "roleName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "lastModified": types.DateTime(),
        "version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(lambda_) for lambda_ in lambdas])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_subnet(
    subnets: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_subnet_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='subnet') to SQL.

    Args:
        subnets (BaseList): The BaseList of Subnets to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "subnetId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "availabilityZone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "assignIpv6AddressOnCreation": types.Boolean(),
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "ipv6CidrBlockAssociationSet": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "cidrBlock": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "availableIpAddressCount": types.Integer(),
        "mapPublicIpOnLaunch": types.Boolean(),
        "defaultForAz": types.Boolean(),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(subnet) for subnet in subnets])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_internetgateway(
    internet_gateways: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_internetgateway_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='internetgateway') to SQL.

    Args:
        internet_gateways (BaseList): The BaseList of Internet Gateways to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "internetGatewayId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "attachments": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [prepare_dataclass(internet_gateway) for internet_gateway in internet_gateways]
    )

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_loadbalancer(
    load_balancers: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_loadbalancer_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='loadbalancer') to SQL.

    Args:
        load_balancers (BaseList): The BaseList of Load Balancers to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "loadBalancerName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "loadBalancerArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scheme": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "instances": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "subnetAvailabilityZonePair": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "dnsName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "availabilityZones": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "createdTime": types.DateTime(),
        "subnets": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "listeners": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "ipAddressType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "securityGroups": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [prepare_dataclass(load_balancer) for load_balancer in load_balancers]
    )

    # Change the _type column to type:
    df.rename(columns={"_type": "type"}, inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_routetable(
    route_tables: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_routetable_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='routetable') to SQL.

    Args:
        route_tables (BaseList): The BaseList of Route Tables to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "routeTableId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "routes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "routeDtos": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "associations": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(route_table) for route_table in route_tables])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_ebsvolume(
    ebs_volumes: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_ebsvolume_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='ebsvolume') to SQL.

    Args:
        ebs_volumes (BaseList): The BaseList of EBS Volumes to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "volumeId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "volumeType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "availabilityZone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "encrypted": types.Boolean(),
        "snapshotId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "createTime": types.DateTime(),
        "size": types.Integer(),
        "iops": types.Integer(),
        "kmsKeyId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "attachments": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(ebs_volume) for ebs_volume in ebs_volumes])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_autoscalinggroup(
    asgs: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_autoscalinggroup_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='auto scaling group') to SQL.

    Args:
        asgs (BaseList): The BaseList of Auto Scaling Groups to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "autoScalingGroupName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "autoScalingGroupARN": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "healthCheckType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "instances": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "availabilityZones": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "launchConfigurationName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdTime": types.DateTime(),
        "loadBalancerNames": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(asg) for asg in asgs])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_ekscluster(
    eks_clusters: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_ekscluster_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='eks cluster') to SQL.

    Args:
        eks_clusters (BaseList): The BaseList of EKS Clusters to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "associations_resourcesVpcConfig_clusterSecurityGroupId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "associations_resourcesVpcConfig_securityGroupIds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "associations_resourcesVpcConfig_vpcId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "associations_resourcesVpcConfig_subnetIds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "version": types.Float(),
        "endpoint": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "resoucesVpcConfig_endpointPrivateAccess": types.Boolean(),
        "resoucesVpcConfig_endpointPublicAccess": types.Boolean(),
        "roleArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "identity_oidc_issuer": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "platformVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "roleName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "logging_clusterLogging": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(eks_cluster) for eks_cluster in eks_clusters])

    # Drop the associations, resoucesVpcConfig, identity, logging columns:
    df.drop(
        columns=["associations", "resoucesVpcConfig", "identity", "logging"],
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


def upload_totalcloud_aws_eksnodegroup(
    eks_nodegroups: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_eksnodegroup_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='eks nodegroup') to SQL.

    Args:
        eks_nodegroups (BaseList): The BaseList of EKS Node Groups to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "associations_clusterArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "associations_clusterName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "associations_subnets": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "associations_resources_autoScalingGroups": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "nodeRoleName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scalingConfig_maxSize": types.Integer(),
        "scalingConfig_desiredSize": types.Integer(),
        "scalingConfig_minSize": types.Integer(),
        "capacityType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "instanceTypes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "releaseVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "version": types.Float(),
        "labels": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "diskSize": types.Integer(),
        "nodeRole": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "launchTemplate_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "launchTemplate_id": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "launchTemplate_version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "amiType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "health": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [prepare_dataclass(eks_nodegroup) for eks_nodegroup in eks_nodegroups]
    )

    # Drop the associations, scalingConfig, launchTemplate columns:
    df.drop(columns=["associations", "scalingConfig", "launchTemplate"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_fargateprofile(
    fargate_profiles: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_fargateprofile_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='eks fargate profile') to SQL.

    Args:
        fargate_profiles (BaseList): The BaseList of Fargate Profiles to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "associations_clusterArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "associations_clusterName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "associations_subnets": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "podExecutionRoleArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "selectors": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "podExecutionRoleName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [prepare_dataclass(fargate_profile) for fargate_profile in fargate_profiles]
    )

    # Drop the associations column:
    df.drop(columns=["associations"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_vpcendpoint(
    vpc_endpoints: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_vpcendpoint_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='vpc endpoint') to SQL.

    Args:
        vpc_endpoints (BaseList): The BaseList of VPC Endpoints to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "policyDocument": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dnsOption": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "serviceName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "securityGroupSet": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "privateDnsEnabled": types.Boolean(),
        "requesterManaged": types.Boolean(),
        "ipAddressType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "routeTableIds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "vpcEndpointType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vpcId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "dnsEntrySets": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "networkInterfaceIds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "subnetIds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(vpc_endpoint) for vpc_endpoint in vpc_endpoints])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_vpcendpointservice(
    vpc_endpoint_services: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_vpcendpointservice_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='vpc endpoint service') to SQL.

    Args:
        vpc_endpoint_services (BaseList): The BaseList of VPC Endpoint Services to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "owner": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "acceptanceRequired": types.Boolean(),
        "managesVpcEndpoints": types.Boolean(),
        "availabilityZone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "baseEndpointDnsName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "supportedIpAddressType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "serviceTypes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "privateDnsName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "privateDnsNameVerificationState": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vpcEndpointPolicySupported": types.Boolean(),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [
            prepare_dataclass(vpc_endpoint_service)
            for vpc_endpoint_service in vpc_endpoint_services
        ]
    )

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_iamgroup(
    iam_groups: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_iamgroup_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='iam group') to SQL.

    Args:
        iam_groups (BaseList): The BaseList of IAM Groups to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "classifications": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "groupId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "GroupPolicyList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "AttachedManagedPolicies": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(iam_group) for iam_group in iam_groups])

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_iampolicy(
    iam_policies: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_iampolicy_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='iam policy') to SQL.

    Args:
        iam_policies (BaseList): The BaseList of IAM Policies to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "IsAttachable": types.Boolean(),
        "PermissionsBoundaryUsageCount": types.Integer(),
        "AttachmentCount": types.Integer(),
        "DefaultVersionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultPolicyVersion_VersionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultPolicyVersion_IsDefaultVersion": types.Boolean(),
        "defaultPolicyVersion_Document_Version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultPolicyVersion_Document_Statement": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "defaultPolicyVersion_CreateDate": types.DateTime(),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "path": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "classifications": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "policyId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(iam_policy) for iam_policy in iam_policies])

    # Change the _type column to type:
    df.rename(columns={"_type": "type"}, inplace=True)

    # Drop the defaultPolicyVersion column:
    df.drop(columns=["defaultPolicyVersion"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_iamrole(
    iam_roles: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_iamrole_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='iam role') to SQL.

    Args:
        iam_roles (BaseList): The BaseList of IAM Roles to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "AttachedManagedPolicies": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "RoleLastUsed": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "roleId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "PermissionsBoundary_PermissionsBoundaryArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "PermissionsBoundary_PermissionsBoundaryType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "path": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "classifications": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "AssumeRolePolicyDocument_Version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "AssumeRolePolicyDocument_Statement": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "trustedEntities": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "RolePolicyList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "InstanceProfileList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(iam_role) for iam_role in iam_roles])

    # Drop the PermissionsBoundary, AssumeRolePolicyDocument columns:
    df.drop(columns=["PermissionsBoundary", "AssumeRolePolicyDocument"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_sagemakernotebook(
    sagemaker_notebooks: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_sagemakernotebook_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='sagemaker notebook') to SQL.

    Args:
        sagemaker_notebooks (BaseList): The BaseList of SageMaker Notebooks to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "subnetId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "networkInterfaceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "volumeSizeInGB": types.Float(),
        "rootAccess": types.Boolean(),
        "instanceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "platformId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "url": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "directInternetAccess": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "roleArn": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "securityGroups": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "defaultCodeRepository": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "kmsKeyId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [
            prepare_dataclass(sagemaker_notebook)
            for sagemaker_notebook in sagemaker_notebooks
        ]
    )

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_aws_cloudfrontdistribution(
    cloudfront_distributions: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_cloudfrontdistribution_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='aws', resource_type='cloudfront distribution') to SQL.

    Args:
        cloudfront_distributions (BaseList): The BaseList of CloudFront Distributions to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'vmdr_reports'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "defaultCacheBehavior_Compress": types.Boolean(),
        "defaultCacheBehavior_FunctionAssociations_Quantity": types.Integer(),
        "defaultCacheBehavior_FunctionAssociations_Items": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "defaultCacheBehavior_LambdaFunctionAssociations_Quantity": types.Integer(),
        "defaultCacheBehavior_LambdaFunctionAssociations_Items": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "defaultCacheBehavior_TargetOriginId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultCacheBehavior_ViewerProtocolPolicy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultCacheBehavior_TrustedSigners_Enabled": types.Boolean(),
        "defaultCacheBehavior_TrustedSigners_Quantity": types.Integer(),
        "defaultCacheBehavior_FieldLevelEncryptionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultCacheBehavior_DefaultTTL": types.Integer(),
        "defaultCacheBehavior_TrustedKeyGroups_Enabled": types.Boolean(),
        "defaultCacheBehavior_TrustedKeyGroups_Quantity": types.Integer(),
        "defaultCacheBehavior_AllowedMethods_CachedMethods_Quantity": types.Integer(),
        "defaultCacheBehavior_AllowedMethods_CachedMethods_Items": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "defaultCacheBehavior_AllowedMethods_Items_Method": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "defaultCacheBehavior_SmoothStreaming": types.Boolean(),
        "defaultCacheBehavior_MinTTL": types.Integer(),
        "defaultCacheBehavior_MaxTTL": types.Integer(),
        "loggingEnabled": types.Boolean(),
        "isIpv6Enabled": types.Boolean(),
        "includeCookies": types.Boolean(),
        "geoRestriction_RestrictionType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "geoRestriction_Quantity": types.Integer(),
        "enabled": types.Boolean(),
        "webAclId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "minimumProtocolVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "httpVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "priceClass": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "loggingBucket": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "origins": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "comment": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "staging": types.Boolean(),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "loggingBucketPrefix": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "acmCertificateARN": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Add in the base fields:
    COLS.update(BASE_AWS_FIELDS)

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [
            prepare_dataclass(cloudfront_distribution)
            for cloudfront_distribution in cloudfront_distributions
        ]
    )

    # Drop the defaultCacheBehavior, geoRestriction columns:
    df.drop(columns=["defaultCacheBehavior", "geoRestriction"], inplace=True)

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_remediation_activities(
    remediation_activities: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_remediation_activities",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_remediation_activities() to SQL.

    Args:
        remediation_activities (BaseList): The BaseList of Remediation Activities to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'totalcloud_remediation_activities'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "resourceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "controlId": types.Integer(),
        "cloudType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "accountId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "region": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "resourceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "remediationAction": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "policyNames": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "controlName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "triggeredOn": types.DateTime(),
        "Errors": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "triggeredBy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "remediationReason": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [
            prepare_dataclass(remediation_activity)
            for remediation_activity in remediation_activities
        ]
    )

    # Upload the data:
    return upload_data(
        df,
        table_name,
        cnxn,
        dtype=COLS,
        override_import_dt=override_import_dt,
    )


def upload_totalcloud_azure_vm(
    vms: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_azure_vm_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='azure', resource_type='vm') to SQL.

    Args:
        vms (BaseList): The BaseList of VMs to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'totalcloud_azure_vm_inventory'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "arsScore": types.Integer(),
        "vulnerabilityStats": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "computerName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "primaryPrivateIPAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "primaryPublicIPAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "primaryPublicIPAddressId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "statuses": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "criticalityScore": types.Integer(),
        "availabilitySetId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "provisioningState": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "licenseType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "size": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "osType": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "networkSecurityGroupId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "imageData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        # Base fields:
        "resourceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorUuids": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "created": types.DateTime(),
        "subscriptionName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subscriptionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "uuid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "qualysTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "remediationEnabled": types.Boolean(),
        "updated": types.DateTime(),
        "additionalDetails": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "region": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "resourceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "controlsFailed": types.Integer(),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customers": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "resourceGroupName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "_type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(vm) for vm in vms])

    # Upload the data:
    return upload_data(
        df, table_name, cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_totalcloud_azure_webapp(
    webapps: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_azure_webapp_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='azure', resource_type='webapp') to SQL.

    Args:
        webapps (BaseList): The BaseList of WebApps to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'totalcloud_azure_webapp_inventory'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "redundancyMode": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "repositorySiteName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "enabled": types.Boolean(),
        "enabledHosts": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "clientCertEnabled": types.Boolean(),
        "subKinds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "usageState": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isDefaultContainer": types.Boolean(),
        "appServicePlan": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "deploymentId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "httpsonly": types.Boolean(),
        "clientAffinityEnabled": types.Boolean(),
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "key": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "defaultHostName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "availabilityState": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "kind": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        # Base fields:
        "resourceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorUuids": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "created": types.DateTime(),
        "subscriptionName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subscriptionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "uuid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "qualysTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "remediationEnabled": types.Boolean(),
        "updated": types.DateTime(),
        "additionalDetails": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "region": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "resourceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "controlsFailed": types.Integer(),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customers": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "resourceGroupName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "_type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame([prepare_dataclass(webapp) for webapp in webapps])

    # Upload the data:
    return upload_data(
        df, table_name, cnxn, dtype=COLS, override_import_dt=override_import_dt
    )


def upload_totalcloud_azure_storageaccount(
    storageaccounts: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_azure_storageaccount_inventory",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_inventory(provider='azure', resource_type='storage account') to SQL.

    Args:
        storageaccounts (BaseList): The BaseList of StorageAccounts to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to 'totalcloud_azure_storageaccount_inventory'.
        override_import_dt (datetime): Use the passed datetime instead of generating one to upload to the database.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "displayName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "connectorId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "skuTier": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "resourceIdentity_type": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "minimumTlsVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "kind": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "firstDiscoveredOn": types.DateTime(),
        "lastDiscoveredOn": types.DateTime(),
        "skuName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "file_lastEnabledTime": types.DateTime(),
        "file_keyType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "file_enabled": types.Boolean(),
        "blob_lastEnabledTime": types.DateTime(),
        "blob_keyType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "blob_enabled": types.Boolean(),
        "primaryLocation": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "secondaryLocation": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hnsEnabled": types.Boolean(),
        "resourceGroupId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "supportsHttpsTrafficOnly": types.Boolean(),
        "statusOfPrimary": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "statusOfSecondary": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "location": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "networkAcls_bypass": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "networkAcls_defaultAction": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "networkAcls_ipRules": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "networkAcls_virtualNetworkRules": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        # Base fields:
        "resourceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorUuids": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "created": types.DateTime(),
        "subscriptionName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subscriptionId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "uuid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "connectorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "qualysTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "remediationEnabled": types.Boolean(),
        "updated": types.DateTime(),
        "additionalDetails": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cloudType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "region": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "resourceType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "controlsFailed": types.Integer(),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customers": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "resourceGroupName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "_type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # Convert the BaseList to a DataFrame:
    df = DataFrame(
        [prepare_dataclass(storageaccount) for storageaccount in storageaccounts]
    )

    # Drop the columns we parsed out:
    df.drop(columns=["blob", "file", "resourceIdentity", "networkAcls"], inplace=True)

    # Upload the data:
    return upload_data(
        df, table_name, cnxn, dtype=COLS, override_import_dt=override_import_dt
    )
