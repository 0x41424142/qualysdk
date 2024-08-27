"""
calls.py - contains the user-facing functions for most cloud agent API calls.
"""

from typing import Union

from .data_classes.Agent import CloudAgent
from .prepare_criteria import prepare_criteria
from ..base.call_api import call_api
from ..base.xml_parser import xml_parser
from ..auth.basic import BasicAuth
from ..base.base_list import BaseList


def list_agents(
    auth: BasicAuth, page_count: Union[int, "all"] = "all", **kwargs
) -> BaseList[CloudAgent]:
    """
    Get a list of Cloud Agents in your subscription, according to the filters provided.

    Args:
        auth (BasicAuth): The authentication object containing the user's credentials.
        page_count (Union[int, 'all']): The number of pages to retrieve. Defaults to 'all'.
        **kwargs: The filters to apply to the list.

    ## Kwargs:

        qwebHostId (int): The QWEB Host ID to filter the agents by.
        lastVulnScan (str): The date of the last vulnerability scan. Formatted like YYYY-MM-DD[THH:MM:SSZ].
        lastComplianceScan (str): The date of the last compliance scan. Formatted like YYYY-MM-DD[THH:MM:SSZ].
        informationGatheredUpdated (str): The date the information was last updated. Formatted like YYYY-MM-DD[THH:MM:SSZ].
        os (str): The operating system of the agent.
        dnsHostName (str): The DNS hostname of the agent.
        address (str): The IP address of the agent.
        vulnsUpdated (str): The date the vulnerabilities were last updated. Formatted like YYYY-MM-DD[THH:MM:SSZ].
        id (int): The **Asset ID** of the agent.
        name (str): The name of the agent.
        created (str): The creation date of the agent. Formatted like YYYY-MM-DD[THH:MM:SSZ].
        type (str): The type of agent.
        netbiosName (str): The NetBIOS name of the agent.
        netbiosNetworkID (str): The NetBIOS network ID of the agent.
        networkGuid (str): The network GUID of the agent.
        trackingMethod (Literal['NONE', 'IP', 'DNSNAME', 'NETBIOS', 'INSTANCE_ID', 'QAGENT']): The tracking method of the agent.
        port (int): The port of the agent.
        installedSoftware (str): Search installed software on the agent.
        tagName (str): The tag name to filter the agents by.
        tagId (int): The tag ID to filter the agents by.
        update: (str): The date the agent was last updated. Formatted like YYYY-MM-DD[THH:MM:SSZ].
        activationKey (str): The activation key of the agent.
        agentConfigurationName (str): The agent configuration name.
        agentConfigurationId (float): The agent configuration ID.
        agentVersion (str): The agent VB version.
        lastCheckedIn (str): The date the agent last checked in. Formatted like YYYY-MM-DD[THH:MM:SSZ].

        DATE OPERATOR KWARGS:
        created_operator (Literal['GREATER', 'LESSER']): The operator to apply to the created date.
        update_operator (Literal['GREATER', 'LESSER']): The operator to apply to the updated date.
        lastVulnScan_operator (Literal['GREATER', 'LESSER']): The operator to apply to the last vulnerability scan date.
        lastComplianceScan_operator (Literal['GREATER', 'LESSER']): The operator to apply to the last compliance scan date.
        informationGatheredUpdated_operator (Literal['GREATER', 'LESSER']): The operator to apply to the information gathered updated date.
        vulnsUpdated_operator (Literal['GREATER', 'LESSER']): The operator to apply to the vulnerabilities updated date.
        lastCheckedIn_operator (Literal['GREATER', 'LESSER']): The operator to apply to the last checked in date.

    Returns:
        BaseList[CloudAgent]: A list of CloudAgent objects.
    """

    # Ensure positive page_count:
    if page_count != "all" and page_count < 1:
        raise ValueError("page_count must be 'all' or a positive integer.")

    payload = {"_xml_data": prepare_criteria(**kwargs)}

    results = BaseList()
    pulled = 0

    while True:
        response = call_api(
            auth=auth,
            module="cloud_agent",
            endpoint="list_agents",
            payload=payload,
        )

        parsed = xml_parser(response.text)

        if parsed.get("ServiceResponse")["responseCode"] != "SUCCESS":
            combined_error = f"{parsed.get('ServiceResponse')['responseErrorDetails']['errorMessage']}: {parsed.get('ServiceResponse')['responseErrorDetails']['errorResolution']}"
            raise ValueError(combined_error)

        if not parsed.get("ServiceResponse").get("data").get("HostAsset"):
            break

        data = parsed.get("ServiceResponse").get("data").get("HostAsset")

        if not isinstance(data, list):
            data = [data]

        for agent in data:
            results.append(CloudAgent(**agent))

        pulled += 1
        print(f"Pulled page {pulled}...")

        if page_count != "all" and pulled >= page_count:
            print("Page count reached. Returning...")
            break

        if parsed.get("ServiceResponse").get("hasMoreRecords") != "true":
            break

        else:
            # Grab the last asset ID to use as the pagination ID
            last_id = parsed["ServiceResponse"]["lastId"]
            payload["_xml_data"] = prepare_criteria(
                pagination_id=int(last_id) - 1, **kwargs
            )

    return results
