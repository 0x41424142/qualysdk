"""
Cloud Agent API call schema
"""

from frozendict import frozendict

CLOUDAGENT_SCHEMA = frozendict(
    {
        "cloud_agent": {
            "url_type": "api",
            "purge_agent": {
                "endpoint": "/qps/rest/2.0/uninstall/am/asset/{placeholder}",  # assetId
                "method": ["POST"],
                "valid_params": [],
                "valid_POST_data": ["placeholder", "_xml_data"],
                "use_requests_json_data": False,
                "return_type": "xml",
                "pagination": False,
                "auth_type": "basic",
                "_xml_data": True,
            },
            "bulk_purge_agent": {
                "endpoint": "/qps/rest/2.0/uninstall/am/asset",
                "method": ["POST"],
                "valid_params": [],
                "valid_POST_data": ["_xml_data"],
                "use_requests_json_data": False,
                "return_type": "xml",
                "pagination": False,
                "auth_type": "basic",
                "_xml_data": True,
            },
            "list_agents": {
                "endpoint": "/qps/rest/2.0/search/am/hostasset",
                "method": ["POST"],
                "valid_params": [],
                "valid_POST_data": ["_xml_data"],
                "use_requests_json_data": False,
                "return_type": "xml",
                "pagination": True,
                "auth_type": "basic",
                "_xml_data": True,
            },
            "launch_ods": {
                "endpoint": "/qps/rest/1.0/ods/ca/agentasset/{placeholder}",
                "method": ["POST"],
                "valid_params": ["scan", "overrideConfigCpu"],
                "valid_POST_data": ["placeholder", "_xml_data"],
                "use_requests_json_data": False,
                "return_type": "xml",
                "pagination": False,
                "auth_type": "basic",
                "_xml_data": True,
            },
            "bulk_launch_ods": {
                "endpoint": "/qps/rest/1.0/ods/ca/agentasset",
                "method": ["POST"],
                "valid_params": ["scan", "overrideConfigCpu"],
                "valid_POST_data": ["_xml_data"],
                "use_requests_json_data": False,
                "return_type": "xml",
                "pagination": False,
                "auth_type": "basic",
                "_xml_data": True,
            },
        },
    }
)
