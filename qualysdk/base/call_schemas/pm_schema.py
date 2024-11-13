"""
Patch Management call schema
"""

from frozendict import frozendict

PM_SCHEMA = frozendict(
    {
        "pm": {
            "url_type": "gateway",
            "deploymentjobs": {
                "endpoint": "/pm/v1/deploymentjobs/{placeholder}",
                "method": ["GET", "POST", "PATCH", "DELETE"],
                "valid_params": [
                    "placeholder",
                    "filter",
                    "attributes",
                    "platform",
                    "coauthorJob",
                    "ownedJob",
                    "pageNumber",
                    "pageSize",
                    "sort",
                ],
                "valid_POST_data": ["placeholder"],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": True,
                "auth_type": "token",
            },
        },
    }
)