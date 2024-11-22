"""
certificate view call schemas
"""

from frozendict import frozendict

CERTVIEW_SCHEMA = frozendict(
    {
        "cert": {
            "url_type": "gateway",
            "list_certs": {
                "endpoint": "/certview/v2/certificates",
                "method": ["POST"],
                "valid_params": [],
                "valid_POST_data": [
                    "certId",
                    "pageSize",
                    "pageNumber",
                    "hash",
                    "validFromDate",
                    "wasUrl",
                    "certificateType",
                ],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": True,
                "auth_type": "token",
            },
        },
    }
)
