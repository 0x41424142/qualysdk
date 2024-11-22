"""
Contains the functions to upload supported Certificate View API pulls to SQL DBs.
"""

from datetime import datetime

from pandas import DataFrame, concat
from sqlalchemy import Connection, types
from sqlalchemy.dialects.mysql import TEXT

from .base import upload_data, prepare_dataclass
from ..base.base_list import BaseList


def upload_cert_certs(
    certs: BaseList,
    cnxn: Connection,
    certs_table_name: str = "cert_certs",
    assets_table_name: str = "cert_assets",
    override_import_dt: datetime = None,
) -> int:
    """
    Upload results from ```cert.list_certs```
    to 2 DB tables: ```cert_certs``` and ```cert_assets``` by default.

    Args:
        certs (BaseList): A BaseList of Certificate objects.
        cnxn (Connection): The Connection object to the SQL database.
        certs_table_name (str): The name of the table to upload to. Defaults to "cert_certs".
        assets_table_name (str): The name of the table to upload to. Defaults to "cert_assets".
        override_import_dt (datetime): If provided, will override the import_datetime column with this value.

    Returns:
        int: The number of rows uploaded.
    """

    """
    Separate certs and assets list into two separate tables.
    We can link assets back to a cert by putting the cert.id in the assets table
    with pandas:
    """

    # Explicitly set the import datetime if not provided
    # so we can keep the two tables in sync:
    if not override_import_dt:
        override_import_dt = datetime.now()

    assets_df = DataFrame()
    certs_df = DataFrame()

    for cert in certs:
        for asset in cert.assets:
            asset_dict = prepare_dataclass(asset)
            # Add the cert ID to the asset so we can link them:
            asset_dict["certId"] = cert.id
            assets_df = concat([assets_df, DataFrame([asset_dict])], ignore_index=True)

        certs_df = concat(
            [certs_df, DataFrame([prepare_dataclass(cert)])],
            ignore_index=True,
        )

    # Upload the data:

    COLS = {
        "id": types.Integer(),
        "certhash": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "keySize": types.Integer(),
        "serialNumber": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "validToDate": types.DateTime(),
        "validTo": types.DateTime(),
        "validFromDate": types.DateTime(),
        "validFrom": types.DateTime(),
        "signatureAlgorithm": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "extendedValidation": types.Boolean(),
        "createdDate": types.DateTime(),
        "dn": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "subject_organization": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subject_locality": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subject_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subject_country": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "subject_organizationUnit": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "updateDate": types.DateTime(),
        "lastFound": types.DateTime(),
        "imported": types.Boolean(),
        "selfSigned": types.Boolean(),
        "issuer_organization": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "issuer_organizationUnit": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "issuer_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "issuer_country": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "issuer_state": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "issuer_certhash": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "issuer_locality": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "issuerCategory": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "instanceCount": types.Integer(),
        "assetCount": types.Integer(),
        "sources": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "assets": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "type": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "rootissuer_organization": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rootissuer_organizationUnit": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rootissuer_name": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rootissuer_country": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rootissuer_state": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rootissuer_certhash": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "rootissuer_locality": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    # Drop columns that we parsed out:
    certs_df.drop(
        columns=[
            "subject",
            "issuer",
            "rootissuer",
        ],
        inplace=True,
    )

    certs_uploaded = upload_data(
        certs_df, certs_table_name, cnxn, COLS, override_import_dt
    )

    print(f"Uploaded {certs_uploaded} to {certs_table_name}. Moving to assets...")

    COLS = {
        "id": types.Integer(),
        "certId": types.Integer(),
        "uuid": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "netbiosName": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "name": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "operatingSystem": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "hostInstances": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "assetInterfaces": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
        "tags": types.String().with_variant(TEXT(charset="utf8"), "mysql", "mariadb"),
        "primaryIp": types.String().with_variant(
            TEXT(charset="utf8"), "mysql", "mariadb"
        ),
    }

    assets_uploaded = upload_data(
        assets_df, assets_table_name, cnxn, COLS, override_import_dt
    )

    print(f"Uploaded {assets_uploaded} to {assets_table_name}.")

    return certs_uploaded
