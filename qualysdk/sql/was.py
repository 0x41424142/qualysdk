"""
Contains the functions to upload supported Container Security API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_was_webapps(
    webapps: BaseList,
    cnxn: Connection,
    table_name: str = "was_webapps",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```was.get_webapps```
    or ```was.get_webapps_verbose```
    to a SQL database.

    Args:
        webapps (BaseList): A BaseList of WebApp objects.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.Integer(),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "url": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "uris": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "riskScore": types.Integer(),
        "os": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "owner_id": types.Integer(),
        "owner_username": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "owner_firstName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "owner_lastName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scope": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "attributes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultProfile_id": types.Integer(),
        "defaultProfile_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultScanner_id": types.Integer(),
        "defaultScanner_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "defaultScannerTags_count": types.Integer(),
        "defaultScannerTags_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scannerLocked": types.Boolean(),
        "progressiveScanning": types.Boolean(),
        "urlExcludelist": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "urlAllowlist": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "postDataExcludelist": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "logoutRegexList": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "authRecords": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dnsOverrides": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "useRobots": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "useSitemap": types.Boolean(),
        "malwareMonitoring": types.Boolean(),
        "malwareNotifications": types.Boolean(),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "comments": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isScheduled": types.Boolean(),
        "lastScan_id": types.Integer(),
        "lastScan_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "lastScan_summary_resultsStatus": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "lastScan_summary_authStatus": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdBy_id": types.Integer(),
        "createdBy_username": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdBy_firstName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdBy_lastName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdDate": types.DateTime(),
        "updatedDate": types.DateTime(),
        "updatedBy_id": types.Integer(),
        "updatedBy_username": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "updatedBy_firstName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "updatedBy_lastName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "screenshot": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "config": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "crawlingScripts": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "postmanCollection": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "headers": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "domains": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subDomain": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "swaggerFile": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "redundancyLinks": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "maxRedundancyLinks": types.Integer(),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(webapp) for webapp in webapps])

    # Drop any columns that we parsed out:
    df.drop(
        columns=[
            "owner",
            "defaultProfile",
            "defaultScanner",
            "defaultScannerTags",
            "lastScan",
            "createdBy",
            "updatedBy",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
