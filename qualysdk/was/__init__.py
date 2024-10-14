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
)
