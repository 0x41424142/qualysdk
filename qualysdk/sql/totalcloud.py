"""
totalcloud.py - Contains the functions to upload supported GAV API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_aws_totalcloud_connectors(
    connectors: BaseList,
    cnxn: Connection,
    table_name: str = "totalcloud_aws_connectors",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload data from totalcloud.get_connectors() to SQL.

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
        "awsAccountId": types.Integer(),
        "accountAlias": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isDisabled": types.Boolean(),
        "pollingFrequency": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "error": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "baseAccountId": types.Integer(),
        "externalId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "arn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "portalConnectorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isPortalConnector": types.Boolean(),
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
