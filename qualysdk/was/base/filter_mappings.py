"""
Contains the datatype filter mappings for
operators
"""

ENDPOINT_MAPPINGS = {
    "count_webapps": {
        "id": "INTEGER",
        "name": "TEXT",
        "url": "TEXT",
        "tags_name": "TEXT",
        "tags_id": "INTEGER",
        "createdDate": "DATE",
        "updatedDate": "DATE",
        "isScheduled": "BOOLEAN",
        "isScanned": "BOOLEAN",
        "lastScan_status": "KEYWORD",
        "lastScan_date": "DATE",
    },
    "get_webapps": {
        "id": "INTEGER",
        "name": "TEXT",
        "url": "TEXT",
        "tags_name": "TEXT",
        "tags_id": "INTEGER",
        "createdDate": "DATE",
        "updatedDate": "DATE",
        "isScheduled": "BOOLEAN",
        "isScanned": "BOOLEAN",
        "lastScan_status": "KEYWORD",
        "lastScan_date": "DATE",
        "verbose": "BOOLEAN",
    },
    "get_webapp_details": {},
    "create_webapp": {
        "name": "TEXT",
        "url": "TEXT",
        "authRecord_id": "INTEGER",
        "uris": "TEXT",
        "tag_ids": "TEXT",
        "domains": "TEXT",
        "scannerTag_ids": "TEXT",
    },
    "delete_webapp": {
        "id": "INTEGER",
        "name": "TEXT",
        "url": "TEXT",
        "tags_name": "TEXT",
        "tags_id": "INTEGER",
        "createdDate": "DATE",
        "updatedDate": "DATE",
        "isScheduled": "BOOLEAN",
        "isScanned": "BOOLEAN",
        "lastScan_status": "KEYWORD",
        "lastScan_date": "DATE",
        "removeFromSubscription": "BOOLEAN",
    },
    "get_selenium_script": {
        "id": "INTEGER",
        "crawlingScripts_id": "INTEGER",
    },
    "count_authentication_records": {
        "id": "INTEGER",
        "name": "TEXT",
        "tags": "INTEGER",
        "tags_name": "TEXT",
        "tags_id": "INTEGER",
        "createdDate": "DATE",
        "updatedDate": "DATE",
        "lastScan_date": "DATE",
        "lastScan_authStatus": "KEYWORD",
        "isUsed": "BOOLEAN",
        "contents": "KEYWORD",
    },
    "count_findings": {
        "id": "INTEGER",
        "uniqueId": "TEXT",
        "qid": "INTEGER",
        "name": "TEXT",
        "type": "KEYWORD",
        "url": "TEXT",
        "webApp_tags_id": "INTEGER",
        "webApp_tags_name": "TEXT",
        "status": "KEYWORD",
        "patch": "INTEGER",
        "webApp_id": "INTEGER",
        "webApp_name": "TEXT",
        "severity": "INTEGER",
        "externalRef": "TEXT",
        "ignoredDate": "DATE",
        "ignoredReason": "KEYWORD",
        "group": "KEYWORD",
        "owasp_name": "TEXT",
        "owasp_code": "INTEGER",
        "wasc_name": "TEXT",
        "wasc_code": "INTEGER",
        "cwe_id": "INTEGER",
        "firstDetectedDate": "DATE",
        "lastDetectedDate": "DATE",
        "lastTestedDate": "DATE",
        "timesDetected": "INTEGER",
        "severity_level": "INTEGER",
    },
}

# Build update_webapp with create_webapp as a base:
ENDPOINT_MAPPINGS["update_webapp"] = ENDPOINT_MAPPINGS["create_webapp"]
ENDPOINT_MAPPINGS["update_webapp"]["webappId"] = "INTEGER"
ENDPOINT_MAPPINGS["update_webapp"]["attributes"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["urlExcludelist"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["urlAllowlist"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["postDataExcludelist"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["useSitemap"] = "BOOLEAN"
ENDPOINT_MAPPINGS["update_webapp"]["headers"] = "TEXT"

# get_authentication_records is the same as count_authentication_records:
ENDPOINT_MAPPINGS["get_authentication_records"] = ENDPOINT_MAPPINGS[
    "count_authentication_records"
]

ENDPOINT_MAPPINGS["delete_authentication_record"] = {
    "id": "INTEGER",
    "name": "TEXT",
    "tags": "INTEGER",
    "tags_name": "TEXT",
    "tags_id": "INTEGER",
    "createdDate": "DATE",
    "updatedDate": "DATE",
    "lastScan_date": "DATE",
    "lastScan_authStatus": "KEYWORD",
    "isUsed": "BOOLEAN",
    "contents": "KEYWORD",
}

ENDPOINT_MAPPINGS["get_findings"] = ENDPOINT_MAPPINGS["count_findings"]
ENDPOINT_MAPPINGS["get_findings"]["verbose"] = "BOOLEAN"

# scans:
ENDPOINT_MAPPINGS["count_scans"] = {
    "id": "INTEGER",
    "name": "TEXT",
    "webApp_id": "INTEGER",
    "webApp_name": "TEXT",
    "webApp_tags_id": "INTEGER",
    "reference": "TEXT",
    "type": "KEYWORD",
    "mode": "KEYWORD",
    "status": "KEYWORD",
    "authStatus": "KEYWORD",
    "resultsStatus": "KEYWORD",
    "launchedDate": "DATE",
}

# get_scans is the same as count_scans:
ENDPOINT_MAPPINGS["get_scans"] = ENDPOINT_MAPPINGS["count_scans"]

ENDPOINT_MAPPINGS["launch_scan"] = {
    "name": "TEXT",
    "type": "KEYWORD",
    "web_app_ids": "INTEGER",
    "included_tags_option": "KEYWORD",
    "included_tag_ids": "INTEGER",
    "scanner_appliance_type": "KEYWORD",
    "profile_id": "INTEGER",
    "auth_record_option": "INTEGER",
    "profile_option": "KEYWORD",
    "scanner_option": "INTEGER",
    "send_mail": "BOOLEAN",
    "send_one_mail": "BOOLEAN",
}

ENDPOINT_MAPPINGS["delete_scan"] = {
    "id": "INTEGER",
    "name": "TEXT",
    "webApp_id": "INTEGER",
    "webApp_name": "TEXT",
    "reference": "TEXT",
    "launchedDate": "DATE",
    "type": "KEYWORD",
    "mode": "KEYWORD",
    "status": "KEYWORD",
    "authStatus": "KEYWORD",
    "resultsStatus": "KEYWORD",
}

FILTER_MAPPING = {
    "INTEGER": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"],
    "TEXT": ["CONTAINS", "EQUALS", "NOT EQUALS"],
    "DATE": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER"],
    "KEYWORD": [
        "EQUALS",
        "NOT EQUALS",
        "IN",
        "NONE",
        "NOT_USED",
        "SUCCESSFUL",
        "FAILED",
        "PARTIAL",
        "FORM_STANDARD",
        "FORM_CUSTOM",
        "FORM_SELENIUM",
        "SERVER_BASIC",
        "SERVER_DIGEST",
        "SERVER_NTLM",
        "CERTIFICATE",
        "OAUTH2_AUTH_CODE",
        "OAUTH2_IMPLICIT",
        "OAUTH2_PASSWORD",
        "OAUTH2_CLIENT_CREDS",
        "VULNERABILITY",
        "DISCOVERY",
        "ONDEMAND",
        "SCHEDULED",
        "API",
        "SUBMITTED",
        "RUNNING",
        "ERROR",
        "CANCELLED",
        "PROCESSING",
        "TO_BE_PROCESSED",
        "NO_HOST_ALIVE",
        "NO_WEB_SERVICE",
        "SUCCESSFUL",
        "SERVICE_ERROR",
        "TIME_LIMIT_REACHED",
        "SCAN_INTERNAL_ERROR",
        "SCAN_RESULTS_INVALID",
        "TIME_LIMIT_EXCEEDED",
        "SCAN_NOT_LAUNCHED",
        "SCANNER_NOT_AVAILABLE",
        "CANCELING",
        "DELETED",
        "CANCELED_WITH_RESULTS",
        # launch scan:
        "ALL",
        "ANY",
        "EXTERNAL",
        "INTERNAL",
        "scannerTags",
        "SPECIFIC",
        "DEFAULT",
    ],
    "BOOLEAN": ["EQUALS", "NOT EQUALS"],
}
