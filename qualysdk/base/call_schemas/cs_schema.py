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
            "get_software_on_container": {
                "endpoint": "/csapi/v1.3/containers/{placeholder}/software",
                "method": ["GET"],
                "valid_params": [
                    "placeholder",
                    "containerSha",
                    "filter",
                    "sort",
                    "isDrift",
                ],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "get_container_vuln_count": {
                "endpoint": "/csapi/v1.3/containers/{placeholder}/vuln/count",
                "method": ["GET"],
                "valid_params": ["placeholder", "containerSha"],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "get_container_vulns": {
                "endpoint": "/csapi/v1.3/containers/{placeholder}/vuln",
                "method": ["GET"],
                "valid_params": [
                    "placeholder",
                    "containerSha",
                    "filter",
                    "type",
                    "isDrift",
                ],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
        },
    }
)
