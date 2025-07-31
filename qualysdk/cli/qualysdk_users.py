"""
CLI script to quickly perform user management
operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import BasicAuth, write_json
from qualysdk.vmdr import users


def cli_users(auth: BasicAuth, args: Namespace, endpoint: str) -> None:
    match endpoint:
        case "get_users":
            kwargs = {}
            if args.external_id_contains:
                kwargs["external_id_contains"] = args.external_id_contains
            if args.external_id_assigned:
                kwargs["external_id_assigned"] = args.external_id_assigned
            result = users.get_user_list(auth, **kwargs)
        case "create_user":
            kwargs = {}
            for arg in [
                "asset_groups",
                "fax",
                "address2",
                "zip_code",
                "external_id",
            ]:
                if getattr(args, arg) is not None:
                    kwargs[arg] = getattr(args, arg)
            if args.no_welcome_email:
                kwargs["send_email"] = False  # correct the wording to match the API
            else:
                kwargs["send_email"] = True
            result = users.add_user(
                auth,
                args.role,
                args.unit,
                args.first_name,
                args.last_name,
                args.title,
                args.phone,
                args.email,
                args.address1,
                args.city,
                args.country,
                args.state,
                **kwargs,
            )
        case "edit_user":
            kwargs = {}
            for arg in [
                "asset_groups",
                "first_name",
                "last_name",
                "title",
                "phone",
                "fax",
                "email",
                "address1",
                "address2",
                "city",
                "state",
                "country",
                "zip_code",
                "external_id",
            ]:
                if getattr(args, arg) is not None:
                    kwargs[arg] = getattr(args, arg)
            result = users.edit_user(auth, args.user_id, **kwargs)

        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    if args.action == "get_users" and args.output:
        result = result.serialized()
        write_json(result, args.output)
    return result


def main():
    parser = ArgumentParser(
        description="CLI script to quickly perform user management operations using qualysdk"
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

    # get_users action:
    get_users_parser = subparsers.add_parser(
        "get_users", help="Get the users that match the given criteria."
    )
    get_users_parser.add_argument(
        "-o",
        "--output",
        help="Output (json) file to write results to",
        type=str,
        default=None,
    )

    get_users_parser.add_argument(
        "--external-id-contains",
        help="Specify an external ID to filter users by",
        type=str,
    )

    get_users_parser.add_argument(
        "--external-id-assigned",
        help="If set, only return users with an external ID assigned to their Qualys account",
        action="store_true",
    )

    # create_user action:
    create_user_parser = subparsers.add_parser("create_user", help="Create a new user.")

    create_user_parser.add_argument(
        "role",
        help="The role of the user to create",
        choices=[
            "manager",
            "unit_manager",
            "scanner",
            "reader",
            "contact",
            "administrator",
        ],
        default="scanner",
    )

    create_user_parser.add_argument(
        "unit",
        help="The business unit of the user to create. Use 'Unassigned' if the user does not belong to a business unit.",
        type=str,
        default="Unassigned",
    )

    create_user_parser.add_argument(
        "first_name",
        help="The first name of the user to create",
        type=str,
    )

    create_user_parser.add_argument(
        "last_name",
        help="The last name of the user to create",
        type=str,
    )

    create_user_parser.add_argument(
        "title",
        help="The title of the user to create",
        type=str,
    )

    create_user_parser.add_argument(
        "phone",
        help="The phone number of the user to create",
        type=str,
    )

    create_user_parser.add_argument(
        "email",
        help="The email of the user to create",
        type=str,
    )

    create_user_parser.add_argument(
        "address1",
        help="The address of the user to create",
        type=str,
    )

    create_user_parser.add_argument(
        "city",
        help="The city of the user to create",
        type=str,
    )

    create_user_parser.add_argument(
        "state",
        help="The state of the user to create. Must be the full name of the state, e.g. 'Maryland' or 'Pennsylvania'",
        type=str,
    )

    create_user_parser.add_argument(
        "country",
        help="The country of the user to create. Must be the full name of the country, e.g. 'United States of America' or 'Canada'",
        type=str,
    )

    create_user_parser.add_argument(
        "-nW",
        "--no-welcome-email",
        help="If set, do not send a welcome email to the user, instead return the user login credentials to stdout. Default is to send a welcome email.",
        action="store_true",
        default=False,
    )

    create_user_parser.add_argument(
        "-aG",
        "--asset-groups",
        help="Comma-separated string of asset group IDs to assign to the user",
        type=str,
    )

    create_user_parser.add_argument(
        "-f",
        "--fax",
        help="The fax number of the user. Because we're still in the 1980s, and Rick Astley is never gonna give you up...",
        type=str,
    )

    create_user_parser.add_argument(
        "-a2",
        "--address2",
        help="The second line of the address of the user if applicable",
        type=str,
    )

    create_user_parser.add_argument(
        "-z",
        "--zip-code",
        help="The zip code of the user",
        type=str,
    )

    create_user_parser.add_argument(
        "-eID",
        "--external-id",
        help="The external ID of the user. This is a unique identifier for the user in your system.",
        type=str,
    )

    # edit_user action:

    edit_user_parser = subparsers.add_parser("edit_user", help="Edit an existing user.")

    edit_user_parser.add_argument(
        "user_id",
        help="Username of the user to edit",
        type=str,
    )

    edit_user_parser.add_argument(
        "--asset-groups",
        help="Comma-separated string of asset group IDs to assign to the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--first-name",
        help="New first name of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--last-name",
        help="New last name of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--title",
        help="New title of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--phone",
        help="New phone number of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--fax",
        help="New fax number of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--email",
        help="New email of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--address1",
        help="New address of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--address2",
        help="New second line of the address of the user if applicable",
        type=str,
    )

    edit_user_parser.add_argument(
        "--city",
        help="New city of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--state",
        help="New state of the user. Must be the full name of the state, e.g. 'Maryland' or 'Pennsylvania'",
        type=str,
    )

    edit_user_parser.add_argument(
        "--country",
        help="New country of the user. Must be the full name of the country, e.g. 'United States of America' or 'Canada'",
        type=str,
    )

    edit_user_parser.add_argument(
        "--zip-code",
        help="New zip code of the user",
        type=str,
    )

    edit_user_parser.add_argument(
        "--external-id",
        help="New external ID of the user. This is a unique identifier for the user in your system.",
        type=str,
    )

    args = parser.parse_args()

    # create BasicAuth object
    auth = BasicAuth(args.username, args.password, platform=args.platform)

    # perform action
    if args.action == "get_users":
        result = cli_users(auth=auth, args=args, endpoint="get_users")
    elif args.action == "create_user":
        result = cli_users(auth=auth, args=args, endpoint="create_user")
    elif args.action == "edit_user":
        result = cli_users(auth=auth, args=args, endpoint="edit_user")
    else:
        parser.print_help()
        exit(1)

    if not args.action == "get_users":
        if isinstance(result, (int, str, float)):
            print(result)
        else:
            print(result.dump_json(indent=2))
    elif not args.output:
        print(result.dump_json(indent=2))


if __name__ == "__main__":
    main()
