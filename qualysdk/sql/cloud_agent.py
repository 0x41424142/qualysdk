"""
cloud_agent.py - Contains the functions to upload supported cloud_agent API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types

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
        "name": types.String(),
        "created": types.DateTime(),
        "modified": types.DateTime(),
        "type": types.String(),
        "tags": types.String(),  # BaseList
        "sourceInfo": types.String(),  # list
        "qwebHostId": types.Integer(),
        "lastComplianceScan": types.DateTime(),
        "lastSystemBoot": types.DateTime(),
        "lastLoggedOnUser": types.String(),
        "dnsHostName": types.String(),
        "agentInfo_agentVersion": types.String(),
        "agentInfo_agentId": types.String(),
        "agentInfo_status": types.String(),
        "agentInfo_lastCheckedIn": types.DateTime(),
        "agentInfo_connectedFrom": types.String(),
        "agentInfo_location": types.String(),
        "agentInfo_locationGeoLatitude": types.Float(),
        "agentInfo_locationGeoLongitude": types.Float(),
        "agentInfo_chirpStatus": types.String(),
        "agentInfo_platform": types.String(),
        "agentInfo_activatedModule": types.String(),
        "agentInfo_manifestVersion": types.String(),
        "agentInfo_agentConfiguration_id": types.Integer(),
        "agentInfo_agentConfiguration_name": types.String(),
        "agentInfo_activationKey_activationId": types.String(),
        "agentInfo_activationKey_title": types.String(),
        "netbiosName": types.String(),
        "criticalityScore": types.Integer(),
        "lastVulnScan": types.DateTime(),
        "vulnsUpdated": types.DateTime(),
        "informationGatheredUpdated": types.DateTime(),
        "domain": types.String(),
        "fqdn": types.String(),
        "os": types.String(),
        "networkGuid": types.String(),
        "address": types.String(),
        "trackingMethod": types.String(),
        "manufacturer": types.String(),
        "model": types.String(),
        "totalMemory": types.Integer(),
        "timezone": types.String(),
        "biosDescription": types.String(),
        "openPort": types.String(),  # BaseList
        "software": types.String(),  # BaseList
        "vuln": types.String(),  # BaseList
        "processor": types.String(),  # BaseList
        "volume": types.String(),  # BaseList
        "account": types.String(),  # BaseList
        "networkInterface": types.String(),  # BaseList
        "isDockerHost": types.Boolean(),
        "dockerInfo": types.String(),  # list
        "cloudProvider": types.String(),
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
