"""
base.py - contains the base functionality for the SQL module of qualysPy.
"""

from datetime import datetime
from dataclasses import dataclass

from sqlalchemy import types

from pandas import DataFrame
from sqlalchemy import create_engine, Connection, types


def db_connect(
    host: str,
    db: str,
    username: str = None,
    password: str = None,
    driver: str = "ODBC Driver 17 for SQL Server",
    trusted_cnxn: bool = False,
) -> Connection:
    """
    Generate a sqlalchemy Connection object to a SQL database.

    Parameters:
    host (str): The hostname of the SQL server.
    db (str): The name of the database.
    username (str): The username to use to connect to the database.
    password (str): The password to use to connect to the database.
    driver (str): The ODBC driver to use to connect to the database.
    trusted_cnxn (bool): If True, use trusted connection.

    Returns:
    Connection: The Connection object to the SQL database.
    """

    # Check if user AND password are provided, or trusted connection is used:
    if not (username and password) and not trusted_cnxn:
        raise ValueError(
            "You must provide a username and password, or use trusted connection."
        )

    # Generate the connection string:
    if trusted_cnxn:
        conn_str = f"mssql+pyodbc://{host}/{db}?driver={driver}&trusted_connection=yes"
    else:
        conn_str = f"mssql+pyodbc://{username}:{password}@{host}/{db}?driver={driver}"

    engine = create_engine(conn_str)

    return engine.connect()


def upload_data(df: DataFrame, table: str, cnxn: Connection, dtype: dict) -> int:
    """
    Upload a DataFrame to a SQL table. Appends 'import_datetime' column to the DataFrame.

    Parameters:
    df (DataFrame): The DataFrame to upload.
    table (str): The name of the table to upload to.
    cnxn (Connection): The Connection object to the SQL database.
    dtype (dict): The data types of the columns in the table.

    Returns:
    int: The number of rows uploaded.
    """

    # Add an import_datetime column:
    df["import_datetime"] = datetime.now()
    dtype["import_datetime"] = types.DateTime()

    # For any string values in the DataFrame, make sure it doesn't
    # exceed VARCHAR(MAX) length:
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.slice(0, 2147483647)

    # Upload the data:
    print(f"Uploading {len(df)} rows to {table}...")
    df.to_sql(table, cnxn, if_exists="append", index=False, dtype=dtype, method=None)

    return len(df)


def prepare_dataclass(dataclass: dataclass) -> dict:
    """
    Prepare the dataclass for insertion into a SQL database
    by converting it to a dictionary with appropriate list/dataclass
    conversions.

    Parameters:
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
        "TRURISK_SCORE_FACTORS",
        "IP",
        "IPV6",
    ]
    DICT_FIELDS = [
        "CORRELATION",
        "CVSS",
        "CVSS_V3",
        "PCI_REASONS",
        "DISCOVERY",
        "CHANGE_LOG",
        "USER_DEF",
    ]

    # Iterate over the attrs of the dataclass and convert them to the appropriate format for SQL insertion.

    for attr in dataclass.__dataclass_fields__.keys():
        if getattr(dataclass, attr):
            if attr in TO_STR_FIELDS:
                setattr(dataclass, attr, str(getattr(dataclass, attr)))
            elif attr in DICT_FIELDS:
                setattr(
                    dataclass, attr, flatten_dict_to_string(getattr(dataclass, attr))
                )

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
