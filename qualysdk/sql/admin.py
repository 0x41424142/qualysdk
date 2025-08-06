"""
Contains the functions to upload supported administration API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data
from ..base.base_list import BaseList


def upload_admin_userdata(
    users: BaseList,
    cnxn: Connection,
    table_name: str = "admin_userdata",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```admin.get_user_details``` or ```admin.search_users``` API calls
    to a SQL database.

    Args:
        users (BaseList): A BaseList of User objects from an admin API call.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to. Defaults to "admin_userdata".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    COLS = {
        "id": types.INTEGER(),
        "username": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "firstName": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "lastName": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "emailAddress": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "title": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "scopeTags": types.JSON(),
        "roleList": types.JSON(),
    }

    # Prepare the dataclass for insertion:
    df = DataFrame([user.serialized() for user in users])

    # Upload the data:
    return upload_data(df, table_name, cnxn, COLS, override_import_dt)
