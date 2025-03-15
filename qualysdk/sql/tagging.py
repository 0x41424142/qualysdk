"""
Contains the functions to upload supported tagging API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame, concat
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_tagging_tags(
    tags: BaseList,
    cnxn: Connection,
    table_name: str = "tagging_tags",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```tagging.get_tags```
    to a SQL database.

    Args:
        tags (BaseList): A BaseList of Tag objects.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "tagging_tags".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.INTEGER(),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "modified": types.DateTime(),
        "ruleType": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "parentTagId": types.INTEGER(),
        "ruleText": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "created": types.DateTime(),
        "children": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "color": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "criticalityScore": types.INTEGER(),
        "description": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "srcAssetGroupId": types.INTEGER(),
        "srcBusinessUnitId": types.INTEGER(),
        "provider": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(tag) for tag in tags])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
