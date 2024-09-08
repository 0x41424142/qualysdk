"""
reports.py - contains functions to work with reports in VMDR.
"""

from typing import Literal, Union
from os.path import join, exists
from os import mkdir
from io import StringIO

from requests.models import Response
from pandas import DataFrame, read_csv

from .data_classes import VMDRReport, ReportTemplate, VMDRScheduledReport
from ..auth import BasicAuth
from ..base import call_api
from ..base import xml_parser
from ..base.base_list import BaseList
from ..exceptions.Exceptions import *


def manage_scheduled_reports(
    auth: BasicAuth,
    action: Literal["list", "launch_now"],
    **kwargs,
) -> Response:
    """
    Backend function to manage scheduled reports in Qualys VMDR.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.
        action: Literal["list", "launch"] - The action to take.

    Returns:
        Response - The response from the API.

    :Kwargs:
        Look at the specific functions for the kwargs they accept: get_scheduled_report_list, launch_scheduled_report, etc.
    """

    # Set specific kwargs
    kwargs["action"] = action
    kwargs["echo_request"] = False

    headers = {"X-Requested-With": "qualysdk SDK"}

    match action:
        case "list":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="get_scheduled_report_list",
                params=kwargs,
                headers=headers,
            )

        case "launch_now":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="launch_scheduled_report",
                payload=kwargs,
                headers=headers,
            )

        case _:
            raise NotImplementedError(f"Action {action} is not valid.")


def manage_reports(
    auth: BasicAuth,
    action: Literal["list", "launch", "cancel", "fetch", "delete"],
    **kwargs,
) -> Response:
    """
    Backend function to manage reports in Qualys VMDR.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.
        action: Literal["list", "launch", "cancel", "fetch", "delete"] - The action to take.

    Returns:
        Response - The response from the API.

    :Kwargs:
        Look at the specific functions for the kwargs they accept: get_report_list, launch_report, etc.
    """

    # Set specific kwargs
    kwargs["action"] = action
    kwargs["echo_request"] = False

    headers = {"X-Requested-With": "qualysdk SDK"}

    match action:
        case "list":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="get_report_list",
                params=kwargs,
                headers=headers,
            )

        case "launch":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="launch_report",
                payload=kwargs,
                headers=headers,
            )

        case "cancel":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="cancel_report",
                payload=kwargs,
                headers=headers,
            )

        case "fetch":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="fetch_report",
                params=kwargs,
                headers=headers,
            )

        case "delete":
            return call_api(
                auth=auth,
                module="vmdr",
                endpoint="delete_report",
                payload=kwargs,
                headers=headers,
            )

        case _:
            raise NotImplementedError(f"Action {action} is not valid.")


def get_report_list(auth: BasicAuth, **kwargs) -> BaseList[VMDRReport]:
    """
    Get a list of reports in VMDR, according to kwargs.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.

    ## Kwargs:

        id: Optional[Union[int,str]] - A specific report ID to get.
        state: Optional[str] - Filter output to reports in a specific state.
        user_login: Optional[str] - Filter output to reports launched by a specific user.
        expires_before_datetime: Optional[str] - Filter output to reports that will expire before this datetime. Formatted like: YYYY-MM-DD[THH:MM:SSZ]
        client_id: Optional[Union[int,str]] - Filter output to reports for a specific client ID. ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!
        client_name: Optional[str] - Filter output to reports for a specific client name. ONLY VALID FOR CONSULTANT SUBSCRIPTIONS!

    Returns:
        BaseList[VMDRReport] - A list of VMDRReport objects.
    """

    response = manage_reports(auth, action="list", **kwargs)

    data = xml_parser(response.text)

    reports = data["REPORT_LIST_OUTPUT"]["RESPONSE"]["REPORT_LIST"]["REPORT"]

    bl = BaseList()

    # Check if there are multiple reports or just one
    if isinstance(reports, dict):
        reports = [reports]

    for report in reports:
        bl.append(VMDRReport.from_dict(report))

    return bl


def get_template_list(auth: BasicAuth) -> BaseList[ReportTemplate]:
    """
    Get the list of report templates in your subscription.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.

    Returns:
        BaseList[ReportTemplate] - A list of ReportTemplate objects.
    """

    response = call_api(
        auth=auth,
        module="vmdr",
        endpoint="get_template_list",
        headers={"X-Requested-With": "qualysdk SDK"},
    )

    data = xml_parser(response.text)

    if "SIMPLE_RETURN" in data:
        raise QualysAPIError(data["SIMPLE_RETURN"]["RESPONSE"]["TEXT"])

    bl = BaseList()

    templates = data["REPORT_TEMPLATE_LIST"]["REPORT_TEMPLATE"]

    # Check if there are multiple templates or just one
    if isinstance(templates, dict):
        templates = [templates]

    for template in templates:
        bl.append(ReportTemplate.from_dict(template))

    return bl


def launch_report(auth: BasicAuth, template_id: str, **kwargs) -> int:
    """
    Generate a new report in VMDR.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.
        template_id: Union[int, str] - The ID of the template to use for the report.

    :Kwargs:

        Parameter| Possible Values |Description|Required|
        |--|--|--|--|
        |auth|qualysdk.auth.BasicAuth|The authentication object.|✅|
        |template_id|Union[int, str] |The template that the report will follow. Use get_report_template_list() To select one.|✅|
        |report_title|str|The name to give to the report. ⚠️ IF YOU REQUEST A PCI COMPLIANCE REPORT, THE TITLE IS AUTO-GENERATED BY QUALYS!|❌|
        |output_format| FOR MAP REPORT: <br> pdf, html, mht, xml, csv<br>FOR SCAN REPORT:<br>pdf, html mht, xml, csv, docx<br>FOR REMEDIATION REPORT:<br>pdf, html, mht, csv<br>FOR COMPLIANCE (NON-PCI) REPORT:<br>pdf, html, mht<br>FOR PCI COMPLIANCE REPORT:<br>pdf, html<br>FOR PATCH REPORT:<br>pdf, online, xml, csv<br>FOR COMPLIANCY POLICY REPORT:<br>pdf, html, mht, xml, csv|The format that the report will be generated in.|❌|
        |hide_header|True/False| ⚠️ SDK auto-sets this to True!|❌|
        |pdf_password|str|If output_format==pdf, file will be encrypted with this password. Note that this is required for recipient_group/recipient_group_id. <br>⚠️ REQUREMENTS:<br>1.8<=N<=32 characters<br>2. Must contain alpha and numeric characters<br>3.Cannot match your Qualys account's password<br>4.Must follow any other password restrictions in Users->Setup->Security|❌|
        |recipient_group|str: "groupOne,GroupTwo"|A comma-separated string of group that the PDF will be shared with. ⚠️ CANNOT BE IN THE SAME REQUEST WITH recipient_group_id|❌|
        |recipient_group_id|str|A comma-separated string of group IDs to share the PDF with. ⚠️ CANNOT BE IN THE SAME REQUEST WITH recipient_group| ❌|
        |report_type|Literal["Map", "Scan", "Patch", "Remediation", "Compliance", "Policy"]|Shape the report to a specific type.|❌|
        |domain|str| Target domain for the report.|⚠️ REQUIRED FOR MAP REPORT|
        |ip_restriction|Comma-separated string of IP addresses to include in a map report.|⚠️ REQUIRED FOR MAP REPORT WHEN domain=='None'|
        |report_refs|str|Comma-separated string of reference IDs.|⚠️ REQUIRED FOR MAP REPORT, MANUAL SCAN REPORT, PCI COMPLIANCE REPORT|
        |asset_group_ids|str|Override asset group IDs defined in the report template with these IDs.|❌|
        |ips_network_id|Union[int, str]|Restrict the report to specific network IDs. ⚠️ MUST BE ENABLED IN THE QUALYS SUBSCRIPTION|❌|
        |ips|str|Comma-separated string of IP addresses to include, overwriting the report template.|❌|
        |assignee_type|Literal["User", "All"]|Specify if tickets assigned to the requesting user, or all tickets will be included in the report. Defaults to "User".|❌|
        |policy_id|Union[int, str]|The specific policy to run the report on.|❌|
        |host_id|str|In policy report output, show results for a single host. |⚠️ REQUIRED WHEN instance_string IS SPECIFIED.|
        |instance_string|str|Specifies a single instance on a host machine.|⚠️ REQUIRED WHEN host_id IS SPECIFIED.|

    Returns:
        int - The ID of the report.
    """

    # Set specific kwargs
    kwargs["template_id"] = template_id
    kwargs["hide_header"] = True

    response = manage_reports(auth, action="launch", **kwargs)

    data = xml_parser(response.text)

    try:
        return int(data["SIMPLE_RETURN"]["RESPONSE"]["ITEM_LIST"]["ITEM"]["VALUE"])
    except KeyError:
        raise QualysAPIError(data["SIMPLE_RETURN"]["RESPONSE"]["TEXT"])


def cancel_report(auth: BasicAuth, id: Union[int, str]) -> str:
    """
    Cancel a report in VMDR.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.
        id: Union[int, str] - The ID of the report to cancel.

    Returns:
        str - The response from the API.
    """

    response = manage_reports(auth, action="cancel", id=id)

    data = xml_parser(response.text)

    return data["SIMPLE_RETURN"]["RESPONSE"]["TEXT"]


def fetch_report(
    auth: BasicAuth, id: Union[int, str], write_out: bool = False
) -> Union[DataFrame, None]:
    """
    Fetch a report in VMDR.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.
        id: Union[int, str] - The ID of the report to fetch.
        write_out: Optional[bool] - If True, write the report to ./reports/<file>. Default is False.

    Returns:
        Union[DataFrame, None] - The report as a DataFrame if it is a CSV or XML report. Otherwise, None.
    """
    return_data = False

    response = manage_reports(auth, action="fetch", id=id)

    file_format = response.headers["Content-Type"].split("/")[-1]
    if ";" in file_format:
        file_format = file_format.split(";")[0]

    # Special case for octet-stream/word documents
    if "octet" in file_format:
        file_format = "docx"

    # Check that there is a reports directory in the directory __file__ is in
    curr_dir = join(__file__, "..")

    # Match the file format and load into the appropriate object
    match file_format:
        case "csv":
            print("Detected CSV format. Returning DataFrame.")
            # Check for a summarization header. If it exists, skip it.
            # We can delete everything before "\r\n\r\n\r\n"
            content = response.text
            count = content.count("\r\n\r\n\r\n")
            if count > 0:
                # Special case for reports with a small table before the actual CSV data starts:
                split_content = content.split("\r\n\r\n\r\n")
                if (
                    '"Severity","Total","Confirmed","Potential","Information Gathered"\r\n'
                    in split_content[~0]
                ):
                    # Split again to get the actual data, this time with 2 \r\n's:
                    content = split_content[~0].split("\r\n\r\n", 1)[
                        ~0
                    ]  # maxsplit lets us ignore newlines except for the table separator
                else:
                    content = split_content[
                        ~0
                    ]  # get the last element, which is the actual data...
            data = read_csv(StringIO(content))
            return_data = True

        case "xml":
            print("Detected XML format. Returning DataFrame.")
            data = DataFrame.from_dict(xml_parser(response.text))
            return_data = True

        case _:
            print(
                f"Detected {file_format} format. Writing to {join(curr_dir, 'output', f'{id}.{file_format}')}"
            )
            write_out = True

    if write_out:
        if not exists(join(curr_dir, "output")):
            mkdir(join(curr_dir, "output"))
            print(f"Created output directory at {join(curr_dir, 'output')}")

        with open(join(curr_dir, "output", f"{id}.{file_format}"), "wb") as f:
            f.write(response.content)
            print(f"Wrote report to {join(curr_dir, 'output', f'{id}.{file_format}')}")

    if return_data:
        return data


def delete_report(auth: BasicAuth, id: Union[int, str]) -> str:
    """
    Delete a report in VMDR.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.
        id: Union[int, str] - The ID of the report to delete.

    Returns:
        str - The response from the API.
    """

    response = manage_reports(auth, action="delete", id=id)

    data = xml_parser(response.text)

    return data["SIMPLE_RETURN"]["RESPONSE"]["TEXT"]


def get_scheduled_report_list(auth: BasicAuth, **kwargs) -> BaseList[VMDRReport]:
    """
    Get a list of scheduled reports in VMDR, according to kwargs.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.

    :Kwargs:
        id: Optional[Union[int,str]] - A specific report ID to get.
        is_active: Optional[bool] - Filter output to active or inactive reports. True for active, False for inactive.

    Returns:
        BaseList[VMDRReport] - A list of VMDRReport objects.
    """

    response = manage_scheduled_reports(auth, action="list", **kwargs)

    data = xml_parser(response.text)

    bl = BaseList()

    try:
        reports = data["SCHEDULE_REPORT_LIST_OUTPUT"]["RESPONSE"][
            "SCHEDULE_REPORT_LIST"
        ]["REPORT"]
        # Check if there are multiple reports or just one
        if isinstance(reports, dict):
            reports = [reports]

        for report in reports:
            bl.append(VMDRScheduledReport.from_dict(report))
    except KeyError:
        print("No reports found.")

    return bl


def launch_scheduled_report(auth: BasicAuth, id: str) -> str:
    """
    Launch a scheduled report in VMDR.

    Parameters:
        auth: Required[BasicAuth] - The BasicAuth object.
        id: str - The ID of the scheduled report to launch.

    Returns:
        str - The response from the API.
    """

    response = manage_scheduled_reports(auth, action="launch_now", id=id)

    data = xml_parser(response.text)

    return data["SIMPLE_RETURN"]["RESPONSE"]["TEXT"]
