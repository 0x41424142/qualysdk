"""
ips.py - IP address manipulation from Qualys subscription and stores them in a BaseList object.
"""

from typing import Union

from ..base.call_api import call_api
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.ip_converters import convert_ips, convert_ranges
from ..base.base_list import BaseList
from ..base import xml_parser


def get_ip_list(auth: BasicAuth, **kwargs) -> BaseList:
    """
    Gets a list of IP addresses from the Qualys subscription.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.

    ## Kwargs:

        action (str): Action to perform on the IP addresses. Defaults to "list". WARNING: SDK automatically sets this value. It is just included for completeness.
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: SDK automatically sets this value. It is just included for completeness.
        ips (str): Show only certain IP addresses/ranges. One or more IPs/ranges may be specified. Multiple entries are comma separated. A host IP range is specified with a hyphen (for example, 10.10.10.44-10.10.10.90).
        network_id (Union[str, int]): Network ID to filter on. Defaults to None. NOTE: This has to be enabled in the Qualys subscription!
        tracking_method (Literal[None, "IP", "DNS", "NETBIOS"]): Tracking method to filter on. Defaults to None. Valid values are IP, DNS, NETBIOS.
        compliance_enabled (Union[str, bool]): Whether to filter to IPs within the compliance module. Defaults to None.
        certview_enabled (Union[str, bool]): Whether to filter to IPs within certview module. Defaults to None.

    Returns:
        BaseList: BaseList object containing the IP addresses/ranges.
    """
    ip_list = BaseList()

    kwargs["action"] = "list"
    kwargs["echo_request"] = False

    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="get_ip_list",
        params=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    if response.status_code == 200:
        data = xml_parser(response.text)["IP_LIST_OUTPUT"]

        if "IP_SET" not in data["RESPONSE"]:
            print("No IP addresses found. Returning empty BaseList.")
            return ip_list

        data = data["RESPONSE"][
            "IP_SET"
        ]  # at this point, data has IP and IP_RANGE keys

        # Convert the IP addresses into IP objects:
        if "IP" in data:
            # Normalize, account for a str:
            if isinstance(data["IP"], str):
                data["IP"] = [data["IP"]]
            single_ips = [ip for ip in data["IP"]]  # Single IPs
            ip_list.extend(convert_ips(single_ips))

        # Convert the IP ranges into IPNetwork objects:
        if "IP_RANGE" in data:
            # Normalize, account for a str:
            if isinstance(data["IP_RANGE"], str):
                data["IP_RANGE"] = [data["IP_RANGE"]]
            range_ips = [ip for ip in data["IP_RANGE"]]  # IP Ranges
            ip_list.extend(convert_ranges(range_ips))

    else:
        raise Exception(f"Failed to pull IP list. Status code: {response.status_code}")

    return ip_list


def add_ips(
    auth: BasicAuth,
    ips: Union[str, BaseList],
    enable_pc: Union[bool, int] = False,
    enable_vm: Union[bool, int] = True,
    enable_sca: Union[bool, int] = False,
    **kwargs,
) -> None:
    """
    Adds IP addresses to the Qualys subscription.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.
        ips (Union[str, BaseList): List of IP addresses/ranges to add. Can be a string or a BaseList object containing IPs. Multiple entries are comma separated. A host IP range is specified with a hyphen.
        enable_pc (Union[bool, int]): Whether to enable policy compliance tracking on the IP addresses. Defaults to False.
        enable_vm (Union[bool, int]): Whether to enable vulnerability management tracking on the IP addresses. Defaults to True.
        enable_sca (bool): Whether to enable SCA on the IP addresses. Defaults to False.
        NOTE: EITHER enable_pc OR enable_vm MUST BE TRUE FOR THE IP ADDITION TO WORK!

    :Kwargs:
        ```
        action (str): Action to perform on the IP addresses. Defaults to "add". WARNING: SDK automatically sets this value. It is just included for completeness.
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: SDK automatically sets this value. It is just included for completeness.
        tracking_method (Literal["IP", "DNS", "NETBIOS"]): Tracking method to filter on. Defaults to "IP". Valid values are IP, DNS, NETBIOS.
        owner (str): Owner of the IP addresses. Defaults to None.
        ud1 (str): User-defined field 1. Defaults to None.
        ud2 (str): User-defined field 2. Defaults to None.
        ud3 (str): User-defined field 3. Defaults to None.
        comment (str): Comment for the IP addresses. Defaults to None.
        ag_title (str): Asset group title to add the IP addresses to. Defaults to None. Required if user is a Unit Manager.
        enable_certview (bool): Whether to enable CertView on the IP addresses. Defaults to False.
        ```

    Returns:
        None
    """

    # Check if either enable_pc or enable_vm is True:
    if not enable_pc and not enable_vm:
        raise ValueError("Either enable_pc or enable_vm must be True!")

    # Check tracking_method:
    if "tracking_method" in kwargs and kwargs["tracking_method"] not in [
        "IP",
        "DNS",
        "NETBIOS",
    ]:
        raise ValueError(
            f"Invalid tracking method. Valid values are IP, DNS, NETBIOS, not {kwargs['tracking_method']}."
        )

    kwargs["action"] = "add"
    kwargs["echo_request"] = False

    # If ips is a BaseList object, convert it to a list of strings:
    if isinstance(ips, BaseList):
        ips = [str(ip) for ip in ips]
        ips = ",".join(ips)

    kwargs["ips"] = ips
    kwargs["enable_pc"] = enable_pc
    kwargs["enable_vm"] = enable_vm
    kwargs["enable_sca"] = enable_sca

    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="add_ips",
        payload=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    result = xml_parser(response.text)["SIMPLE_RETURN"]["RESPONSE"]["TEXT"]

    print(result)


def update_ips(auth: BasicAuth, ips: Union[str, BaseList], **kwargs) -> None:
    """
    Update specific details of IP addresses in the Qualys subscription.

    Params:
        auth (BasicAuth): Qualys BasicAuth object.
        ips (Union[str, BaseList): List of IP addresses/ranges to update. Can be a string or a BaseList object containing IPs. Multiple entries are comma separated. A host IP range is specified with a hyphen.

    :Kwargs:
        ```
        action (str): Action to perform on the IP addresses. Defaults to "update". WARNING: SDK automatically sets this value. It is just included for completeness.
        echo_request (bool): Whether to echo the request. Defaults to False. WARNING: SDK automatically sets this value. It is just included for completeness.
        network_id (Union[str, int]): Network ID to filter on. Defaults to None. NOTE: This has to be enabled in the Qualys subscription!
        tracking_method (Literal["IP", "DNS", "NETBIOS"]): Tracking method to filter on. Defaults to "IP". Valid values are IP, DNS, NETBIOS.
        host_dns (str): The DNS hostname for the IP you want to update. A single IP must be specified in the same request and the IP will only be updated if it matches the hostname specified.
        host_netbios (str): The NetBIOS hostname for the IP you want to update. A single IP must be specified in the same request and the IP will only be updated if it matches the hostname specified.
        owner (str): Owner of the IP addresses. Defaults to None.
        ud1 (str): User-defined field 1. Defaults to None.
        ud2 (str): User-defined field 2. Defaults to None.
        ud3 (str): User-defined field 3. Defaults to None.
        comment (str): Comment for the IP addresses. Defaults to None.

    Returns:
        None
    """

    kwargs["action"] = "update"
    kwargs["echo_request"] = False

    # If ips is a BaseList object, convert it to a list of strings:
    if isinstance(ips, BaseList):
        ips = [str(ip) for ip in ips]
        ips = ",".join(ips)

    kwargs["ips"] = ips

    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="update_ips",
        payload=kwargs,
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    result = xml_parser(response.text)["SIMPLE_RETURN"]["RESPONSE"]["TEXT"]

    print(result)
