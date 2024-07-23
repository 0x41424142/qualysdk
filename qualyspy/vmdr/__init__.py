"""
VMDR (Vulnerability Management) module

This module contains ways to interact with the Qualys VMDR API. Valid endpoints are defined in the CALL_SCHEMA dictionary.

VMDR QQL Syntax help: https://qualysguard.qg2.apps.qualys.com/portal-help/en/vm/search/how_to_search.htm
"""

from .data_classes import (
    Software,
    VendorReference,
    CVEID,
    KBEntry,
    Bugtraq,
    ThreatIntel,
    Compliance,
    Tag,
    CloudTag,
    Detection,
    QDSFactor,
    QDS,
)
from .data_classes.lists import BaseList

from .query_kb import query_kb
from .get_host_list import get_host_list
from .get_host_list_detections import get_hld
from .ips import get_ip_list, add_ips, update_ips
from .assetgroups import *
from .vmscans import get_scan_list
