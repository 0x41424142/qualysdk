"""
Contains the lookups for tagging module's kwargs
"""

ENDPOINT_MAPPINGS = {
    "count_tags": {
        "id": "INTEGER",
        "name": "TEXT",
        "parent": "INTEGER",
        "ruleType": "KEYWORD",
        "provider": "KEYWORD",
        "color": "TEXT",
    },
}

# search/get tags takes the same kwargs as count_tags:
ENDPOINT_MAPPINGS["get_tags"] = ENDPOINT_MAPPINGS["count_tags"]


FILTER_MAPPING = {
    "INTEGER": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER", "IN"],
    "TEXT": ["CONTAINS", "EQUALS", "NOT EQUALS"],
    "DATE": ["EQUALS", "NOT EQUALS", "GREATER", "LESSER"],
    "KEYWORD": [
        "EQUALS",
        "NOT EQUALS",
        "IN",
        "EC2",
        "AZURE",
        "GCP",
        "IBM",
        "OCI",
        "STATIC",
        "GROOVY",
        "OS_REGEX",
        "NETWORK_RANGE",
        "NAME_CONTAINS",
        "INSTALLED_SOFTWARE",
        "OPEN_PORTS",
        "VULN_EXIST",
        "ASSET_SEARCH",
        "CLOUD_ASSET",
        "NETWORK_TAG",
        "NETWORK",
        "NETWORK_RANGE_ENHANCED",
        "CLOUD_ASSET",
        "GLOBAL_ASSET_VIEW",
        "TAGSET",
        "BUSINESS_INFORMATION",
        "VULN_DETECTION",
    ],
    "BOOLEAN": ["EQUALS", "NOT EQUALS"],
}


def validate_kwargs(endpoint: str, **kwargs):
    """
    Validate the kwargs for the given endpoint

    Args:
        endpoint (str): The endpoint to validate the kwargs for
        **kwargs: The kwargs to validate
    """
    if endpoint not in ENDPOINT_MAPPINGS:
        raise ValueError(
            f"Invalid endpoint: {endpoint}. Must be one of {ENDPOINT_MAPPINGS.keys()}"
        )

    for key, value in kwargs.items():
        if key.endswith("_operator"):
            continue
        if key not in ENDPOINT_MAPPINGS[endpoint]:
            raise ValueError(
                f"Invalid key: {key}. Must be one of {ENDPOINT_MAPPINGS[endpoint].keys()}"
            )
