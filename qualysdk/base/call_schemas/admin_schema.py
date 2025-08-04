"""
Administration call schema
"""

from frozendict import frozendict

ADMIN_SCHEMA = frozendict(
    {
        "admin": {
            "url_type": "api",
            "get_user_id": {
                "endpoint": "/qps/rest/2.0/get/am/user/{placeholder}",
                "method": ["GET"],
                "valid_params": ["placeholder", "user_id"],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "xml",
                "pagination": False,
                "auth_type": "basic",
                "_xml_data": False,
            },
        },
    }
)
