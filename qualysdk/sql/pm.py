"""
Contains the functions to upload supported Patch Management API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_pm_jobs(
    jobs: BaseList,
    cnxn: Connection,
    table_name: str = "pm_jobs",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.list_jobs```
    to a SQL database.

    Args:
        jobs (BaseList): A BaseList of PMJob objects.
        cnxn (Connection): The Connection object to the SQL database.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "coAuthorUserIds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subCategory": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dynamicQQLType": types.Integer(),
        "matchAllTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "recurringWeekDays": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "totalAssetCount": types.Integer(),
        "isDynamicPatchesQQL": types.Boolean(),
        "assetCount": types.Integer(),
        "customPatchUrlConfigured": types.Boolean(),
        "linkedJobReferenceCount": types.Integer(),
        "created_date": types.DateTime(),
        "created_user_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "created_user_id": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "triggerStatus": types.Integer(),
        "recurringDayOfMonth": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "jobSource": types.Integer(),
        "readOnly": types.Boolean(),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "exclusionAssetIds": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scheduleType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "dayOfMonth": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "disabledPatches": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "filterType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "updated_date": types.DateTime(),
        "updated_user_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "updated_user_id": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "additionalQQLS": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "timezone": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "exclusionFilterType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "nextScheduleDateTime": types.DateTime(),
        "platform": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "mitigationActionCount": types.Integer(),
        "isPriorityJob": types.Boolean(),
        "customerId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "exclusionTags": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "taggedAssetCount": types.Integer(),
        "patchCount": types.Integer(),
        "applicableAssetCount": types.Integer(),
        "patchTuesdayPlusXDays": types.Integer(),
        "schemaVersion": types.Integer(),
        "recurringLastDayOfMonth": types.Boolean(),
        "recurringWeekDayOfMonth": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isRecurring": types.Boolean(),
        "lastScheduleDateTime": types.DateTime(),
        "dynamicPatchesQQL": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "startDateTime": types.DateTime(),
        "timezoneType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "deleted": types.Boolean(),
        "monthlyRecurringType": types.Integer(),
        "completionPercent": types.Float(),
        "category": types.Integer(),
        "linkedJobId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "assetResultReceivedCount": types.Integer(),
        "isVulnContext": types.Boolean(),
        "isAssetImported": types.Boolean(),
        "remediationQids": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(job) for job in jobs])

    # Drop cols that are parsed out into other fields:
    df.drop(
        columns=[
            "created",
            "updated",
        ],
        inplace=True,
    )

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
