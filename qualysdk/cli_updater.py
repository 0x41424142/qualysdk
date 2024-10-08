"""
Qualysdk-updater is a CLI tool installed with 
the SDK to check for and install updates from 
PyPI.
"""

from argparse import ArgumentParser
from subprocess import run, check_call
from sys import executable

from requests import Response, get
from packaging import version

# define constants for CLI colors:
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def get_pypi_versions() -> Response:
    """
    Get the versions of qualysdk available on PyPI.

    Returns:
        Response: The response object from the request.
    """

    return get("https://pypi.org/pypi/qualysdk/json")


def parse_pypi_response(response: Response) -> dict:
    """
    Parse the response from PyPI.

    Args:
        response (Response): The response object from the request.

    Returns:
        dict: The parsed response.

    Raises:
        HTTPError: If the response is not successful
    """

    response.raise_for_status()
    return delete_yanked_versions(response.json())


def delete_yanked_versions(pypi_data: dict) -> dict:
    """
    Removes yanked versions from the versions dictionary.

    Helper function for parse_pypi_response.

    Args:
        pypi_data (dict): The versions dictionary.

    Returns:
        dict: The versions dictionary with yanked versions removed.
    """

    return {k: v for k, v in pypi_data.items() if not (k == "yanked" and v)}


def show_update_info(pypi_data: dict) -> None:
    """
    Print the update information to the console.

    Args:
        pypi_data (dict): The parsed response from PyPI.
    """

    vsn = pypi_data["info"].get("version")
    release_data = pypi_data["releases"].get(vsn)[0]

    print(f"⬆️ {YELLOW} An update is available!{RESET}")
    print(f"Latest Version: {YELLOW}{vsn}{RESET}")
    print(f"Release date: {YELLOW}{release_data.get('upload_time')}{RESET}")
    print(f"MD5: {release_data.get('md5_digest')}")
    print(
        f"🐈 {GREEN} GitHub Release Notes:{RESET}",
        "https://github.com/0x41424142/qualysdk/releases/tag/v" + vsn,
    )
    print(f"🐍 {GREEN} PyPI Page:{RESET}", f"https://pypi.org/project/qualysdk/{vsn}/")


def check_installed_version() -> version.Version:
    """
    Use subprocess to get the installed version of qualysdk
    for the given environment.

    Returns:
        version.Version: The installed version of qualysdk.
    """

    return version.parse(
        run(
            [executable, "-m", "pip", "show", "qualysdk"],
            capture_output=True,
            text=True,
        )
        .stdout.split("\n")[1]
        .split(": ")[1]
    )


def prompt_for_install() -> bool:
    """
    Prompt the user to install the latest version of qualysdk.

    Returns:
        bool: True if the user wants to install, False if not.
    """

    response = input(
        f"Would you like to install the {GREEN}latest version{RESET} over current version: {YELLOW}v{check_installed_version()}{RESET}? [y/N]: "
    )
    return response.lower() in ["y", "yes"]


def main() -> int:
    """
    Entry point for the updater CLI tool.

    Returns:
        int: 0 if successful, 1 if not.
    """

    parser = ArgumentParser(description="Check for and install updates for qualysdk")

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Display the current version of qualysdk",
    )

    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="Check if a new version of qualysdk is available",
    )

    parser.add_argument(
        "-i",
        "--install",
        action="store_true",
        help="Install the latest version of qualysdk",
    )

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Bypass the confirmation prompt when installing",
        default=False,
    )

    args = parser.parse_args()

    # If every arg is False or only -y was specified,
    #  print the help message and exit.
    if not any(vars(args).values()) or (args.yes and not args.install):
        parser.print_help()
        return 1

    if args.version:
        print(f"{YELLOW}Current installed version: {check_installed_version()}{RESET}")
        return 0

    if args.check or args.install:
        response = get_pypi_versions()
        # yanked versions are automatically removed
        pypi_data = parse_pypi_response(response)

        latest_version = version.parse(pypi_data.get("info").get("version"))
        current_version = check_installed_version()
        if latest_version > current_version:
            show_update_info(pypi_data)
            if args.install:
                if args.yes or prompt_for_install():
                    print(f"⬆️ {YELLOW} Installing v{latest_version}...{RESET}")
                    try:
                        check_call(
                            [
                                executable,
                                "-m",
                                "pip",
                                "install",
                                "--upgrade",
                                "qualysdk",
                            ]
                        )
                        print(
                            f"✅ {GREEN}qualysdk has been updated to v{latest_version}{RESET}"
                        )
                    except Exception as e:
                        print(f"{RED}qualysdk update failed: {type(e).__name__}{RESET}")
                        return 1
                    return 0
                else:
                    print(f"{RED}Upgrade cancelled.{RESET}")
                    return 0
            return 0
        else:
            print(f"✅ {GREEN}qualysdk is up to date ({current_version}).{RESET}")
            return 0


if __name__ == "__main__":
    main()