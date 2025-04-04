"""
base.py - contains the base functionality for the SQL module of qualysdk.
"""

from datetime import datetime
from dataclasses import dataclass
from typing import Literal

from pandas import DataFrame
from sqlalchemy import create_engine, Connection, types

from ..base.base_class import IP_TYPES
from ..base.base_list import BaseList


def db_connect(
    host: str = "localhost",
    db: str = "qualysdk",
    username: str = None,
    password: str = None,
    trusted_cnxn: bool = False,
    db_type: Literal["mssql", "mysql", "postgresql", "sqlite", "sqlite3"] = "mssql",
    port: int = 1433,
) -> Connection:
    """

    Generate a sqlalchemy Connection object to a SQL database.

    Args:
        host (str): The hostname of the SQL server.
        db (str): The name of the database.
        username (str): The username to use to connect to the database.
        password (str): The password to use to connect to the database.
        trusted_cnxn (bool): If True, use trusted connection on MSSQL. If False, use username and password. Defaults to False.
        db_type (str): The type of database to connect to. Defaults to 'mssql'. Options are 'mssql', 'mysql', 'postgresql', 'sqlite', 'sqlite3'.
        port (int): The port to connect to the database on. Defaults to 1433.

    Returns:
        Connection: The Connection object to the SQL database.
    """

    # Check if user AND password are provided, or trusted connection is used:
    if (
        not (username and password)
        and not trusted_cnxn
        and db_type not in ["sqlite", "sqlite3"]
    ):
        raise ValueError(
            "You must provide a username and password, or use trusted connection."
        )

    if trusted_cnxn and db_type != "mssql":
        raise ValueError("Trusted connection is only available for MSSQL.")

    match db_type:
        case "mssql":
            if trusted_cnxn:
                conn_str = rf"mssql+pymssql://{host}:{port}/{db}"
            else:
                conn_str = f"mssql+pymssql://{username}:{password}@{host}:{port}/{db}"
        case "mysql":
            conn_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db}"
        case "postgresql":
            conn_str = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}"
        case "sqlite" | "sqlite3":
            conn_str = f"sqlite:///{db}"
        case _:
            raise ValueError("Database type not supported.")

    engine = create_engine(conn_str)

    return engine.connect()


def upload_data(
    df: DataFrame,
    table: str,
    cnxn: Connection,
    dtype: dict,
    override_import_dt: datetime = None,
) -> int:
    """
    Upload a DataFrame to a SQL table. Appends 'import_datetime' column to the DataFrame.

    Args:
        df (DataFrame): The DataFrame to upload.
        table (str): The name of the table to upload to.
        cnxn (Connection): The Connection object to the SQL database.
        dtype (dict): The data types of the columns in the table. Key is the column name, value is the data type as sqlalchemy.types.Something()
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    # Add an import_datetime column:
    df["import_datetime"] = (
        datetime.now() if not override_import_dt else override_import_dt
    )
    dtype["import_datetime"] = types.DateTime()

    # Change any timezone-aware datetime columns to timezone-naive.
    # This is needed because some DBs (especially MSSQL) don't
    # play well with SQLALchemy/Pandas timezone-aware datetimes.
    for col in df.select_dtypes(include=["datetime64[ns, UTC]"]).columns:
        df[col] = df[col].dt.tz_localize(None)

    # Upload the data:
    print(f"Uploading {len(df)} rows to {table}...")
    df.to_sql(table, cnxn, if_exists="append", index=False, dtype=dtype, chunksize=4000)

    return len(df)


def prepare_dataclass(dataclass: dataclass) -> dict:
    """
    Prepare the dataclass for insertion into a SQL database
    by converting it to a dictionary with appropriate list/dataclass
    conversions.

    Args:
        dataclass (dataclass): The dataclass to convert.

    Returns:
        dict: The dataclass converted to a dictionary.
    """

    TO_STR_FIELDS = [
        "IP_SET",
        "APPLIANCE_IDS",
        "DNS_LIST",
        "HOST_IDS",
        "NETBIOS_LIST",
        "ASSIGNED_USER_IDS",
        "ASSIGNED_UNIT_IDS",
        "EC2_IDS",
        "COMMENTS",
        "DOMAIN_LIST",
        "BUGTRAQ_LIST",
        "SOFTWARE_LIST",
        "VENDOR_REFERENCE_LIST",
        "CVE_LIST",
        "THREAT_INTELLIGENCE",
        "COMPLIANCE_LIST",
        "TAGS",
        "CLOUD_PROVIDER_TAGS",
        "IP",
        "IPV6",
        "QDS",
        "QDS_FACTORS",
        "QIDS",
        "ASSET_GROUP_TITLE",
        "ASSET_GROUP_TITLE_LIST",
        "TARGET",
        "OPTION_PROFILES",
        "REPORT_TEMPLATES",
        "REMEDIATION_POLICIES",
        "DISTRIBUTION_GROUPS",
    ]

    DICT_FIELDS = [
        "CORRELATION",
        "CVSS",
        "CVSS_V3",
        "PCI_REASONS",
        "DISCOVERY",
        "CHANGE_LOG",
        "USER_DEF",
        "TRURISK_SCORE_FACTORS",
        "VLANS",
        "ML_VERSION",
        "VULNSIGS_VERSION",
        "OPTION_PROFILE",
        "STATUS",
        "DETAILS",
        "USER",
    ]

    # Iterate over the attrs of the dataclass and convert them to the appropriate format for SQL insertion.

    for attr in dataclass.__dataclass_fields__.keys():
        if getattr(dataclass, attr):
            if attr in TO_STR_FIELDS:
                setattr(dataclass, attr, str(getattr(dataclass, attr)))
            elif attr in DICT_FIELDS and isinstance(getattr(dataclass, attr), dict):
                setattr(
                    dataclass, attr, flatten_dict_to_string(getattr(dataclass, attr))
                )

    # If there are any leftover empties or ipv4/ipv6 addresses,
    # convert them to None/str as a failsafe: #NOTE: Refactor at some point!
    for attr in dataclass.__dataclass_fields__.keys():
        if not getattr(dataclass, attr):
            setattr(dataclass, attr, None)
        elif type(getattr(dataclass, attr)) not in [str, int, float, bool, datetime]:
            setattr(dataclass, attr, str(getattr(dataclass, attr)))

    sql_dict = dataclass.to_dict()

    return sql_dict


def flatten_dict_to_string(d, parent_key="") -> str:
    """
    Format dictionary fields to a string for SQL insertion.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{k}" if parent_key else k
        if isinstance(v, dict):
            items.append(flatten_dict_to_string(v, new_key))
        else:
            items.append(f"{new_key}:{v}")
    return ", ".join(items)


def upload_json(
    json_data: dict,
    cnxn: Connection,
    table_name: str,
    override_import_dt: datetime = None,
) -> int:
    """
    Upload a JSON-serializable dictionary to a SQL table.
    Appends 'import_datetime' column to the JSON data.

    Args:
        json_data (dict): The JSON data to upload.
        cnxn (Connection): The Connection object to the SQL database.
        table_name (str): The name of the table to upload to.
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    def check_nested_types(data):
        """
        Recursively check for datetime or ipaddress types in the data.
        Raise an error if such types are found.
        """

        if isinstance(data, dict):
            for key, value in data.items():
                check_nested_types(value)
        elif isinstance(data, list):
            for item in data:
                check_nested_types(item)
        elif isinstance(data, datetime):
            raise ValueError(
                f"Datetime object found. Please run to_serializable_dict() or to_serializable_list() before passing data to this function."
            )
        elif isinstance(data, IP_TYPES):
            raise ValueError(
                "IP address object found. Please run to_serializable_dict() or to_serializable_list() before passing data to this function."
            )

    # Perform the check on the provided json_data
    check_nested_types(json_data)

    df = DataFrame.from_records(json_data)

    # Add an import_datetime column:
    df["import_datetime"] = (
        datetime.now() if not override_import_dt else override_import_dt
    )
    df["import_datetime"] = df["import_datetime"].dt.tz_localize(None)

    # Convert all dict and list columns to strings:
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(lambda x: str(x) if isinstance(x, (dict, list)) else x)

    # Upload the data:
    print(f"Uploading {len(df)} rows to {table_name}...")
    df.to_sql(table_name, cnxn, if_exists="append", index=False, chunksize=4000)

    return len(df)
