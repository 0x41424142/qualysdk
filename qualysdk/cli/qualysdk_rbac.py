"""
CLI script to quickly perform administration user management
operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import BasicAuth, write_json
from qualysdk.admin.rbac import get_user_details, search_users, update_user


def cli_users(auth: BasicAuth, args: Namespace, endpoint: str) -> None:
    match endpoint:
        case "get_user_details":
            result = get_user_details(auth, args.user_id)
        case "search_users":
            if args.all:
                # If --all is set, we search for all active users
                args.user_id = 1
                args.id_operator = "GREATER"
            elif not args.user_id:
                # If no user_id is provided, we default to searching for all users
                args.user_id = None
                args.id_operator = "EQUALS"
            result = search_users(
                auth,
                role_name=args.role,
                user_id=args.user_id,
                user_id_operator=args.id_operator,
                username=args.qualys_username,
            )
        case "update_user":
            result = update_user(
                auth,
                args.user_id,
                add_tag_ids=args.add_tag_ids if args.add_tag_ids else None,
                add_tag_names=args.add_tag_names if args.add_tag_names else None,
                add_role_ids=args.add_role_ids if args.add_role_ids else None,
                add_role_names=args.add_role_names if args.add_role_names else None,
                remove_tag_ids=args.remove_tag_ids if args.remove_tag_ids else None,
                remove_tag_names=args.remove_tag_names if args.remove_tag_names else None,
                remove_role_ids=args.remove_role_ids if args.remove_role_ids else None,
                remove_role_names=args.remove_role_names if args.remove_role_names else None,
            )

        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    # hasattr check to avoid AttributeError, as update_user does not have --output argument
    if hasattr(args, "output") and args.output:
        result = result.serialized()
        write_json(result, args.output)
    return result


def main():
    parser = ArgumentParser(
        description="CLI script to quickly perform user permissions operations in the administration module using qualysdk."
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

    # get_user_details action:
    get_user_details_parser = subparsers.add_parser(
        "get_user_details",
        help="Get the details of a specific user from the Qualys administration module.",
    )

    get_user_details_parser.add_argument(
        "user_id",
        help="The administration ID of the user to retrieve details for",
        type=int,
    )

    get_user_details_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )

    # search_users action:
    search_users_parser = subparsers.add_parser(
        "search_users", help="Search for users in the admin module."
    )

    search_users_parser.add_argument(
        "-r",
        "--role",
        help="The role of the user(s) to search for",
        type=str,
        default=None,
    )

    search_users_parser.add_argument(
        "-i",
        "--user-id",
        help="The user ID to search for",
        type=int,
        default=None,
    )

    search_users_parser.add_argument(
        "--id-operator",
        help="The operator to use for the user ID search",
        type=str,
        choices=["EQUALS", "GREATER", "LESSER"],
        default="EQUALS",
    )

    search_users_parser.add_argument(
        "-qU",
        "--qualys-username",
        help="The username to search for",
        type=str,
        default=None,
    )

    search_users_parser.add_argument(
        "-a",
        "--all",
        help="If set, will return all active users. Shorthand for `--user-id=1` & --id-operator='GREATER'.",
        action="store_true",
    )

    search_users_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )

    update_user_parser = subparsers.add_parser(
        "update_user", help="Update an existing user's tags/scope."
    )

    update_user_parser.add_argument(
        "user_id",
        help="ID of the user to update",
        type=str,
    )

    update_user_parser.add_argument(
        "--add-tag-ids",
        help="List of tag IDs to add to the user. Use like: --add-tag-ids 123 456 789",
        type=int,
        nargs="+",
        default=[],
    )

    update_user_parser.add_argument(
        "--add-tag-names",
        help="List of tag names to add to the user. Use like: --add-tag-names tag1 tag2 tag3",
        type=str,
        nargs="+",
        default=[],
    )

    update_user_parser.add_argument(
        "--add-role-ids",
        help="List of role IDs to add to the user. Use like: --add-role-ids 123 456 789",
        type=int,
        nargs="+",
        default=[],
    )

    update_user_parser.add_argument(
        "--add-role-names",
        help="List of role names to add to the user. Use like: --add-role-names role1 role2 role3",
        type=str,
        nargs="+",
        default=[],
    )

    update_user_parser.add_argument(
        "--remove-tag-ids",
        help="List of tag IDs to remove from the user. Use like: --remove-tag-ids 123 456 789",
        type=int,
        nargs="+",
        default=[],
    )

    update_user_parser.add_argument(
        "--remove-tag-names",
        help="List of tag names to remove from the user. Use like: --remove-tag-names tag1 tag2 tag3",
        type=str,
        nargs="+",
        default=[],
    )

    update_user_parser.add_argument(
        "--remove-role-ids",
        help="List of role IDs to remove from the user. Use like: --remove-role-ids 123 456 789",
        type=int,
        nargs="+",
        default=[],
    )

    update_user_parser.add_argument(
        "--remove-role-names",
        help="List of role names to remove from the user. Use like: --remove-role-names role1 role2 role3",
        type=str,
        nargs="+",
        default=[],
    )

    args = parser.parse_args()

    # create BasicAuth object
    auth = BasicAuth(args.username, args.password, platform=args.platform)

    # perform action
    if args.action == "get_user_details":
        result = cli_users(auth=auth, args=args, endpoint="get_user_details")
    elif args.action == "search_users":
        if not any([args.role, args.user_id, args.qualys_username, args.all]):
            parser.error(
                "At least one of --role, --user-id, --qualys-username, or --all must be specified."
            )
        result = cli_users(auth=auth, args=args, endpoint="search_users")
    elif args.action == "update_user":
        if not any(
            [
                args.add_tag_ids,
                args.add_tag_names,
                args.add_role_ids,
                args.add_role_names,
                args.remove_tag_ids,
                args.remove_tag_names,
                args.remove_role_ids,
                args.remove_role_names,
            ]
        ):
            parser.error(
                "At least one of --add-tag-ids, --add-tag-names, --add-role-ids, "
                "--add-role-names, --remove-tag-ids, --remove-tag-names, "
                "--remove-role-ids, or --remove-role-names must be specified."
            )
        result = cli_users(auth=auth, args=args, endpoint="update_user")
    else:
        parser.print_help()
        exit(1)

    # hasattr check to avoid AttributeError, as update_user does not have --output argument
    if hasattr(args, "output") and not args.output:
        print(result.dump_json())
    elif not hasattr(args, "output"):
        print(result)


if __name__ == "__main__":
    main()
