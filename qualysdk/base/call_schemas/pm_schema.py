"""
Patch Management call schema
"""

from frozendict import frozendict

PM_SCHEMA = frozendict(
    {
        "pm": {
            "url_type": "gateway",
            "deploymentjobs": {
                "endpoint": "/pm/v1/deploymentjobs{placeholder}",
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
            "deploymentjob": {
                "endpoint": "/pm/v1/deploymentjob{placeholder}",
                "method": ["GET", "POST", "PATCH", "DELETE"],
                "valid_params": ["placeholder"],
                "valid_POST_data": [
                    "placeholder",
                    "deploymentJobId",
                    "jobInstanceId",
                    "pageSize",
                    "sort",
                    "approvedPatches",
                    "assetIds",
                    "assetTagIds",
                    "coAuthorUserIds",
                    "continueOnPatchFailure",
                    "dayOfMonth",
                    "description",
                    "duringDeployment",
                    "dynamicPatchesQQL",
                    "dynamicQQLType",
                    "additionalDynamicPatchesQQL",
                    "additionalDynamicQQLType",
                    "exclusionAssetIds",
                    "exclusionTagIds",
                    "exclusionFilterType",
                    "filterType",
                    "isDynamicPatchesQQL",
                    "matchAllTagIds",
                    "minimizeWindow",
                    "monthlyRecurringType",
                    "name",
                    "notification",
                    "opportunisticDownloads",
                    "patchTuesdayPlusXDays",
                    "platform",
                    "postDeployment",
                    "rebootCountdown",
                    "rebootOption",
                    "suppressReboots",
                    "preDeployment",
                    "recurring",
                    "recurringDayOfMonth",
                    "recurringLastDayOfMonth",
                    "recurringDayOfMonth",
                    "recurringWeekDayOfMonth",
                    "recurringWeekDays",
                    "scheduleType",
                    "startDateTime",
                    "status",
                    "timeout",
                    "timeoutUnit",
                    "downloadRandomizeTime",
                    "downloadRandomizeTimeUnit",
                    "timezone",
                    "timezoneType",
                    "type",
                    "linkedJobId",
                    "linkedJobReferenceCount",
                ],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "vulnerabilities": {
                "endpoint": "/pm/v1/vulnerabilities",
                "method": ["POST"],
                "valid_params": [],
                "valid_POST_data": ["qids"],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "get_version": {
                "endpoint": "/pm/v1/details",
                "method": ["GET"],
                "valid_params": [],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "get_patches": {
                "endpoint": "/pm/v2/patches",
                "method": ["POST"],
                "valid_params": [
                    "pageSize",
                    "platform",
                ],
                "valid_POST_data": [
                    "query",
                    "havingQuery",
                    "attributes",
                ],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": True,
                "auth_type": "token",
            },
            "get_assets": {
                "endpoint": "/pm/v1/assets",
                "method": ["POST"],
                "valid_params": [
                    "pageSize",
                    "platform",
                ],
                "valid_POST_data": [
                    "query",
                    "havingQuery",
                    "attributes",
                ],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": True,
                "auth_type": "token",
            },
            "get_patch_count": {
                "endpoint": "/pm/v1/patches/count",
                "method": ["GET"],
                "valid_params": [
                    "platform",
                    "query",
                    "havingQuery",
                ],
                "valid_POST_data": [],
                "use_requests_json_data": False,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
            "lookup_host_uuids": {
                "endpoint": "/pm/v1/assets/uuids",
                "method": ["POST"],
                "valid_params": [],
                "valid_POST_data": ["assetIds"],
                "use_requests_json_data": True,
                "return_type": "json",
                "pagination": False,
                "auth_type": "token",
            },
        },
    }
)
