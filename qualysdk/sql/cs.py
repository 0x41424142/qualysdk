"""
Contains the functions to upload supported Container Security API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_cs_containers(
    containers: BaseList,
    cnxn: Connection,
    table_name: str = "cs_containers",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```cs.list_containers```
    to a SQL database.

    Args:
        containers (BaseList): A BaseList of Container objects.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "imageId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "imageUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "containerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "created": types.DateTime(),
        "updated": types.DateTime(),
        "label": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "uuid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "sha": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "privileged": types.Boolean(),
        "path": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "imageSha": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "macAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "customerUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "ipv4": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "ipv6": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "host_sensorUuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "host_hostname": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "host_ipAddress": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "host_uuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "host_lastUpdated": types.DateTime(),
        "hostArchitecture": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "state": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "portMapping": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "stateChanged": types.DateTime(),
        "services": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "operatingSystem": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "lastScanned": types.DateTime(),
        "source": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "environment": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "arguments": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "command": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "drift": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "vulnerabilities": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "softwares": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isDrift": types.Boolean(),
        "isRoot": types.Boolean(),
        "cluster": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "users": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "riskScore": types.Integer(),
        "riskScoreCalculatedDate": types.DateTime(),
        "cloudProvider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "maxQdsScore": types.Integer(),
        "qdsSeverity": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "formulaUsed": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanTypes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "criticality": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "criticalityUpdated": types.DateTime(),
        "isExposedToWorld": types.Boolean(),
        "k8sExposure": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "exceptions": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "compliance_failCount": types.Integer(),
        "compliance_passCount": types.Integer(),
        "compliance_errorCount": types.Integer(),
        "lastComplianceScanned": types.DateTime(),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(container) for container in containers])

    # Drop cols that are parsed out into other fields:
    df.drop(
        columns=[
            "host",
            "cluster",
            "compliance",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
