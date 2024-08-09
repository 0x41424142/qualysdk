"""
query_kb.py - contains the query_kb function for the qualysdk package.

This function is used to query the Qualys KnowledgeBase (KB), which is a database of vulnerabilities and their details.
"""

from typing import *
from urllib.parse import parse_qs, urlparse

from .data_classes.kb_entry import KBEntry
from .data_classes.lists.base_list import BaseList
from ..base.call_api import call_api
from ..auth.token import BasicAuth
from ..base.xml_parser import xml_parser


def query_kb(auth: BasicAuth, **kwargs) -> List[KBEntry]:
    """
    Query the Qualys KnowledgeBase (KB) for vulnerabilities matching the kiven kwargs.
    Can be used to download the entire KB (no kwargs) or to search for specific vulnerabilities.
    NOTE: this function automatically appends 'action=list' to the kwargs. You do not need to include it. Should you do so, it will be overwritten. It is just recognized as valid for the sake of completeness.

    Params:
        auth (BasicAuth) The authentication object.

    :Kwargs:
        ```
        action (str) #The action to perform. Default is 'list'. WARNING: any value you pass is overwritten with 'list'. It is just recognized as valid for the sake of completeness.
        code_modified_after (str) #The date to search for vulnerabilities modified after Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        code_modified_before (str) #The date to search for vulnerabilities modified before Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        echo_request (str) #Response will include the request you sent.
        details Literal["Basic", "All", "None"]: #The level of detail to return. Default is 'Basic'.
        ids (str) #The IDs of the vulnerabilities to return as a comma-separated string.
        id_min (int) #The minimum ID of the vulnerabilities to return.
        id_max (int) #The maximum ID of the vulnerabilities to return.
        is_patchable (bool) #Whether the vulnerability is patchable. Default is 'False'.
        last_modified_after (str) #The date to search for vulnerabilities last modified after Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        last_modified_before (str) #The date to search for vulnerabilities last modified before Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        last_modified_by_user_after (str) #The date to search for vulnerabilities last modified by user after Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        last_modified_by_user_before (str) #The date to search for vulnerabilities last modified by user before Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        last_modified_by_service_after (str) #The date to search for vulnerabilities last modified by service after Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        last_modified_by_service_before (str) #The date to search for vulnerabilities last modified by service before Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        published_after (str) #The date to search for vulnerabilities published after Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        published_before (str) #The date to search for vulnerabilities published before Formatted as 'YYYY-MM-DD[THH:MM:SSZ]' format UTC/GMT.
        discovery_method (str) #The discovery method of the vulnerability.
        discovery_auth_types (str) #The authentication types used to discover the vulnerability.
        show_pci_reasons (bool) #Whether to show PCI reasons. Default is 'False'.
        show_supported_modules_info (bool) #Whether to show supported modules info. Default is 'False'.
        show_disabled_flag (bool) #Whether to show the disabled flag. Default is 'False'.
        show_qid_change_log (bool) #Whether to show the QID change log. Default is 'False'.
        ```
    Returns:
        List of KBEntry objects representing the vulnerabilities returned by the query.
    """

    # add the action to the kwargs:
    kwargs["action"] = "list"

    responses = BaseList()
    pulled = 0

    # qualys expects all boolean values to be represented as a 0 or 1:
    for key, value in kwargs.items():
        if isinstance(value, bool):
            kwargs[key] = 1 if value else 0

    while True:
        # make the request:
        response = call_api(
            auth=auth,
            module="vmdr",
            endpoint="query_kb",
            params=kwargs,
            headers={"X-Requested-With": "qualysdk SDK"},
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        xml = xml_parser(response.text)

        # check if there is no vuln list
        if "VULN_LIST" not in xml["KNOWLEDGE_BASE_VULN_LIST_OUTPUT"]["RESPONSE"]:
            break

        for e in xml["KNOWLEDGE_BASE_VULN_LIST_OUTPUT"]["RESPONSE"]["VULN_LIST"][
            "VULN"
        ]:
            responses.append(KBEntry.from_dict(e))  # append entry

        pulled += 1
        print(f"Page {pulled} complete.")
        # KB API normally does not paginate, but if it does
        if "WARNING" in xml["KNOWLEDGE_BASE_VULN_LIST_OUTPUT"]["RESPONSE"]:
            if "URL" in xml["KNOWLEDGE_BASE_VULN_LIST_OUTPUT"]["RESPONSE"]["WARNING"]:
                print(
                    f"Pagination detected. Pulling next page from url: {xml['KNOWLEDGE_BASE_VULN_LIST_OUTPUT']['RESPONSE']['WARNING']['URL']}"
                )
                # parse the url to get the query params
                ps = parse_qs(
                    urlparse(
                        xml["KNOWLEDGE_BASE_VULN_LIST_OUTPUT"]["RESPONSE"]["WARNING"][
                            "URL"
                        ]
                    ).query
                )
                # update the kwargs with the new params
                kwargs.update(ps)

            else:
                break
        else:
            break

    return responses
