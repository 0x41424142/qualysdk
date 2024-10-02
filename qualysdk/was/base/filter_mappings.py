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
}

FILTER_MAPPING = {
    "INTEGER": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"],
    "TEXT": ["CONTAINS", "EQUALS", "NOT EQUALS"],
    "DATE": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER"],
    "KEYWORD": ["EQUALS", "NOT EQUALS", "IN"],
    "BOOLEAN": ["EQUALS", "NOT EQUALS"],
}
