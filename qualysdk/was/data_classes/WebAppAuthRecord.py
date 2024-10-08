"""
Contains the WebAppAuthRecord class for the WAS module.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from operator import ge
from typing import Union, Literal

from requests import get

from qualysdk.was.data_classes.Tag import WASTag

from ...base.base_list import BaseList
from .Comment import Comment
from .WebAppAuthFormRecord import WebAppAuthFormRecord
from .WebAppAuthServerRecord import WebAppAuthServerRecord


def build_oauth2_record(dataclass) -> None:
    """
    Builds the OAuth2 record for a WebAppAuthRecord

    Args:
        dataclass: The dataclass to build the OAuth2 record for

    Returns:
        None
    """

    for field in [
        "grantType",
        "accessTokenUrl",
        "clientId",
        "clientSecret",
        "scope",
        "seleniumCreds",
    ]:
        setattr(
            dataclass,
            f"oauth2Record_{field}",
            getattr(dataclass, "oauth2Record").get(field),
        )

    setattr(
        dataclass,
        "oauth2Record_seleniumCreds",
        getattr(dataclass, "oauth2Record").get("seleniumCreds") == "true",
    )

    setattr(dataclass, "oauth2Record", None)


def handle_qualys_list(data: dict, key: str) -> tuple[int, BaseList]:
    """
    Normalizes list responses from Qualys

    Args:
        data (dict): The data to normalize
        key (str): The key to normalize

    Returns:
        tuple[int, BaseList]: The count and the list
    """

    # Mappings for object creation:
    MAPPINGS = {
        "WebAppAuthFormRecordField": WebAppAuthFormRecord,
        "WebAppAuthServerRecordField": WebAppAuthServerRecord,
        "Comment": Comment,
        "Tag": WASTag,
        "formRecord": WebAppAuthFormRecord,
        "serverRecord": WebAppAuthServerRecord,
    }

    # Easy short circuit, with walrus to save value:
    if data.get("count") == "0":
        return 0, BaseList()

    list_key = data.get("list")

    fields_record = False
    # Check for the record-specific fields key:
    if not list_key and len(data.keys()) > 1:
        list_key = data.get("fields", {}).get("list")
        # Raise the data up by one key:
        if not list_key:
            return int(data["fields"].get("count", 0)), BaseList()

        to_raise = list(list_key.keys())[0]
        list_key = list_key[to_raise]
        fields_record = True

    if not list_key:
        return int(data.get("count", 0)), BaseList()

    if not fields_record:
        list_data = list_key.get(key)
    else:
        list_data = list_key

    if isinstance(list_data, dict):
        list_data = [list_data]

    base_list = BaseList()

    for i in list_data:
        # Get the class to use:
        class_name = MAPPINGS.get(key, None)
        if not class_name:
            continue
        base_list.append(class_name.from_dict(i))

    return len(base_list), base_list


def handle_record_attrs(
    dataclass, subkey: Literal["form", "server", "comments"]
) -> None:
    """
    Sets the sslOnly and authVault attributes
    on a record. Backend function.

    Args:
        dataclass: The dataclass to set the attributes on
        subkey: The subkey to set the attributes on

    Returns:
        None
    """

    if subkey not in ["formRecord", "serverRecord", "Comment"]:
        raise ValueError("subkey must be one of 'form', 'server', or 'Comment'")
    if subkey != "Comment":
        setattr(
            dataclass,
            f"{subkey}_authVault",
            getattr(dataclass, subkey).get("authVault") == "true",
        )
        setattr(
            dataclass,
            f"{subkey}_sslOnly",
            getattr(dataclass, subkey).get("sslOnly") == "true",
        )
        setattr(dataclass, f"{subkey}_type", getattr(dataclass, subkey).get("type"))
        if "seleniumCreds" in getattr(dataclass, subkey):
            setattr(
                dataclass,
                f"{subkey}_seleniumCreds",
                getattr(dataclass, subkey).get("seleniumCreds") == "true",
            )

        list_data = handle_qualys_list(getattr(dataclass, subkey), subkey)
        setattr(dataclass, f"{subkey}_fields_count", list_data[0])
        setattr(dataclass, f"{subkey}_fields_list", list_data[1])
        setattr(dataclass, subkey, None)
    else:
        list_data = handle_qualys_list(getattr(dataclass, "comments"), subkey)
        setattr(dataclass, f"comments_count", list_data[0])
        setattr(dataclass, f"comments_list", list_data[1])
        setattr(dataclass, "comments", None)


def handle_date_by_attrs(dataclass, subkey: Literal["createdBy", "updatedBy"]) -> None:
    """
    Handles date fields by attributes

    Args:
        dataclass: The dataclass to handle
        subkey: The subkey to handle

    Returns:
        None
    """
    if subkey not in ["createdBy", "updatedBy", "owner"]:
        raise ValueError("subkey must be one of 'createdBy', 'updatedBy', 'owner'")

    if getattr(dataclass, subkey):
        setattr(dataclass, f"{subkey}_id", int(getattr(dataclass, subkey).get("id")))
        setattr(
            dataclass, f"{subkey}_username", getattr(dataclass, subkey).get("username")
        )
        setattr(
            dataclass,
            f"{subkey}_firstName",
            getattr(dataclass, subkey).get("firstName"),
        )
        setattr(
            dataclass, f"{subkey}_lastName", getattr(dataclass, subkey).get("lastName")
        )
        setattr(dataclass, subkey, None)


@dataclass
class WebAppAuthRecord:
    """
    Represents an authentication record
    in Qualys WAS
    """

    id: Union[str, int] = None
    name: str = None
    owner: None = None
    # owner is parsed into below fields:
    owner_id: Union[str, int] = None
    owner_username: str = None
    owner_firstName: str = None
    owner_lastName: str = None
    # end owner
    formRecord: None = None
    # form_record is parsed into below fields:
    formRecord_type: str = None
    formRecord_sslOnly: bool = None
    formRecord_authVault: bool = None
    formRecord_seleniumCreds: bool = None
    formRecord_fields_count: Union[str, int] = 0
    formRecord_fields_list: BaseList = None
    # end form_record
    serverRecord: None = None
    # serverRecord is parsed into below fields:
    serverRecord_type: str = None
    serverRecord_sslOnly: bool = None
    serverRecord_authVault: bool = None
    serverRecord_fields_count: Union[str, int] = 0
    serverRecord_fields_list: BaseList = None
    # end serverRecord
    oauth2Record: None = None
    # oauth2Record is parsed into below fields:
    oauth2Record_grantType: str = None
    oauth2Record_accessTokenUrl: str = None
    oauth2Record_clientId: str = None
    oauth2Record_clientSecret: str = None
    oauth2Record_scope: str = None
    oauth2Record_seleniumCreds: bool = None
    # end oauth2Record
    tags: None = None
    # tags is parsed into below fields:
    tags_count: Union[str, int] = 0
    tags_list: BaseList = None
    # end tags
    comments: None = None
    # comments is parsed into below fields:
    comments_count: Union[str, int] = 0
    comments_list: BaseList = None
    # end comments
    createdDate: Union[str, datetime] = None
    updatedDate: Union[str, datetime] = None
    createdBy: None = None
    # createdBy is parsed into below fields:
    createdBy_id: Union[str, int] = None
    createdBy_username: str = None
    createdBy_firstName: str = None
    createdBy_lastName: str = None
    # end createdBy
    updatedBy: None = None
    # updatedBy is parsed into below fields:
    updatedBy_id: Union[str, int] = None
    updatedBy_username: str = None
    updatedBy_firstName: str = None
    updatedBy_lastName: str = None
    # end updatedBy

    def __post_init__(self):
        setattr(self, "id", int(self.id))

        DT_FIELDS = ["createdDate", "updatedDate"]
        DATEBY_FIELDS = ["owner", "createdBy", "updatedBy"]
        RECORD_FIELDS = ["formRecord", "serverRecord", "comments"]

        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        for field in DATEBY_FIELDS:
            if getattr(self, field):
                handle_date_by_attrs(self, field)

        if self.tags:
            res = handle_qualys_list(self.tags, "Tag")
            setattr(self, "tags_count", res[0])
            setattr(self, "tags_list", res[1])
            setattr(self, "tags", None)

        for field in RECORD_FIELDS:
            if getattr(self, field):
                handle_record_attrs(self, field if field != "comments" else "Comment")

        if self.oauth2Record:
            build_oauth2_record(self)

    def to_dict(self):
        return asdict(self)

    def __dict__(self):
        return self.to_dict()

    def __str__(self):
        return str(self.name)

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
