"""
CLI script to quickly perform Tagging
operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import BasicAuth, write_json, write_excel, BaseList
from qualysdk.tagging import *


def cli_findings(auth: BasicAuth, args: Namespace, endpoint: str) -> None:
    # hasattr is needed to prevent AttributeError:
    if hasattr(args, "kwarg") and getattr(args, "kwarg"):
        kwargs = dict(args.kwarg)
    else:
        kwargs = {}
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
        case "get_tag_details":
            result = get_tag_details(auth, tag_id=args.tagId)
        case "create_tag":
            # parse out children into a list:
            if "children" in kwargs:
                kwargs["children"] = BaseList(kwargs["children"].split(","))
            result = create_tag(auth, args.name, **kwargs)
        case "delete_tag":
            # parse out tag ids into a list:
            args.tagId = args.tagId.split(",")
            result = delete_tag(auth, tag_id=args.tagId)
        case "update_tag":
            # parse out children into a list:
            if "add_children" in kwargs:
                kwargs["add_children"] = BaseList(kwargs["add_children"].split(","))
            if "remove_children" in kwargs:
                kwargs["remove_children"] = BaseList(kwargs["remove_children"].split(","))
            result = update_tag(auth, args.tagId, **kwargs)
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    if args.output:
        if endpoint == "get_tag_details":
            result = result.to_serializable_dict()
            write_json(result, args.output)
        else:
            (
                write_json(result, args.output)
                if endpoint == "count_tags"
                else write_excel(result, args.output)
            )
    return result


def main():
    parser = ArgumentParser(
        description="CLI script to quickly perform tagging operations using qualysdk"
    )
    parser.add_argument("-u", "--username", required=True, help="Qualys username", type=str)
    parser.add_argument("-p", "--password", required=True, help="Qualys password", type=str)
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

    get_details_parser = subparsers.add_parser(
        "get_tag_details", help="Get all details of a single tag."
    )

    get_details_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )

    get_details_parser.add_argument(
        "-t",
        "--tagId",
        help="ID of the tag to pull details for",
        type=int,
        required=True,
    )

    create_tag_parser = subparsers.add_parser(
        "create_tag",
        help='Create a new tag. NOTE: For creating children tags, use --kwarg children with a comma-separated string, like: "child1,child2,etc"',
    )
    create_tag_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )
    create_tag_parser.add_argument(
        "-n", "--name", help="Name of the tag to create", type=str, required=True
    )
    create_tag_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    delete_tag_parser = subparsers.add_parser(
        "delete_tag",
        help="Delete a tag. NOTE: For deleting multiple tags, use --kwarg tagId with a comma-separated string, like: 'id1,id2,etc'",
    )
    delete_tag_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )
    delete_tag_parser.add_argument(
        "-t",
        "--tagId",
        help="ID(s) of the tag to delete. Multiple values can be provided as a comma-separated string",
        type=str,
        required=True,
    )

    update_tag_parser = subparsers.add_parser(
        "update_tag",
        help="Update a tag. NOTE: For adding/removing children tags, use --kwarg add_children/remove_children with a comma-separated string, like: 'id1,id2,etc'",
    )
    update_tag_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )
    update_tag_parser.add_argument(
        "-t", "--tagId", help="ID of the tag to update", type=int, required=True
    )
    update_tag_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times. For add_children, supply a comma-separated string of names. for remove_children, supply a comma-separated string of ids.",
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
    elif args.action == "get_tag_details":
        result = cli_findings(auth=auth, args=args, endpoint="get_tag_details")
    elif args.action == "create_tag":
        result = cli_findings(auth=auth, args=args, endpoint="create_tag")
    elif args.action == "delete_tag":
        result = cli_findings(auth=auth, args=args, endpoint="delete_tag")
    elif args.action == "update_tag":
        result = cli_findings(auth=auth, args=args, endpoint="update_tag")
    else:
        parser.print_help()
        exit(1)

    if not args.output:
        if isinstance(result, int):
            print(result)
        else:
            print(result.dump_json(indent=2))


if __name__ == "__main__":
    main()
