"""
Web Application Scanning (WAS) module
"""

from .webapps import (
    count_webapps,
    get_webapps,
    get_webapp_details,
    get_webapps_verbose,
    create_webapp,
    update_webapp,
    delete_webapp,
    purge_webapp,
    get_selenium_script,
)

from .authentication_records import (
    count_authentication_records,
    get_authentication_records,
    get_authentication_record_details,
    get_authentication_records_verbose,
    create_authentication_record,
    delete_authentication_record,
)

from .findings import (
    count_findings,
    get_findings,
    get_finding_details,
    get_findings_verbose,
)

from .scans import (
    count_scans,
    get_scans,
    get_scan_details,
    get_scans_verbose,
    launch_scan,
    cancel_scan,
    get_scan_status,
    scan_again,
    delete_scan,
    get_scan_results,
)
