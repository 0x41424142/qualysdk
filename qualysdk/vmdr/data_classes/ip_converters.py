"""
ip_converters.py - contains the IP and IPRange helpers for the VMDR module.

The helpers convert string inputs from raw API responses into ipaddress.IPvxAddress/IPvxNetwork objects.
"""

from ipaddress import (
    ip_address,
    ip_network,
    IPv4Address,
    IPv6Address,
    IPv4Network,
    IPv6Network,
    summarize_address_range,
)
from typing import Union


def single_ip(ip: str) -> ip_address:
    """
    Converts a single IP string into an ipaddress.IPv4Address or ipaddress.IPv6Address object.

    Params:
        ip (str): IP address string.

    Returns:
        Union[IPv4Address, IPv6Address]: IPv4Address or IPv6Address object.
    """
    return ip_address(ip)


def single_range(ip_range: str) -> ip_network:
    """
    Converts an IP range string into an ipaddress.IPv4Network or ipaddress.IPv6Network object.

    Params:
        ip_range (str): IP range string.

    Returns:
        Union[IPv4Network, IPv6Network]: IPv4Network or IPv6Network object.
    """
    start, end = ip_range.split("-")

    start, end = ip_address(start), ip_address(end)

    # A little confusing, but summarize_address_range returns a generator, so we use list comprehension and then grab the first element.
    return ip_network([i for i in summarize_address_range(start, end)][0])


# Bulk IP and IP range conversion functions:


def convert_ips(ips: list[str]) -> list[Union[IPv4Address, IPv6Address]]:
    """
    Converts a list of IP strings into a list of ipaddress.IPv4Address or ipaddress.IPv6Address objects.

    Params:
        ips (list[str]): List of IP address strings.

    Returns:
        list[Union[IPv4Address, IPv6Address]]: List of IPv4Address or IPv6Address objects.
    """
    return [single_ip(ip) for ip in ips]


def convert_ranges(ip_ranges: list[str]) -> list[Union[IPv4Network, IPv6Network]]:
    """
    Converts a list of IP range strings into a list of ipaddress.IPv4Network or ipaddress.IPv6Network objects.

    Params:
        ip_ranges (list[str]): List of IP range strings.

    Returns:
        list[Union[IPv4Network, IPv6Network]]: List of IPv4Network or IPv6Network objects.
    """
    return [single_range(ip_range) for ip_range in ip_ranges]
