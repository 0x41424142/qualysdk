"""
CLI script to quickly perform Patch Management
(PM) operations using qualysdk.
"""

from argparse import ArgumentParser, Namespace

from qualysdk import TokenAuth, write_excel, BaseList
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
        case "lookup_cves":
            result = lookup_cves(auth, args.qids, args.threads)
        case "get_patches":
            result = get_patches(auth, args.platform, **kwargs)
        case "get_patch_count":
            result = get_patch_count(auth, args.platform, **kwargs)
        case "get_assets":
            result = get_assets(auth, args.platform, **kwargs)
        case "get_patch_catalog":
            result = get_patch_catalog(auth, args.patch_id, args.os, **kwargs)
        case _:
            raise ValueError(f"Invalid endpoint: {endpoint}.")

    # if get_patch_count was called, the return is just an int. We can
    # write this to a TXT:
    if endpoint == "get_patch_count":
        if not args.output.endswith(".txt"):
            args.output += ".txt"
        with open(args.output, "w") as f:
            f.write(str(result))
        print(f"Results written to {args.output}")
        return

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

    # lookup_cves action:
    lookup_cves_parser = subparsers.add_parser(
        "lookup_cves", help="Look up CVEs for a given QID(s)."
    )

    lookup_cves_parser.add_argument(
        "-q",
        "--qids",
        help="Specify the QID(s) to look up. Can be used multiple times",
        type=str,
        required=True,
        action="append",
    )

    lookup_cves_parser.add_argument(
        "-t",
        "--threads",
        help="Specify the number of threads to use. Default is 5",
        type=int,
        default=5,
    )

    lookup_cves_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="pm_cves.xlsx",
    )

    get_patches_parser = subparsers.add_parser(
        "get_patches", help="Get patches for a given platform."
    )

    get_patches_parser.add_argument(
        "--os",
        help="Specify the platform to get patches for. Default is 'all'",
        type=str,
        default="all",
        choices=["all", "windows", "linux"],
    )

    get_patches_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="pm_patches.xlsx",
    )

    get_patches_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    get_patch_count_parser = subparsers.add_parser(
        "get_patch_count",
        help="Get the number of patches available for a platform according to query and havingQuery.",
    )

    get_patch_count_parser.add_argument(
        "--os",
        help="Specify the operating system to get patches for. Default is 'Windows'",
        type=str,
        default="windows",
        choices=["windows", "linux"],
    )

    get_patch_count_parser.add_argument(
        "--query",
        help="Specify a patch QQL query",
        type=str,
        default=None,
    )

    get_patch_count_parser.add_argument(
        "--havingQuery",
        help="Specify a PM asset QQL query",
        type=str,
        default=None,
    )

    get_patch_count_parser.add_argument(
        "-o",
        "--output",
        help="Output txt file to write results to. Default is 'pm_patch_count.txt'",
        type=str,
        default="pm_patch_count.txt",
    )

    get_assets_parser = subparsers.add_parser(
        "get_assets", help="Get assets for a given platform."
    )

    get_assets_parser.add_argument(
        "--os",
        help="Specify the platform to get assets for. Default is 'all'",
        type=str,
        default="all",
        choices=["all", "windows", "linux"],
    )

    get_assets_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="pm_assets.xlsx",
    )

    get_assets_parser.add_argument(
        "--kwarg",
        help="Specify a keyword argument to pass to the action. Can be used multiple times",
        action="append",
        nargs=2,
        metavar=("key", "value"),
    )

    get_patch_catalog_parser = subparsers.add_parser(
        "get_patch_catalog", help="Get patch catalog entries for a given platform."
    )

    get_patch_catalog_parser.add_argument(
        "--os",
        help="Specify the platform to get patches for. Default is 'Windows'",
        type=str,
        default="windows",
        choices=["windows", "linux"],
    )

    get_patch_catalog_parser.add_argument(
        "-o",
        "--output",
        help="Output xlsx file to write results to",
        type=str,
        default="pm_patch_catalog.xlsx",
    )

    get_patch_catalog_parser.add_argument(
        "--patch-id",
        help="Specify the patch ID to get catalog entries for. Can be used multiple times",
        type=str,
        required=True,
        action="append",
    )

    get_patch_catalog_parser.add_argument(
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
        case "lookup_cves":
            args.kwarg = {}  # No kwargs for this endpoint
            # look for a string of QIDs separated by commas.
            # if found, split it into a list of QIDs:
            for i, qid in enumerate(args.qids):
                if "," in qid:
                    args.qids.pop(i)
                    args.qids.extend(qid.split(","))
            # Check for any non-numeric chars. If found, remove them:
            for i, qid in enumerate(args.qids):
                args.qids[i] = "".join([c for c in qid if c in "1234567890"])
            cli_fn(auth=auth, args=args, endpoint="lookup_cves")
        case "get_patches":
            args.platform = args.os
            cli_fn(auth=auth, args=args, endpoint="get_patches")
        case "get_assets":
            args.platform = args.os
            cli_fn(auth=auth, args=args, endpoint="get_assets")
        case "get_patch_count":
            args.kwarg = {}  # No kwargs for this endpoint
            args.platform = args.os
            cli_fn(auth=auth, args=args, endpoint="get_patch_count")
        case "get_patch_catalog":
            args.platform = args.os
            cli_fn(auth=auth, args=args, endpoint="get_patch_catalog")
        case _:
            parser.print_help()
            exit(1)


if __name__ == "__main__":
    main()
