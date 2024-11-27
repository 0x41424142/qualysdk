"""
CLI script to quickly perform Certificate View
(CERT) operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import TokenAuth, write_excel, BaseList
from qualysdk.cert import *


def cli_fn(auth: TokenAuth, args: Namespace, endpoint: str) -> None:
    kwargs = dict(args.kwarg) if args.kwarg else {}
    if "page_count" in kwargs:
        kwargs["page_count"] = int(kwargs["page_count"])
    for kwarg in kwargs:
        if str(kwargs[kwarg]).lower() == "true":
            kwargs[kwarg] = True
        elif str(kwargs[kwarg]).lower() == "false":
            kwargs[kwarg] = False

    match endpoint:
        case "list_certs":
            result = list_certs(auth, **kwargs)
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    # If the result object does NOT have the len() method available,
    # we need to wrap it in a BaseList:
    if not hasattr(result, "__len__"):
        bl = BaseList()
        bl.append(result)
        result = bl

    write_excel(result, args.output)


def main():
    parser = ArgumentParser(
        description="CLI script to quickly perform Certificate View (CERT) operations using qualysdk"
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

    list_certs_parser = subparsers.add_parser(
        "list_certs", help="Get a list of certificates according to kwargs."
    )
    list_certs_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="qualysdk-certview-certs.xlsx",
    )
    list_certs_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    args = parser.parse_args()

    # create TokenAuth object
    auth = TokenAuth(args.username, args.password, platform=args.platform)

    match args.action:
        case "list_certs":
            cli_fn(auth=auth, args=args, endpoint="list_certs")
        case _:
            parser.print_help()
            exit(1)


if __name__ == "__main__":
    main()
