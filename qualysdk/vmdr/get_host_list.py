"""
get_host_list.py - call the VMDR host list API.
"""

from typing import Union

# from xmltodict import parse
from urllib.parse import urlparse, parse_qs

from ..base.call_api import call_api
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.hosts import VMDRHost, VMDRID
from ..base.base_list import BaseList
from ..base import xml_parser


def get_host_list(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> list:
    """
    Get the host list from the VMDR API.
    For a full list of parameters, see the Qualys API documentation: [Qualys API VMPc User Guide](https://cdn2.qualys.com/docs/qualys-api-vmpc-user-guide.pdf)

    Parameters:
        auth (BasicAuth): The authentication object.
        page_count (Union[int, "all"]): The number of pages to get. If "all", get all pages. Defaults to "all".

    :Kwargs:

        action (Optional[str]): The action to perform. Default is 'list'. WARNING: any value you pass is overwritten with 'list'. It is just recognized as valid for the sake of completeness.
        echo_request (Optional[bool]): Whether to show the request. Default is 'False'. ends up being passed to API as 0 or 1.
        show_asset_id (Optional[bool]): Whether to show the asset IDs. Default is 'False'. ends up being passed to API as 0 or 1.
        details (Optional[Union[Literal["Basic", "Basic/AGs", "All", "All/AGs", "None"], None]]): The level of detail to return. Default is 'Basic'. Basic includes host ID, IP, tracking method, DNS, netBIOS, and OS. Basic/AGs includes basic host information plus asset group information. Asset group information includes the asset group ID and title. All shows all basic host information plus last vulnerability and compliance scan dates. All/AGs includes all information plus asset group information: group ID and title. None shows only the host ID (or asset ID if show_asset_id is set to 1 (True)).
        os_pattern (Optional[str]): The OS regex pattern to search for. It follows the PCRE standard, and must be URL-encoded. To match an empty string, use '%5E%24'.
        truncation_limit (Optional[int]): The maximum number of characters to return for each field. Default is 1000, and can be set to 0 for no truncation all the way up to 1,000,000. Past 1M, the API will return an error.
        ips (Optional[str]): Only show assets with certain IP addresses/ranges. Multiple values specified as a comma-separated string. A range is specified with a hyphen. Example: 10.0.0.1-10.0.0.255
        ipv6 (Optional[str]): Only show assets with certain IPv6 addresses/ranges. Multiple values specified as a comma-separated string.
        ag_ids (Optional[str]): Only show assets in certain asset group IDs. Multiple values specified as a comma-separated string. A range is specified with a hyphen. Example: 1-5. A valid ID is required or the API will return an error.
        ag_titles (Optional[str]): Only show assets with specified string in the asset group title. Multiple values specified as a comma-separated string.
        ids (Optional[str]): Only show assets with certain asset IDs. Multiple values specified as a comma-separated string. A range is specified with a hyphen. Example: 1-5. A valid ID is required or the API will return an error.
        id_min (Optional[int]): Only show assets with asset IDs greater than or equal to this value.
        id_max (Optional[int]): Only show assets with asset IDs less than or equal to this value.
        network_ids (Optional[str]): Valid only when the Network Support feature is enabled for the users account). Restrict the request to certain custom network IDs. Multiple network IDs are comma separated.
        compliance_enabled (Optional[bool]): Only show assets with compliance enabled. Default is 'False'. ends up being passed to API as 0 or 1.

        DATE PARAMS

        no_vm_scan_since (Optional[str]): Only show assets that have not been scanned since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        no_compliance_scan_since (Optional[str]): Only show assets that have not had a compliance scan since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_scan_since (Optional[str]): Only show assets that have been scanned since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        compliance_scan_since (Optional[str]): Only show assets that have had a compliance scan since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_processed_before (Optional[str]): Only show assets that have been processed by the VM module before this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_processed_after (Optional[str]): Only show assets that have been processed by the VM module after this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_scan_date_before (Optional[str]): Only show assets that have been scanned by the VM module before this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_scan_date_after (Optional[str]): Only show assets that have been scanned by the VM module after this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_auth_scan_date_before (Optional[str]): Only show assets that have been authenticated scanned by the VM module before this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        vm_auth_scan_date_after (Optional[str]): Only show assets that have been authenticated scanned by the VM module after this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        scap_scan_since (Optional[str]): Only show assets that have been scanned by the SCAP module since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        no_scap_scan_since (Optional[str]): Only show assets that have not been scanned by the SCAP module since this date. Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.

        TAG PARAMS

        use_tags (bool): Whether to use tags. Default is 'False'. ends up being passed to API as 0 or 1.
        tag_set_by (Optional[Literal["id","name"]]): search for tags by ID or name. Default is 'id'.
        tag_include_selector (Optional[Literal["any","all"]]): Specified tags will be included if any or all are matched. Default is 'any'. Only valid if use_tags is set to 1 (True).
        tag_exclude_selector (Optional[Literal["any","all"]]): Specified tags will be excluded if any or all are matched. Default is 'any'. Only valid if use_tags is set to 1 (True).
        tag_set_include (Optional[str]): Only show assets with tags that match this string. Multiple values specified as a comma-separated string. Only valid if use_tags is set to 1 (True).
        tag_set_exclude (Optional[str]): Only show assets with tags that do not match this string. Multiple values specified as a comma-separated string. Only valid if use_tags is set to 1 (True).
        show_tags (Optional[bool]): Whether to show tags. Default is 'False'. ends up being passed to API as 0 or 1.

        ARS (Asset Risk Score) PARAMS

        show_ars (Optional[bool]): Whether to show the ARS. Default is 'False'. ends up being passed to API as 0 or 1.
        ars_min (Optional[int]): Only show assets with an ARS greater than or equal to this value.
        ars_max (Optional[int]): Only show assets with an ARS less than or equal to this value.
        show_ars_factors (Optional[bool]): Whether to show the ARS factors. Default is 'False'. ends up being passed to API as 0 or 1.

        TRURISK PARAMS

        show_trurisk (Optional[bool]): Whether to show the TruRisk. Default is 'False'. ends up being passed to API as 0 or 1.
        trurisk_min (Optional[int]): Only show assets with a TruRisk greater than or equal to this value.
        trurisk_max (Optional[int]): Only show assets with a TruRisk less than or equal to this value.
        show_trurisk_factors (Optional[bool]): Whether to show the TruRisk factors. Default is 'False'. ends up being passed to API as 0 or 1.

        CLOUD HOST PARAMS

        host_metadata (Optional[Literal["all", "ec2", "azure", "google"]]): Specify all to list all cloud and non-cloud assets. Specify a service to just get cloud assets for that service plus non-cloud assets.
        host_metadata_fields (Optional[str]): Specify the fields to return for cloud assets. Multiple values specified as a comma-separated string. Only valid if host_metadata is set to a cloud service.
        show_cloud_tags (Optional[bool]): Whether to show cloud tags. Default is 'False'. ends up being passed to API as 0 or 1.
        cloud_tag_fields (Optional[str]): Specify the cloud tag name and value, separated by a colon. Multiple values specified as a comma-separated string. If this is not specified and show_cloud_tags is 1, all tags are returned.

    Returns:

        list[Union[VMDRHost, VMDRID]]: A list of VMDRHost or VMDRID objects.
    """

    responses = BaseList()
    pulled = 0

    # add the action to the kwargs:
    kwargs["action"] = "list"

    if kwargs.get("truncation_limit") and (
        kwargs["truncation_limit"] in [0, "0"]
        and kwargs["details"] not in ["None", None]
    ):
        print(
            "[!] Warning: You have specified to pull all data with no pagination. This is generally not recommended, as it uses lots of resources and take a long time to complete. Please consider specifying a page_count or truncation_limit to avoid this issue."
        )

    while True:
        # make the request:
        response = call_api(
            auth=auth,
            module="vmdr",
            endpoint="get_host_list",
            params=kwargs,
            headers={"X-Requested-With": "qualysdk SDK"},
        )
        if response.status_code != 200:
            print("No data returned.")
            return responses

        xml = xml_parser(response.content)

        if (
            "HOST_LIST" not in xml["HOST_LIST_OUTPUT"]["RESPONSE"]
            and "ID_SET" not in xml["HOST_LIST_OUTPUT"]["RESPONSE"]
        ):
            print("No host list returned.")
            return

        # If details is none, ID_SET will be returned instead of HOST_LIST
        if "ID_SET" in xml["HOST_LIST_OUTPUT"]["RESPONSE"]:
            # check if ID_SET is a list of dicts or a single dict:
            if isinstance(xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"], dict):
                # if it's a single dict, convert it to a list of dicts:
                xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"] = [
                    xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"]
                ]

            for ID in xml["HOST_LIST_OUTPUT"]["RESPONSE"]["ID_SET"]["ID"]:
                # create a VMDRID object and append to responses
                # This code will only run if details=None, so now we just need to check if show_asset_id is set to 1:
                if kwargs.get("show_asset_id"):
                    responses.append(VMDRID(ID=ID, TYPE="asset"))
                else:  # elif not kwargs.get("show_asset_id"):
                    responses.append(VMDRID(ID=ID, TYPE="host"))
        else:
            # HOST_LIST will be returned
            # first, check if xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"]
            # is a list of dicts or a single dict:
            if isinstance(
                xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"], dict
            ):
                # if it's a single dict, convert it to a list of dicts:
                xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"] = [
                    xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"]
                ]

            for host in xml["HOST_LIST_OUTPUT"]["RESPONSE"]["HOST_LIST"]["HOST"]:
                # return a list of VMDRHost objects
                responses.append(VMDRHost.from_dict(host))

        pulled += 1

        if page_count != "all" and pulled >= page_count:
            print("Page count reached.")
            break

        if "WARNING" in xml["HOST_LIST_OUTPUT"]["RESPONSE"]:
            if "URL" in xml["HOST_LIST_OUTPUT"]["RESPONSE"]["WARNING"]:
                print(
                    f"Pagination detected. Pulling next page from url: {xml['HOST_LIST_OUTPUT']['RESPONSE']['WARNING']['URL']}"
                )
                # get the id_min parameter from the URL to pass into kwargs:
                params = parse_qs(
                    urlparse(
                        xml["HOST_LIST_OUTPUT"]["RESPONSE"]["WARNING"]["URL"]
                    ).query
                )
                kwargs["id_min"] = params["id_min"][0]

            else:
                break
        else:
            break

    return responses
