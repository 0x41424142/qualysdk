"""
Code to generate XML service requests to Qualys WAS API
"""

from html import unescape
from datetime import datetime

import xmltodict

from ..base.web_app_service_requests import format_xml_list


def build_scan_service_request(
    **kwargs,
) -> dict[str, str]:
    """
    Build the XML request to launch a WAS scan.

    Args:
        kwargs: The keyword arguments to build the request.

    Returns:
        dict: The XML payload to be sent to the Qualys API.
    """

    request_dict = {
        "ServiceRequest": {
            "data": {
                "WasScan": {
                    "name": kwargs.get("name", f"New WAS Scan - {datetime.now()}"),
                    "type": kwargs.get("type", "DISCOVERY"),
                    "target": {
                        "scannerAppliance": {
                            "type": kwargs.get("scanner.appliance.type", "EXTERNAL"),
                        },
                        "webApps": {
                            "set": {
                                "WebApp": format_xml_list(
                                    kwargs.get("web.app.ids", []), "id"
                                ),
                            },
                        }
                        if kwargs.get("web.app.ids")
                        else None,
                        "profileOption": kwargs.get("profile.option", "DEFAULT"),
                        "tags": {
                            "included": {
                                "option": kwargs.get("included.tags.option", "ALL"),
                                "tagList": {
                                    "set": format_xml_list(
                                        kwargs.get("included.tag.ids", []), "Tag"
                                    )
                                },
                            },
                        }
                        if kwargs.get("included.tag.ids")
                        else None,
                        "scannerOption": kwargs.get("scanner.option", "DEFAULT"),
                        "cancelOption": kwargs.get("cancel.option", "DEFAULT"),
                        "authRecordOption": kwargs.get("auth.record.option", "NONE"),
                    },
                    "profile": {"id": kwargs.get("profile.id")},
                    "sendMail": kwargs.get("send.mail", False),
                    "sendOneMail": kwargs.get("send.one.mail", False),
                }
            }
        }
    }

    if not request_dict["ServiceRequest"]["data"]["WasScan"]["target"]["webApps"]:
        request_dict["ServiceRequest"]["data"]["WasScan"]["target"].pop("webApps")
    if not request_dict["ServiceRequest"]["data"]["WasScan"]["target"]["tags"]:
        request_dict["ServiceRequest"]["data"]["WasScan"]["target"].pop("tags")

    # Unescape any HTML. Necessary due to xmltodict's behavior.
    try:
        xml = unescape(xmltodict.unparse(request_dict, pretty=True))
        payload = {"_xml_data": xml}
    except Exception as e:
        raise ValueError(f"Error unescaping XML: {e}")

    return payload
