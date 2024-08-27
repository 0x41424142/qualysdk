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
    upload_vmdr_static_search_lists,
    upload_vmdr_users,
    upload_vmdr_scan_list,
    upload_vmdr_report_list,
    upload_vmdr_scheduled_report_list,
    upload_vmdr_template_list,
    upload_vmdr_kb_qvs,
    upload_vmdr_activity_log,
)

from .gav import upload_gav_hosts

from .cloud_agent import upload_cloud_agents
