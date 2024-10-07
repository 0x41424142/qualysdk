"""
Contains the datatype filter mappings for
operators
"""

from tkinter import END


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
    # update_webapp is almost the same as create_webapp. See below
}

ENDPOINT_MAPPINGS["update_webapp"] = ENDPOINT_MAPPINGS["create_webapp"]
ENDPOINT_MAPPINGS["update_webapp"]["webappId"] = "INTEGER"
ENDPOINT_MAPPINGS["update_webapp"]["attributes"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["urlExcludelist"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["urlAllowlist"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["postDataExcludelist"] = "TEXT"
ENDPOINT_MAPPINGS["update_webapp"]["useSitemap"] = "BOOLEAN"
ENDPOINT_MAPPINGS["update_webapp"]["headers"] = "TEXT"

FILTER_MAPPING = {
    "INTEGER": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"],
    "TEXT": ["CONTAINS", "EQUALS", "NOT EQUALS"],
    "DATE": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER"],
    "KEYWORD": ["EQUALS", "NOT EQUALS", "IN"],
    "BOOLEAN": ["EQUALS", "NOT EQUALS"],
}
