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
        "drift_category": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vulnerabilities": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "drift_reason": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "drift_software": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "drift_vulnerability": types.String().with_variant(
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
            "drift",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_cs_software(
    software: BaseList,
    cnxn: Connection,
    table_name: str = "cs_software",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```cs.get_software_on_container```
    to a SQL database.

    Args:
        software (BaseList): A BaseList of csSoftware objects.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "packagePath": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "fixVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        # vulnerabilities is parsed into below fields:
        "vulnerabilities_severity5Count": types.Integer(),
        "vulnerabilities_severity4Count": types.Integer(),
        "vulnerabilities_severity3Count": types.Integer(),
        "vulnerabilities_severity2Count": types.Integer(),
        "vulnerabilities_severity1Count": types.Integer(),
        # End vulnerabilities fields
        "containerSha": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(software) for software in software])

    # Drop cols that are parsed out into other fields:
    df.drop(
        columns=[
            "vulnerabilities",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_cs_vulns(
    vulns: BaseList,
    cnxn: Connection,
    table_name: str = "cs_vulns",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```cs.get_container_vulns```
    to a SQL database.

    Args:
        vulns (BaseList): A BaseList of csVuln objects.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "qid": types.Integer(),
        "title": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "result": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "severity": types.Integer(),
        "customerSeverity": types.Integer(),
        "qdsScore": types.Integer(),
        "cvssInfo_baseScore": types.Float(),
        "cvssInfo_temporalScore": types.Float(),
        "cvssInfo_accessVector": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cvss3Info_baseScore": types.Float(),
        "cvss3Info_temporalScore": types.Float(),
        "port": types.Integer(),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "risk": types.Integer(),
        "category": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "discoveryType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "authType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "supportedBy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "product": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vendor": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "cveids": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "threatIntel": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "software": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "lastFound": types.DateTime(),
        "firstFound": types.DateTime(),
        "typeDetected": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "source": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "reason": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "imageResult": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "containerResult": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "containerSha": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vulnerability": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isExempted": types.Boolean(),
        "vendorData": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(vuln) for vuln in vulns])
    # Drop cols that are parsed out into other fields:
    df.drop(
        columns=["cvssInfo", "cvss3Info"],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
