"""
static_searchlist.py - Contains the StaticSearchlist dataclass for the Qualys VMDR module.
"""

from dataclasses import dataclass, field
from typing import *
from datetime import datetime

from ...base import BaseList
from .detection import Detection

@dataclass
class StaticSearchList:
    """
    StaticSearchList - represents a single Static Search List in VMDR.
    """

    ID: int = field(metadata={"description": "The ID of the Static Search List."})
    TITLE: str = field(metadata={"description": "The title of the Static Search List."})
    GLOBAL: bool = field(metadata={"description": "Whether the Static Search List is global."})
    OWNER: str = field(metadata={"description": "The owner of the Static Search List."})
    CREATED: Union[str, datetime] = field(metadata={"description": "The date the Static Search List was created."})
    MODIFIED: Union[str, datetime] = field(metadata={"description": "The date the Static Search List was last modified."})
    MODIFIED_BY: str = field(metadata={"description": "The user who last modified the Static Search List."})
    QIDS: BaseList[Detection]