"""
purge.py - Contains the user-facing functions to purge data from the VMDR module.
"""

from typing import Union, Literal
from datetime import datetime

from ..base.base_list import BaseList
from ..auth.basic import BasicAuth
from ..base.call_api import call_api
from ..base.xml_parser import xml_parser


def purge_hosts(
    auth: BasicAuth, data_scope: Literal["vm", "pc", "vm,pc"] = "vm,pc", **kwargs
) -> str:
    """Purge host data from VMDR/PC.

    Args:
        auth (BasicAuth): The BasicAuth object.
        data_scope (Literal['vm', 'pc', 'vm,pc']): The data scope to purge. Default: 'vm,pc'.
        **kwargs: Arbitrary keyword arguments.

    ## Kwargs:

    - `ids` (str): The host IDs to purge as a comma-separated string.
    - `ips` (str): The IPs to purge as a comma-separated string. A range can be specified with a hyphen.
    - `ag_ids` (str): The asset group IDs to purge as a comma-separated string.
    - `ag_titles` (str): The asset group titles to purge as a comma-separated string.
    - `network_ids` (str): The network IDs to purge as a comma-separated string. ⚠️ ONLY VALID IF NETWORK SUPPORT IS ENABLED IN YOUR SUBSCRIPTION.
    - `no_vm_scan_since` (Union[str, datetime]): Purge hosts that have not been scanned since this datetime. Format: YYYYMM-DD[THH:MM:SSZ]
    - `no_compliance_scan_since` (Union[str, datetime]): Purge hosts that have not been scanned for compliance since this datetime. Format: YYYYMM-DD[THH:MM:SSZ]
    - `compliance_enabled` (bool): Filter hosts by compliance_enabled.
    - `os_pattern` (str): Filter hosts by a URL-encoded, PCRE-compatible regular expression pattern.

    Returns:
        str: The response from the API.
    """

    # Force-set certain kwargs:
    kwargs["action"] = "purge"
    kwargs["echo_request"] = False
    kwargs["data_scope"] = data_scope

    # If no_<scan_type>_scan_since is a datetime object, convert it to a str:
    if kwargs.get("no_vm_scan_since"):
        kwargs["no_vm_scan_since"] = kwargs["no_vm_scan_since"].strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    if kwargs.get("no_compliance_scan_since"):
        kwargs["no_compliance_scan_since"] = kwargs[
            "no_compliance_scan_since"
        ].strftime("%Y-%m-%dT%H:%M:%SZ")

    # if data_scope is specified, play it safe and lowercase it:
    if kwargs.get("data_scope"):
        kwargs["data_scope"] = kwargs["data_scope"].lower()

    # Call the API:
    result = call_api(
        module="vmdr",
        endpoint="purge_hosts",
        headers={"X-Requested-With": "Qualysdk SDK"},
        auth=auth,
        params=kwargs,
    )

    data = xml_parser(result.text)

    if isinstance(data["BATCH_RETURN"]["RESPONSE"]["BATCH_LIST"].get("BATCH"), list):
        return str(data["BATCH_RETURN"]["RESPONSE"]["BATCH_LIST"]["BATCH"])

    return data["BATCH_RETURN"]["RESPONSE"]["BATCH_LIST"]["BATCH"]["TEXT"]
