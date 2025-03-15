"""
CLI script to quickly perform Tagging
operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import BasicAuth, write_json, write_excel
from qualysdk.tagging import *


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
        case "count_tags":
            result = count_tags(auth, **kwargs)
        case "get_tags":
            result = get_tags(auth, **kwargs)
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    if args.output:
        write_json(result, args.output) if endpoint == "count_tags" else write_excel(
            result, args.output
        )
    return result


def main():
    parser = ArgumentParser(
        description="CLI script to quickly perform tagging operations using qualysdk"
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

    # count_tags action:
    count_tags_parser = subparsers.add_parser(
        "count_tags", help="Count how many tags match the given criteria."
    )
    count_tags_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )

    count_tags_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    # get_tags action:
    get_tags_parser = subparsers.add_parser(
        "get_tags", help="Get the tags that match the given criteria."
    )
    get_tags_parser.add_argument(
        "-o",
        "--output",
        help="Output (xlsx) file to write results to",
        type=str,
        default=None,
    )
    get_tags_parser.add_argument(
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
    if args.action == "count_tags":
        result = cli_findings(auth=auth, args=args, endpoint="count_tags")
    elif args.action == "get_tags":
        result = cli_findings(auth=auth, args=args, endpoint="get_tags")
    else:
        parser.print_help()
        exit(1)

    if not args.output:
        print(result)


if __name__ == "__main__":
    main()
