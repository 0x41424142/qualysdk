"""
Administration call schema
"""

from frozendict import frozendict

ADMIN_SCHEMA = frozendict(
    {
        "admin": {
            "url_type": "api",
            "get_user_details": {
                "endpoint": "/qps/rest/2.0/get/am/user/{placeholder}",
                "method": ["GET"],
                "valid_params": ["placeholder", "user_id"],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "basic",
                "_xml_data": False,
            },
            "search_users": {
                "endpoint": "/qps/rest/2.0/search/am/user",
                "method": ["POST"],
                "valid_params": [],
                "valid_POST_data": ["user_id", "user_id_operator", "username", "role_name"],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": True,
                "auth_type": "basic",
                "_xml_data": False,
            },
            "update_user": {
                "endpoint": "/qps/rest/2.0/update/am/user/{placeholder}",
                "method": ["POST"],
                "valid_params": ["placeholder", "user_id"],
                "valid_POST_data": [
                    "add_tag_ids",
                    "add_tag_names",
                    "add_role_ids",
                    "add_role_names",
                    "remove_tag_ids",
                    "remove_tag_names",
                    "remove_role_ids",
                    "remove_role_names",
                ],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": False,
                "auth_type": "basic",
                "_xml_data": False,
            },
        },
    }
)
