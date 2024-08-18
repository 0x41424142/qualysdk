"""
assetgroups.py - AG manipulation functions for the Qualys VMDR module.
"""

from typing import *
from urllib.parse import parse_qs, urlparse
from ipaddress import IPv4Address, IPv6Address

from ..auth import BasicAuth
from .data_classes import AssetGroup
from ..base import *


def get_ag_list(
    auth: BasicAuth, page_count: Union["all", int] = "all", **kwargs
) -> list[AssetGroup]:
    """
    Gets a list of asset groups from the Qualys subscription.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.
        page_count (Union["all", int]): The number of pages to retrieve. Defaults to "all". If an integer is passed, that number of pages will be retrieved.

    :Kwargs:
        ```
        action (str): Action to perform on the asset groups. Defaults to "list". WARNING: SDK automatically sets this value to list. It is just included for completeness.
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: SDK automatically sets this value to 0. It is just included for completeness.
        output_format (Literal["csv", "xml"]): The output format of the response. Defaults to "xml". WARNING: SDK automatically sets this value to xml. It is just included for completeness.
        ids (str): The ID of the asset group to get. Defaults to None (all), but can be a single ID or a comma-separated string of IDs.
        id_min (int): The minimum ID of the asset group to get. Defaults to None.
        id_max (int): The maximum ID of the asset group to get. Defaults to None.
        truncation_limit (int): The truncation limit of the asset groups. Defaults to all records. 0 indicates all records. If non-0, the response will be truncated to the specified number of records. Pagination is handled automatically.
        network_ids (str): The network IDs of the asset groups to get. Defaults to None. Can be a single ID or a comma-separated string of IDs. WARNING: This has to be enabled in the Qualys subscription!
        unit_id (str): The unit ID of the asset groups to get. Defaults to None. Must be a single ID.
        user_id (str): The user ID of the asset groups to get. Defaults to None. Must be a single ID.
        title (str): The title of the asset groups to get. Defaults to None. Must be an exact match.
        show_attributes (Union[None, str]): Choose what attributes are returned. Defaults to None (show basic attrs), can be "ALL", "ID", "TITLE", .. For full list, see Qualys documentation: https://cdn2.qualys.com/docs/qualys-api-vmpc-user-guide.pdf
        ```
    Returns:
        BaseList[AssetGroup]: BaseList object containing the AssetGroup objects.
    """

    if type(page_count) in [int, float] and page_count <= 0:
        raise ValueError("page_count must be 'all' or an integer greater than 0.")

    results = BaseList()
    pulled = 0

    while True:
        kwargs["action"] = "list"
        kwargs["echo_request"] = False
        kwargs["output_format"] = "xml"

        # Enforce uppercase for show_attributes:
        if kwargs.get("show_attributes"):
            kwargs["show_attributes"] = kwargs["show_attributes"].upper()

        response = call_api(
            auth=auth,
            module="vmdr",
            endpoint="get_ag_list",
            params=kwargs,
            headers={"X-Requested-With": "qualysdk SDK"},
        )

        if response.status_code == 200:
            data = xml_parser(response.text)["ASSET_GROUP_LIST_OUTPUT"]

            if "ASSET_GROUP" not in data["RESPONSE"]["ASSET_GROUP_LIST"]:
                print("No asset groups found. Returning empty BaseList.")
                break

            # Check if type(data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"]) is dict.
            # If so, put it inside a list to normalize the class instantiation.
            if isinstance(data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"], dict):
                data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"] = [
                    data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"]
                ]

            for ag in data["RESPONSE"]["ASSET_GROUP_LIST"]["ASSET_GROUP"]:
                results.append(AssetGroup(**ag))

            pulled += 1
            # Check page count:
            if page_count != "all" and pulled >= page_count:
                print(f"Page count reached. Returning {pulled} pages.")
                break

            # Check for pagination:
            if data["RESPONSE"].get("WARNING"):
                # Get the id_min param:
                url = data["RESPONSE"]["WARNING"]["URL"]
                parsed_url = urlparse(url)
                id_min = parse_qs(parsed_url.query)["id_min"][0]
                kwargs["id_min"] = id_min
                print(f"Pagination detected. new id_min param: {id_min}")
            else:
                break

    return results


def manage_ag(
    auth: BasicAuth,
    action: Literal["add", "edit", "delete"],
    id: Union[AssetGroup, BaseList, str] = None,
    **kwargs,
) -> str:
    """
    Main function to perform an action on an asset group.

    Gets called by the add_ag, edit_ag, and delete_ag functions.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.
        action (Literal["add", "edit", "delete"]): The action to perform on the asset group.
        id (Union[AssetGroup, BaseList, str]): The ID of the asset group to edit or delete. Defaults to None. If a single AssetGroup, or a BaseList of AssetGroups is passed, the function will iterate over them.

    :Kwargs:
        ```
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: SDK automatically sets this value to 0. It is just included for completeness.

        (WHEN action=="add"):
            title (str): Title of the asset group. Required.
            comments (str): Comments for the asset group.
            division (str): Division of the asset group.
            function (str): Function of the asset group.
            location (str): Location of the asset group.
            business_impact (Literal["critical", "high", "medium", "low", "none"]): Business impact of the asset group.
            ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to add to the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
            appliance_ids (Union[BaseList[int], str]): Appliance IDs to add to the asset group. Comma-separated string, or a BaseList of integers.
            default_appliance_id (int): Default appliance ID for the asset group.
            domains (Union[BaseList[str], str]): Domains to add to the asset group. Comma-separated string, or a BaseList of strings.
            dns_names (Union[BaseList[str], str]): DNS names to add to the asset group. Comma-separated string, or a BaseList of strings.
            netbios_names (Union[BaseList[str], str]): NetBIOS names to add to the asset group. Comma-separated string, or a BaseList of strings.
            cvss_enviro_cdp (Literal["high", "medium-high", "low-medium", "low", "none"]): CVSS environmental CDP for the asset group.
            cvss_enviro_td (Literal["high", "medium", "low", "none"]): CVSS environmental TD for the asset group.
            cvss_enviro_cr (Literal["high", "medium", "low"]): CVSS environmental CR for the asset group.
            cvss_enviro_ir (Literal["high", "medium", "low"]): CVSS environmental IR for the asset group.
            cvss_enviro_ar (Literal["high", "medium", "low"]): CVSS environmental AR for the asset group.

        (WHEN action=="edit"):
            set_comments (str): New comments for the asset group.
            set_division (str): New division for the asset group.
            set_function (str): New function for the asset group.
            set_location (str): New location for the asset group.
            set_business_impact (Literal["critical", "high", "medium", "low", "none"]): New business impact for the asset group.
            add_ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to add to the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
            remove_ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to remove from the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
            set_ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to set for the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
            add_appliance_ids (Union[BaseList[int], str]): Appliance IDs to add to the asset group. Comma-separated string, or a BaseList of integers.
            remove_appliance_ids (Union[BaseList[int], str]): Appliance IDs to remove from the asset group. Comma-separated string, or a BaseList of integers.
            set_appliance_ids (Union[BaseList[int], str]): Appliance IDs to set for the asset group. Comma-separated string, or a BaseList of integers.
            set_default_appliance_id (int): New default appliance ID for the asset group.
            add_domains (Union[BaseList[str], str]): Domains to add to the asset group. Comma-separated string, or a BaseList of strings.
            remove_domains (Union[BaseList[str], str]): Domains to remove from the asset group. Comma-separated string, or a BaseList of strings.
            set_domains (Union[BaseList[str], str]): Domains to set for the asset group. Comma-separated string, or a BaseList of strings.
            add_dns_names (Union[BaseList[str], str]): DNS names to add to the asset group. Comma-separated string, or a BaseList of strings.
            remove_dns_names (Union[BaseList[str], str]): DNS names to remove from the asset group. Comma-separated string, or a BaseList of strings.
            set_dns_names (Union[BaseList[str], str]): DNS names to set for the asset group. Comma-separated string, or a BaseList of strings.
            add_netbios_names (Union[BaseList[str], str]): NetBIOS names to add to the asset group. Comma-separated string, or a BaseList of strings.
            remove_netbios_names (Union[BaseList[str], str]): NetBIOS names to remove from the asset group. Comma-separated string, or a BaseList of strings.
            set_netbios_names (Union[BaseList[str], str]): NetBIOS names to set for the asset group. Comma-separated string, or a BaseList of strings.
            set_title (str): New title for the asset group.
            set_cvss_enviro_cdp (Literal["high", "medium-high", "low-medium", "low", "none"]): New CVSS environmental CDP for the asset group.
            set_cvss_enviro_td (Literal["high", "medium", "low", "none"]): New CVSS environmental TD for the asset group.
            set_cvss_enviro_cr (Literal["high", "medium", "low"]): New CVSS environmental CR for the asset group.
            set_cvss_enviro_ir (Literal["high", "medium", "low"]): New CVSS environmental IR for the asset group.
            set_cvss_enviro_ar (Literal["high", "medium", "low"]): New CVSS environmental AR for the asset group.

        (WHEN action=="delete"):
            A single value in the id parameter.
        ```
    """

    # First, check the action:
    if action not in ["add", "edit", "delete"]:
        raise ValueError("action must be 'add', 'edit', or 'delete'.")

    kwargs["action"] = action

    POSSIBLE_LIST_ARGS = [
        "id",
        "ids",
        "ips",
        "appliance_ids",
        "domains",
        "dns_names",
        "netbios_names",
        "add_ips",
        "remove_ips",
        "set_ips",
        "add_appliance_ids",
        "remove_appliance_ids",
        "set_appliance_ids",
        "add_domains",
        "remove_domains",
        "set_domains",
        "add_dns_names",
        "remove_dns_names",
        "set_dns_names",
        "add_netbios_names",
        "remove_netbios_names",
        "set_netbios_names",
    ]
    POSSIBLE_IP_OBJ_ARGS = ["ips", "add_ips", "remove_ips", "set_ips"]

    # Look for single IP objects and convert them to strings:
    for arg in POSSIBLE_IP_OBJ_ARGS:
        if arg in kwargs and any(
            isinstance(kwargs[arg], obj) for obj in [IPv4Address, IPv6Address]
        ):
            kwargs[arg] = str(kwargs[arg])

    # Check if any list args are passed.
    # If so, convert them to comma-separated strings:
    for arg in POSSIBLE_LIST_ARGS:
        if arg in kwargs:
            if isinstance(kwargs[arg], BaseList):
                kwargs[arg] = [str(item) for item in kwargs[arg]]
                kwargs[arg] = ",".join(kwargs[arg])

    # Check if id is a single AssetGroup object:
    if isinstance(id, AssetGroup):
        id = id.id

    # Check if id is a BaseList object:
    if isinstance(id, BaseList):
        id = [str(ag.id) for ag in id]
        id = ",".join(id)

    if id:
        kwargs["id"] = id

    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="manage_ag",
        payload=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    result = xml_parser(response.text)["SIMPLE_RETURN"]["RESPONSE"]["TEXT"]

    return result


def add_ag(auth: BasicAuth, title: str, **kwargs) -> str:
    """
    Adds an asset group to the Qualys subscription.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.
        title (str): Title of the asset group.

    :Kwargs:
        ```
        comments (str): Comments for the asset group.
        division (str): Division of the asset group.
        function (str): Function of the asset group.
        location (str): Location of the asset group.
        business_impact (Literal["critical", "high", "medium", "low", "none"]): Business impact of the asset group.
        ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to add to the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
        appliance_ids (Union[BaseList[int], str]): Appliance IDs to add to the asset group. Comma-separated string, or a BaseList of integers.
        default_appliance_id (int): Default appliance ID for the asset group.
        domains (Union[BaseList[str], str]): Domains to add to the asset group. Comma-separated string, or a BaseList of strings.
        dns_names (Union[BaseList[str], str]): DNS names to add to the asset group. Comma-separated string, or a BaseList of strings.
        netbios_names (Union[BaseList[str], str]): NetBIOS names to add to the asset group. Comma-separated string, or a BaseList of strings.
        cvss_enviro_cdp (Literal["high", "medium-high", "low-medium", "low", "none"]): CVSS environmental CDP for the asset group.
        cvss_enviro_td (Literal["high", "medium", "low", "none"]): CVSS environmental TD for the asset group.
        cvss_enviro_cr (Literal["high", "medium", "low"]): CVSS environmental CR for the asset group.
        cvss_enviro_ir (Literal["high", "medium", "low"]): CVSS environmental IR for the asset group.
        cvss_enviro_ar (Literal["high", "medium", "low"]): CVSS environmental AR for the asset group.
        ```
    Returns:
        str: Response text from the Qualys API.
    """

    return manage_ag(auth, action="add", title=title, **kwargs)


def edit_ag(auth: BasicAuth, id: Union[AssetGroup, BaseList, str], **kwargs) -> str:
    """
    Edits an asset group in the Qualys subscription.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.
        id (Union[AssetGroup, BaseList, str]): The ID of the asset group to edit. If a single AssetGroup, or a BaseList of AssetGroups is passed, the function will iterate over them.

    :Kwargs:
        ```
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: SDK automatically sets this value to 0. It is just included for completeness.
        set_comments (str): New comments for the asset group.
        set_division (str): New division for the asset group.
        set_function (str): New function for the asset group.
        set_location (str): New location for the asset group.
        set_business_impact (Literal["critical", "high", "medium", "low", "none"]): New business impact for the asset group.
        add_ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to add to the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
        remove_ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to remove from the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
        set_ips (Union[str, ipaddress.IPVxAddress, BaseList[ipaddress.IPVxAddress]]): IP addresses to set for the asset group. Comma-separated string, a single ipaddress.IPvxAddress, or a BaseList of ipaddress.IPvxAddress.
        add_appliance_ids (Union[BaseList[int], str]): Appliance IDs to add to the asset group. Comma-separated string, or a BaseList of integers.
        remove_appliance_ids (Union[BaseList[int], str]): Appliance IDs to remove from the asset group. Comma-separated string, or a BaseList of integers.
        set_appliance_ids (Union[BaseList[int], str]): Appliance IDs to set for the asset group. Comma-separated string, or a BaseList of integers.
        set_default_appliance_id (int): New default appliance ID for the asset group.
        add_domains (Union[BaseList[str], str]): Domains to add to the asset group. Comma-separated string, or a BaseList of strings.
        remove_domains (Union[BaseList[str], str]): Domains to remove from the asset group. Comma-separated string, or a BaseList of strings.
        set_domains (Union[BaseList[str], str]): Domains to set for the asset group. Comma-separated string, or a BaseList of strings.
        add_dns_names (Union[BaseList[str], str]): DNS names to add to the asset group. Comma-separated string, or a BaseList of strings.
        remove_dns_names (Union[BaseList[str], str]): DNS names to remove from the asset group. Comma-separated string, or a BaseList of strings.
        set_dns_names (Union[BaseList[str], str]): DNS names to set for the asset group. Comma-separated string, or a BaseList of strings.
        add_netbios_names (Union[BaseList[str], str]): NetBIOS names to add to the asset group. Comma-separated string, or a BaseList of strings.
        remove_netbios_names (Union[BaseList[str], str]): NetBIOS names to remove from the asset group. Comma-separated string, or a BaseList of strings.
        set_netbios_names (Union[BaseList[str], str]): NetBIOS names to set for the asset group. Comma-separated string, or a BaseList of strings.
        set_title (str): New title for the asset group.
        set_cvss_enviro_cdp (Literal["high", "medium-high", "low-medium", "low", "none"]): New CVSS environmental CDP for the asset group.
        set_cvss_enviro_td (Literal["high", "medium", "low", "none"]): New CVSS environmental TD for the asset group.
        set_cvss_enviro_cr (Literal["high", "medium", "low"]): New CVSS environmental CR for the asset group.
        set_cvss_enviro_ir (Literal["high", "medium", "low"]): New CVSS environmental IR for the asset group.
        set_cvss_enviro_ar (Literal["high", "medium", "low"]): New CVSS environmental AR for the asset group.
        ```
    Returns:
        str: Response text from the Qualys API.
    """

    return manage_ag(auth, action="edit", id=id, **kwargs)


def delete_ag(auth: BasicAuth, id: Union[AssetGroup, str]) -> str:
    """
    Deletes a single asset group from the Qualys subscription.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.
        id (Union[AssetGroup, str]): The ID of the asset group to delete.

    Returns:
        str: Response text from the Qualys API.
    """

    return manage_ag(auth, action="delete", id=id)
