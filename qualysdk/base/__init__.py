"""
Basic functionality / helpers for qualysdk.
"""

from .call_api import call_api
from .call_schema import CALL_SCHEMA
from .xml_parser import xml_parser
from .base_list import BaseList
from .csv_export import write_csv, write_excel
from .json_export import write_json


class DONT_EXPAND:
    """
    This singleton class is used to
    indicate that nested data should
    not be blown out in the dataclasses.
    Used mainly for JSON export.
    """

    flag = False
