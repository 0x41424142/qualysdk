"""
CLI script to quickly perform Web Application Scanning
(WAS) operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import BasicAuth, write_excel, BaseList
from qualysdk.was import *


def cli_findings(auth: BasicAuth, args: Namespace, endpoint: str) -> None:
    kwargs = dict(args.kwarg) if args.kwarg else {}
    if "page_count" in kwargs:
        kwargs["page_count"] = int(kwargs["page_count"])
    for kwarg in kwargs:
        if str(kwargs[kwarg]).lower() == "true":
            kwargs[kwarg] = True
        elif str(kwargs[kwarg]).lower() == "false":
            kwargs[kwarg] = False

    match endpoint:
        case "get_findings":
            result = get_findings(auth, **kwargs)
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    # If the result object does NOT have the len() method available,
    # we need to wrap it in a BaseList:
    if not hasattr(result, "__len__"):
        bl = BaseList()
        bl.append(result)

    write_excel(result, args.output)


def main():
    parser = ArgumentParser(
        description="CLI script to quickly perform Web Application Scanning (WAS) operations using qualysdk"
    )
    parser.add_argument(
        "-u", "--username", required=True, help="Qualys username", type=str
    )
    parser.add_argument(
        "-p", "--password", required=True, help="Qualys password", type=str
    )
    parser.add_argument(
        "-P",
        "--platform",
        help="Qualys platform",
        default="qg3",
        choices=["qg1", "qg2", "qg3", "qg4"],
    )

    # subparser for action:
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # get_findings action:
    list_findings_parser = subparsers.add_parser(
        "get_findings", help="Get a list of WAS findings."
    )
    list_findings_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="was_findings.xlsx",
    )
    list_findings_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    args = parser.parse_args()

    # create BasicAuth object
    auth = BasicAuth(args.username, args.password, platform=args.platform)

    # perform action
    if args.action == "get_findings":
        cli_findings(auth=auth, args=args, endpoint="get_findings")
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
