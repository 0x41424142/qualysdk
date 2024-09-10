"""
totalcloud.py - Contains the functions to upload supported GAV API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


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
