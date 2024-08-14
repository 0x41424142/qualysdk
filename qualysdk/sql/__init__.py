"""
SQL server integration for qualysdk
"""

from .base import db_connect
from .vmdr import (
    upload_vmdr_ags,
    upload_vmdr_kb,
    upload_vmdr_hosts,
    upload_vmdr_ips,
    upload_vmdr_hld,
    upload_vmdr_scanners,
    upload_vmdr_static_searchlists,
    upload_vmdr_users,
    upload_vmdr_scanlist,
)
