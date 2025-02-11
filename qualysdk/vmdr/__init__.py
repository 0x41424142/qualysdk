"""
VMDR (Vulnerability Management) module

This module contains ways to interact with the Qualys VMDR API. Valid endpoints are defined in the CALL_SCHEMA dictionary.

VMDR QQL Syntax help: https://qualysguard.qg2.apps.qualys.com/portal-help/en/vm/search/how_to_search.htm
"""

from .query_kb import query_kb, get_kb_qvs
from .get_host_list import get_host_list
from .get_host_list_detections import get_hld, get_cve_hld
from .ips import get_ip_list, add_ips, update_ips
from .assetgroups import get_ag_list, add_ag, edit_ag, delete_ag
from .vmscans import (
    get_scan_list,
    launch_scan,
    pause_scan,
    resume_scan,
    cancel_scan,
    fetch_scan,
    delete_scan,
)
from .scanner_appliances import get_scanner_list
from .searchlists import get_static_searchlists, get_dynamic_searchlists
from .reports import (
    get_report_list,
    get_template_list,
    launch_report,
    cancel_report,
    fetch_report,
    delete_report,
    get_scheduled_report_list,
    launch_scheduled_report,
)

from .users import get_user_list, add_user, edit_user
from .activity_log import get_activity_log
from .purge import purge_hosts
