"""
cloud_agent.py - Contains the functions to upload supported cloud_agent API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_cloud_agents(
    hosts: BaseList,
    cnxn: Connection,
    table_name: str = "cloud_agent_agents",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```cloud_agent.list_agents``` to a SQL database.

    Args:
        agents (BaseList): A BaseList of CloudAgent objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "cloud_agent_agents".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.Integer(),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "created": types.DateTime(),
        "modified": types.DateTime(),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "tags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "sourceInfo": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # list
        "qwebHostId": types.Integer(),
        "lastComplianceScan": types.DateTime(),
        "lastSystemBoot": types.DateTime(),
        "lastLoggedOnUser": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dnsHostName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_agentVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_agentId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_status": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_lastCheckedIn": types.DateTime(),
        "agentInfo_connectedFrom": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_location": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_locationGeoLatitude": types.Float(),
        "agentInfo_locationGeoLongitude": types.Float(),
        "agentInfo_chirpStatus": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_platform": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_activatedModule": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_manifestVersion": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_agentConfiguration_id": types.Integer(),
        "agentInfo_agentConfiguration_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_activationKey_activationId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "agentInfo_activationKey_title": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "netbiosName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "criticalityScore": types.Integer(),
        "lastVulnScan": types.DateTime(),
        "vulnsUpdated": types.DateTime(),
        "informationGatheredUpdated": types.DateTime(),
        "domain": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "fqdn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "os": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "networkGuid": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "address": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "trackingMethod": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "manufacturer": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "model": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "totalMemory": types.Integer(),
        "timezone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "biosDescription": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "openPort": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "software": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "vuln": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "processor": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "volume": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "account": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "networkInterface": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # BaseList
        "isDockerHost": types.Boolean(),
        "dockerInfo": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),  # list
        "cloudProvider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(host) for host in hosts])

    # Drop cols that are parsed out into other fields:
    df.drop(
        columns=[
            "agentInfo_activationKey",
            "agentInfo_agentConfiguration",
            "agentInfo",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
