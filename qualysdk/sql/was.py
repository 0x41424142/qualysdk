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
        table_name (str): The name of the table to upload to.
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


def upload_was_authentication_records(
    authRecords: BaseList,
    cnxn: Connection,
    table_name: str = "was_authentication_records",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```was.get_authentication_records```
    or ```was.get_authentication_records_verbose``` to a SQL database.

    Args:
        authRecords (BaseList): A BaseList of WebAppAuthRecord objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.Integer(),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
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
        "formRecord_type": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "formRecord_sslOnly": types.Boolean(),
        "formRecord_authVault": types.Boolean(),
        "formRecord_seleniumCreds": types.Boolean(),
        "formRecord_fields_count": types.Integer(),
        "formRecord_fields_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "serverRecord_type": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "serverRecord_sslOnly": types.Boolean(),
        "serverRecord_authVault": types.Boolean(),
        "serverRecord_fields_count": types.Integer(),
        "serverRecord_fields_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "oauth2Record_grantType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "oauth2Record_clientId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "oauth2Record_clientSecret": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "oauth2Record_scope": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "oauth2Record_accessTokenUrl": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "oauth2Record_seleniumCreds": types.Boolean(),
        "tags_count": types.Integer(),
        "tags_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "comments_count": types.Integer(),
        "comments_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdDate": types.DateTime(),
        "updatedDate": types.DateTime(),
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
    }

    # REDACT PASSWORDS IN serverRecord_fields_list
    # and formRecord_fields_list:
    REDACT_FIELDS = ["serverRecord_fields_list", "formRecord_fields_list"]
    for field in REDACT_FIELDS:
        for auth in authRecords:
            if getattr(auth, field):
                for record in getattr(auth, field):
                    record.redact_password()

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(record) for record in authRecords])

    # Drop any columns that we parsed out:
    df.drop(
        columns=[
            "owner",
            "formRecord",
            "serverRecord",
            "oauth2Record",
            "tags",
            "comments",
            "createdBy",
            "updatedBy",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_was_findings(
    findings: BaseList,
    cnxn: Connection,
    table_name: str = "was_findings",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```was.get_findings```
    or ```was.get_findings_verbose``` to a SQL database.

    Args:
        findings (BaseList): A BaseList of WebAppFinding objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.Integer(),
        "uniqueId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "qid": types.Integer(),
        "detectionScore": types.Integer(),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "potential": types.Boolean(),
        "findingType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "group": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "severity": types.SmallInteger(),
        "url": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "firstDetectedDate": types.DateTime(),
        "lastDetectedDate": types.DateTime(),
        "lastTestedDate": types.DateTime(),
        "fixedDate": types.DateTime(),
        "timesDetected": types.Integer(),
        "webApp_id": types.Integer(),
        "webApp_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "webApp_url": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isIgnored": types.Boolean(),
        "ignoredReason": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ignoredBy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ignoredDate": types.DateTime(),
        "ignoredComment": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "reactivatedDate": types.DateTime(),
        "reactivateIn": types.Integer(),
        "param": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "cwe_count": types.Integer(),
        "cwe_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "owasp_count": types.Integer(),
        "owasp_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "accessPath_count": types.Integer(),
        "accessPath_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "payloads_count": types.Integer(),
        "payloads_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "resultList_count": types.Integer(),
        "resultList_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "patch": types.Integer(),
        "cvssV3_base": types.Float(),
        "cvssV3_impact": types.Float(),
        "cvssV3_attackVector": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "severityComment": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "editedSeverityUser": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "history_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "wasc_count": types.Integer(),
        "wasc_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sslData_protocol": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sslData_virtualhost": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sslData_ip": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sslData_port": types.Integer(),
        "sslData_result": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sslData_list": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sslData_certificateFingerprint": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "sslData_flags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "updatedDate": types.DateTime(),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(finding) for finding in findings])

    # Drop any columns that we parsed out:
    df.drop(
        columns=[
            "webApp",
            "cwe",
            "owasp",
            "resultList",
            "cvssV3",
            "history",
            "wasc",
            "sslData",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
