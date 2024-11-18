"""
CLI script to quickly perform Patch Management
(PM) operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import TokenAuth, write_excel, BaseList, write_json
from qualysdk.pm import *


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
        case "list_jobs":
            result = list_jobs(auth, **kwargs)
        case "get_job_results":
            result = get_job_results(auth, args.job_id, **kwargs)
        case "get_job_runs":
            result = get_job_runs(auth, args.job_id, **kwargs)
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
        description="CLI script to quickly perform Patch Management (PM) operations using qualysdk"
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
    list_jobs_parser = subparsers.add_parser("list_jobs", help="Get a list of PM jobs.")
    list_jobs_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="pm_jobs.xlsx",
    )
    list_jobs_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    job_results_parser = subparsers.add_parser(
        "get_job_results", help="Get results for a PM job."
    )
    job_results_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="pm_job_{JOB_ID}_results.xlsx",
    )
    job_results_parser.add_argument(
        "-j",
        "--job-id",
        help="Specify the job ID to get results for. Can be used multiple times",
        type=str,
        required=True,
        action="append",
    )
    job_results_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    job_runs_parser = subparsers.add_parser(
        "get_job_runs", help="Get runs for a PM job."
    )
    job_runs_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="pm_job_{JOB_ID}_runs.xlsx",
    )
    job_runs_parser.add_argument(
        "-j",
        "--job-id",
        help="Specify the job ID to get runs for",
        type=str,
        required=True,
    )
    job_runs_parser.add_argument(
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
        case "list_jobs":
            cli_fn(auth=auth, args=args, endpoint="list_jobs")
        case "get_job_results":
            if len(args.job_id) > 1:
                args.output = args.output.replace("{JOB_ID}", "multiple_jobs")
            else:
                args.output = args.output.replace("{JOB_ID}", args.job_id[0])
            cli_fn(auth=auth, args=args, endpoint="get_job_results")
        case "get_job_runs":
            args.output = args.output.replace("{JOB_ID}", args.job_id)
            cli_fn(auth=auth, args=args, endpoint="get_job_runs")
        case _:
            parser.print_help()
            exit(1)


if __name__ == "__main__":
    main()
