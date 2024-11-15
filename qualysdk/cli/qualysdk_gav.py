"""
CLI script to quickly perform Global AssetView
(GAV) operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import TokenAuth, write_excel, BaseList
from qualysdk.gav import *
from qualysdk.base.json_export import write_json


def parse_asset_id(value):
    try:
        return int(value)
    except ValueError:
        return value


def cli_findings(auth: TokenAuth, args: Namespace, endpoint: str) -> None:
    kwargs = dict(args.kwarg) if args.kwarg else {}
    if "page_count" in kwargs:
        kwargs["page_count"] = int(kwargs["page_count"])
    for kwarg in kwargs:
        if str(kwargs[kwarg]).lower() == "true":
            kwargs[kwarg] = True
        elif str(kwargs[kwarg]).lower() == "false":
            kwargs[kwarg] = False

    match endpoint:
        case "count_assets":
            result = count_assets(auth, **kwargs)
        case "get_all_assets":
            result = get_all_assets(auth, **kwargs)
        case "get_asset":
            kwargs["assetId"] = args.asset_id
            result = get_asset(auth, **kwargs)
        case "query_assets":
            result = query_assets(auth, **kwargs)
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    # If the result object does NOT have the len() method available,
    # we need to wrap it in a BaseList:
    if not hasattr(result, "__len__") and endpoint != "count_assets":
        bl = BaseList()
        bl.append(result)
        result = bl

    (
        write_excel(result, args.output)
        if endpoint != "count_assets"
        else write_json(result, args.output)
    )


def main():
    parser = ArgumentParser(
        description="CLI script to quickly perform Global AssetView (GAV) operations using qualysdk"
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
    count_assets_parser = subparsers.add_parser(
        "count_assets",
        help="Count how many assets match a GAV QQL filter & save to a JSON file.",
    )
    count_assets_parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file to write results to",
        type=str,
        default="gav_asset_count.json",
    )
    count_assets_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    get_all_assets_parser = subparsers.add_parser(
        "get_all_assets", help="Pull a list of all assets in the GAV API."
    )

    get_all_assets_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="gav_all_assets.xlsx",
    )

    get_all_assets_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    get_asset_parser = subparsers.add_parser(
        "get_asset",
        help="Get a specific asset by asset ID (not host ID) & save to a JSON file.",
    )

    get_asset_parser.add_argument(
        "asset_id",
        help="The ID of the asset to get.",
        type=parse_asset_id,
    )

    get_asset_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="gav_asset.xlsx",
    )

    get_asset_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    query_assets_parser = subparsers.add_parser(
        "query_assets", help="Query assets based on a GAV QQL filter."
    )

    query_assets_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="gav_queried_assets.xlsx",
    )

    query_assets_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    args = parser.parse_args()

    # create TokenAuth object
    auth = TokenAuth(args.username, args.password, platform=args.platform)

    # perform action
    if args.action == "count_assets":
        cli_findings(auth=auth, args=args, endpoint="count_assets")
    elif args.action == "get_all_assets":
        cli_findings(auth=auth, args=args, endpoint="get_all_assets")
    elif args.action == "get_asset":
        cli_findings(auth=auth, args=args, endpoint="get_asset")
    elif args.action == "query_assets":
        cli_findings(auth=auth, args=args, endpoint="query_assets")
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
