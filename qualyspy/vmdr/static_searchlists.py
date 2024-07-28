"""
static_searchlists.py - Contains functions to interact with Static Searchlists in VMDR.
"""

from typing import *
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import *
from ..base import call_api, xml_parser
from .data_classes import BaseList
from .data_classes import StaticSearchlist