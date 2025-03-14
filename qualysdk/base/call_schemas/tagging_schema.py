"""
Tag call schema
"""

from frozendict import frozendict

TAGGING_SCHEMA = frozendict(
    {
        "tagging": {
            "url_type": "api",
            "call_tags_api": {
                "endpoint": "/qps/rest/2.0/{placeholder}/am/tag/{tagId}",
                "method": ["POST", "GET"],
                "valid_params": ["placeholder", "_xml_data", "action", "tagId"],
                "valid_POST_data": ["_xml_data", "tagId"],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": True,
                "auth_type": "basic",
                "_xml_data": False,
            },
        },
    }
)
