"""
Qualysdk-updater is a CLI tool installed with
the SDK to check for and install updates from
PyPI.
"""

from argparse import ArgumentParser
from subprocess import run, check_call, DEVNULL
from sys import executable

from requests import Response, get
from packaging import version

# define constants for CLI colors:
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
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
    digests = release_data.get("digests")
    if not digests:
        digests = {"blake2_256": "N/A", "sha256": "N/A", "md5_digest": "N/A"}

    print(f"🟧 {YELLOW}An update is available!{RESET}")
    print(f"📅 Latest Version: {YELLOW}v{vsn}{RESET}")
    print(f"📅 Release Date: {YELLOW}{release_data.get('upload_time')}{RESET}")
    print(f"✅ MD5: {RED}{digests.get('md5')}{RESET}")
    print(f"✅ BLAKE2b_256: {RED}{digests.get('blake2b_256')}{RESET}")
    print(f"✅ SHA256: {RED}{digests.get('sha256')}{RESET}")
    print(
        f"🐈 {GREEN}GitHub Release Notes:{RESET}{BLUE} https://github.com/0x41424142/qualysdk/releases/tag/v{vsn} {RESET}"
    )
    print(
        f"🐍 {GREEN}PyPI Page:{RESET}{BLUE} https://pypi.org/project/qualysdk/{vsn}/ {RESET}"
    )


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
        exit(0)

    if args.version:
        print(
            f"{YELLOW}Qualysdk version currently installed: v{check_installed_version()}{RESET}"
        )
        exit(0)

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
                    print(f"🟧 {YELLOW}Installing v{latest_version}...{RESET}")
                    try:
                        check_call(
                            [
                                executable,
                                "-m",
                                "pip",
                                "install",
                                "--upgrade",
                                "qualysdk",
                            ],
                            stdout=DEVNULL,
                        )
                        print(
                            f"✅ {GREEN}Qualysdk has been updated to v{latest_version}{RESET}"
                        )
                    except Exception as e:
                        print(f"{RED}Qualysdk update failed: {type(e).__name__}{RESET}")
                        exit(1)
                    exit(0)
                else:
                    print(f"{RED}Upgrade cancelled.{RESET}")
                    exit(0)
            exit(0)
        else:
            print(f"✅ {GREEN}Qualysdk is up to date (v{current_version}).{RESET}")
            exit(0)


if __name__ == "__main__":
    main()
