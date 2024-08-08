"""
SQL server integration for qualysPy
"""

from .base import db_connect
from .supported_uploads import upload_vmdr_ags, upload_vmdr_kb, upload_vmdr_hosts, upload_vmdr_ips
