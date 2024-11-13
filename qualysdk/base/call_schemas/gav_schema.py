"""
Global AssetView call schema
"""

from frozendict import frozendict

GAV_SCHEMA = frozendict(
    {
        "gav": {
            "url_type": "gateway",
            "count_assets": {
                "endpoint": "/am/v1/assets/host/count",
                "method": ["POST"],
                "valid_params": ["filter", "lastSeenAssetId", "lastModifiedDate"],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "get_all_assets": {
                "endpoint": "/am/v1/assets/host/list",
                "method": ["POST"],
                "valid_params": [
                    "excludeFields",
                    "includeFields",
                    "lastModifiedDate",
                    "lastSeenAssetId",
                    "pageSize",
                ],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": True,
                "auth_type": "token",
            },
            "get_asset": {
                "endpoint": "/am/v1/asset/host/id",
                "method": ["POST"],
                "valid_params": ["excludeFields", "includeFields", "assetId"],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "query_assets": {
                "endpoint": "/am/v1/assets/host/filter/list",
                "method": ["POST"],
                "valid_params": [
                    "filter",
                    "excludeFields",
                    "includeFields",
                    "lastModifiedDate",
                    "lastSeenAssetId",
                    "pageSize",
                ],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": True,
                "auth_type": "token",
            },
        },
    }
)
