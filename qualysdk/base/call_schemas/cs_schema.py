"""
Container security call schemas
"""

from frozendict import frozendict

CS_SCHEMA = frozendict(
    {
        "containersecurity": {
            "url_type": "gateway",
            "list_containers": {
                "endpoint": "/csapi/v1.3/containers/list",
                "method": ["GET"],
                "valid_params": ["filter", "paginationQuery", "limit"],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": True,
                "auth_type": "token",
            },
            "get_container_details": {
                "endpoint": "/csapi/v1.3/containers/{placeholder}",
                "method": ["GET"],
                "valid_params": ["placeholder", "containerSha"],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
        },
    }
)
