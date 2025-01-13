"""
Contains the functions to upload supported Patch Management API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame, concat
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
        table_name (str): The name of the table to upload to. Defaults to "pm_jobs".
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


def upload_pm_job_results(
    job_results: BaseList,
    cnxn: Connection,
    jobs_table_name: str = "pm_job_results_jobResults",
    assets_table_name: str = "pm_job_results_assets",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.get_job_results```
    to 2 DB tables: ```pm_job_results_jobResults```
    and ```pm_job_results_assets``` by default.

    Args:
        job_results (BaseList): A BaseList of JobResultSummary objects.
        cnxn (Connection): The Connection object to the SQL database.
        jobs_table_name (str): The name of the table to upload to. Defaults to "pm_job_results".
        assets_table_name (str): The name of the table to upload to. Defaults to "pm_job_results_assets".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    """
    Separate job summary and assets list into two separate tables.
    We can link assets back to a job by putting the job.id in the assets table
    with pandas:
    """

    # Explicitly set the import datetime if not provided
    # so we can keep the two tables in sync:
    if not override_import_dt:
        override_import_dt = datetime.now()

    assets_df = DataFrame()
    job_results_df = DataFrame()

    for job_result in job_results:
        for asset in job_result.assets:
            asset_dict = prepare_dataclass(asset)
            assets_df = concat([assets_df, DataFrame([asset_dict])], ignore_index=True)

        job_results_df = concat(
            [job_results_df, DataFrame([prepare_dataclass(job_result)])],
            ignore_index=True,
        )

    # Upload the data:

    COLS = {
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "assetCount": types.Integer(),
        "patchCount": types.Integer(),
        "createdBy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "createdOn": types.DateTime(),
        "assets": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    job_summaries_uploaded = upload_data(
        job_results_df, jobs_table_name, cnxn, COLS, override_import_dt
    )

    print(
        f"Uploaded {job_summaries_uploaded} to {jobs_table_name}. Moving to assets..."
    )

    COLS = {
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "operatingSystem": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "jobId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "lastLoggedOnUser": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "successPatches": types.Integer(),
        "installedPatches": types.Integer(),
        "failedPatches": types.Integer(),
        "supersededPatches": types.Integer(),
        "notApplicablePatches": types.Integer(),
        "executing": types.Boolean(),
        "pendingExecution": types.Boolean(),
        "pendingReboot": types.Boolean(),
        "pendingVerification": types.Boolean(),
        "jobInstanceId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "interfaces": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "skipPatchCount": types.Integer(),
        "additionalFields": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "endDateTime": types.DateTime(),
        "startDateTime": types.DateTime(),
        "statusDateTime": types.DateTime(),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "statusCode": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "jobSentOn": types.DateTime(),
        "installed": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "failed": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "success": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "superseded": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "notApplicable": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "failedActionsCount": types.Integer(),
        "successfulActionsCount": types.Integer(),
        "skippedActionsCount": types.Integer(),
        "interimResultStatus": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "totalPatchCount": types.Integer(),
        "runId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "scanDateTime": types.DateTime(),
        "pendingForRebootInAnotherJob": types.Boolean(),
        "pendingForRebootInAnotherJobName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "osIdentifier": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    assets_uploaded = upload_data(
        assets_df, assets_table_name, cnxn, COLS, override_import_dt
    )

    return assets_uploaded


def upload_pm_job_runs(
    runs: BaseList,
    cnxn: Connection,
    table_name: str = "pm_job_runs",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.get_job_runs```
    to a SQL database.

    Args:
        runs (BaseList): A BaseList of PMJobRun objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_job_runs".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "jobInstanceId": types.Integer(),
        "jobId": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "scheduledDateTime": types.DateTime(),
        "timezoneType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(run) for run in runs])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_cves(
    qids: BaseList,
    cnxn: Connection,
    table_name: str = "pm_cves_for_qids",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.lookup_cves```
    to a SQL database.

    Args:
        qids (BaseList): A BaseList of QID objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_cves_for_qids".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.Integer(),
        "title": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "cves": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "detectedDate": types.DateTime(),
        "severity": types.Integer(),
        "vulnType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(qid) for qid in qids])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_patches(
    patches: BaseList,
    cnxn: Connection,
    table_name: str = "pm_patches",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.get_patches```
    to a SQL database.

    Args:
        patches (BaseList): A BaseList of Patch objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_patches".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "title": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "platform": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "architecture": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "bulletin": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "category": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cve": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "kb": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "modifiedDate": types.DateTime(),
        "appFamily": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "product": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "publishedDate": types.DateTime(),
        "qid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "rebootRequired": types.Boolean(),
        "supersededBy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "supersedes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vendor": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "vendorSeverity": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vendorlink": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "missingCount": types.Integer(),
        "installedCount": types.Integer(),
        "advisory": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "enabled": types.Boolean(),
        "packageDetails": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isSecurity": types.Boolean(),
        "isSuperseded": types.Boolean(),
        "isRollback": types.Boolean(),
        "isCustomizedDownloadUrl": types.Boolean(),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(patch) for patch in patches])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_assets(
    assets: BaseList,
    cnxn: Connection,
    table_name: str = "pm_assets",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.get_assets``` to a SQL database.

    Args:
        assets (BaseList): A BaseList of PMAsset objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_assets".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "operatingSystem": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "version": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "platform": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "osIdentifier": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "interfaces": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanStatus": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "status": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "statusCode": types.Integer(),
        "installedPatchCount": types.Integer(),
        "missingPatchCount": types.Integer(),
        "nonSupersededMissingPatchCount": types.Integer(),
        "activatedModules": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "lastLoggedOnUser": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "scanDateTime": types.DateTime(),
        "statusDateTime": types.DateTime(),
        "hardware_model": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hardware_manufacturer": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "architecture": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "osNotSupportedForModules": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(asset) for asset in assets])

    # Drop the hardware column:
    df.drop(columns=["hardware"], inplace=True)

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_assetids_to_uuids(
    uuids: BaseList[tuple[str, str]],
    cnxn: Connection,
    table_name: str = "pm_assetids_to_uuids",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.lookup_host_uuids``` to a SQL database.

    Args:
        uuids (BaseList[tuple[str,str]]): A BaseList of tuples of asset IDs and UUIDs.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_assetids_to_uuids".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "assetId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "uuid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
    }

    # This data is structured a bit differently.
    # It is a tuple with 2 strings.

    # Prepare the dataclass for insertion:
    df = DataFrame(uuids, columns=["asset_id", "uuid"])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_patch_catalog(
    patches: BaseList,
    cnxn: Connection,
    table_name: str = "pm_patch_catalog",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.get_patch_catalog```
    to a SQL database.

    Args:
        patches (BaseList): A BaseList of CatalogPatch objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_patch_catalog".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "patchId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "id": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "title": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "appFamily": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vendor": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "product": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "platform": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "kb": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "isSuperseded": types.Boolean(),
        "isSecurity": types.Boolean(),
        "isRollback": types.Boolean(),
        "servicePack": types.Boolean(),
        "advisory": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "vendorlink": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "osIdentifier": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "advisoryLink": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "deleted": types.Boolean(),
        "rebootRequired": types.Boolean(),
        "vendorSeverity": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "qid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "enabled": types.Boolean(),
        "downloadMethod": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "supportedOs": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "supersedes": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "notification": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "cve": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "architecture": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "packageDetails": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "patchFeedProviderId": types.Integer(),
        "syncDateTime": types.DateTime(),
        "vendorPatchId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "modifiedDate": types.DateTime(),
        "publishedDate": types.DateTime(),
        "category": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "isEsuPatch": types.Boolean(),
        "supersededBy": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "bulletin": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(patch) for patch in patches])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_windows_products(
    products: BaseList,
    cnxn: Connection,
    table_name: str = "pm_windows_products",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.get_products_in_windows_patch```
    to a SQL database.

    Args:
        products (BaseList): A BaseList of AssociatedProduct objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_windows_products".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "patchId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "product": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(product) for product in products])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_linux_packages(
    packages: BaseList,
    cnxn: Connection,
    table_name: str = "pm_linux_packages",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.get_packages_in_linux_patch```
    to a SQL database.

    Args:
        packages (BaseList): A BaseList of AssociatedProduct objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_linux_packages".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "patchId": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "packageName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "architecture": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(package) for package in packages])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)


def upload_pm_product_vuln_counts(
    counts: BaseList,
    cnxn: Connection,
    table_name: str = "pm_product_vuln_counts",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```pm.count_product_vulns``` to a SQL database.

    Args:
        counts (BaseList): A BaseList of ProductVulnCount objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "pm_product_vuln_counts".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """
    '''@dataclass
class ProductVulnCount(BaseClass):
    """
    Represents a product and its associated QID count/details.
    """

    name: str
    totalQIDCount: int = 0
    patchableQIDCount: int = None
    type: str = None
    patchableQIDs: str = None
    totalQIDs: int = None
    severity: Literal["Critical", "Important", "Moderate", "Low", "None"] = "Undefined"'''

    COLS = {
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "totalQIDCount": types.Integer(),
        "patchableQIDCount": types.Integer(),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "patchableQIDs": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "totalQIDs": types.Integer(),
        "severity": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(count) for count in counts])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
