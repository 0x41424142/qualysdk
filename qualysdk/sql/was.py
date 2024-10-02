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
        "riskScore": types.Integer(),
        "owner": types.Integer(),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "createdDate": types.DateTime(),
        "updatedDate": types.DateTime(),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([prepare_dataclass(webapp) for webapp in webapps])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
