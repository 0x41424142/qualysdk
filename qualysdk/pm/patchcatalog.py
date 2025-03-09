"""
Contains user-facing functions for interacting with the /pm/v*/patchcatalog* endpoints
"""

from typing import Union, Literal, overload
from queue import Queue
from threading import Thread, Lock
from datetime import datetime

from .data_classes.CatalogPatch import CatalogPatch, PackageDetail
from .data_classes.AssociatedProduct import AssociatedProduct
from .data_classes.ProductVulnCount import ProductVulnCount
from ..base.base_list import BaseList
from ..auth.token import TokenAuth
from ..base.call_api import call_api
from ..exceptions.Exceptions import QualysAPIError


@overload
def get_patch_catalog(
    auth: TokenAuth,
    patchId: Union[int, str],
    platform: Literal["windows", "linux"] = "windows",
    **kwargs,
) -> BaseList[CatalogPatch]:
    ...


@overload
def get_patch_catalog(
    auth: TokenAuth,
    patchId: Union[BaseList[str, int], list[str, int]],
    platform: Literal["windows", "linux"] = "windows",
    **kwargs,
) -> BaseList[CatalogPatch]:
    ...


def get_patch_catalog(
    auth: TokenAuth,
    patchId: str,
    platform: Literal["windows", "linux"] = "windows",
    **kwargs,
) -> BaseList[CatalogPatch]:
    """
    Retrieve details on patches available for a given platform by patch UUID.

    NOTE: You must call this API with EITHER windows OR linux patch UUID(s), not both.

    Args:
        auth (TokenAuth): The authentication object.
        platform (Literal['windows', 'linux']): The platform to filter by. Default is 'windows'.

    ## Kwargs:

        - attributes (str): A comma-separated string of attributes to return.

    Returns:
        BaseList[CatalogPatch]: A BaseList of CatalogPatch objects.
    """

    platform = platform.title()

    if platform not in ["Windows", "Linux"]:
        raise ValueError("platform must be 'windows' or 'linux'")

    if isinstance(patchId, str) and "," in patchId:
        patchId = patchId.replace(" ", "").split(",")

    if not isinstance(patchId, (list, BaseList)):
        patchId = [patchId]

    params = {
        "platform": platform,
    }

    if "attributes" in kwargs:
        params["attributes"] = kwargs["attributes"]

    results = BaseList()
    pulled = 0

    # Set up chunking
    while True:
        if not patchId:
            # After loop has run its course,
            # list will be empty and we can break
            break

        # call api with a chunk of 1K
        result = call_api(
            auth,
            "pm",
            "get_patch_catalog",
            jsonbody={"patchUuid": patchId[:1000]},
            params=params,
        )

        if result.status_code not in range(200, 299):
            raise QualysAPIError(result.json())

        # Remove processed patchIds from the list:
        patchId = patchId[1000:]

        j = result.json()

        for catalog_entry in j:
            results.append(CatalogPatch(**catalog_entry))

        pulled += 1
        if pulled % 5 == 0:
            print(f"Pulled {pulled} chunks of 1K patch catalog entries")

    return results


def _get_products_or_packages_in_patch(
    auth: TokenAuth, endpoint: Literal["products", "packages"], **kwargs
):
    """
    Backend function for user-facing get_packages_in_linux_patch
    and get_products_in_windows_patch functions.

    Args:
        auth (TokenAuth): The authentication object.
        endpoint (Literal['products', 'packages']): The endpoint to call.

    ## Kwargs:

        - any other kwargs from the calling function

    Returns:
        response (requests.Response): The response object.
    """

    if endpoint not in ["products", "packages"]:
        raise ValueError(f"endpoint must be 'products' or 'packages', not {endpoint}")

    if endpoint == "products":
        kwargs["placeholder"] = kwargs.pop("patchId")
        return call_api(
            auth,
            "pm",
            "get_products_in_windows_patch",
            params=kwargs,
        )
    elif endpoint == "packages":
        # Rename patchId to patchUuid. Qualys quirk.
        kwargs["patchUuid"] = kwargs.pop("patchId")
        return call_api(
            auth,
            "pm",
            "get_packages_in_linux_patch",
            params=kwargs,
        )


def _thread_worker(
    auth: TokenAuth,
    endpoint: Literal["products", "packages"],
    patchQueue: Queue,
    responses: BaseList,
    LOCK: Lock,
    tracker: datetime,
    error_flag: bool,
    **kwargs,
):
    """
    Worker function for threading in get_packages_in_linux_patch and get_products_in_windows_patch.

    Args:
        auth (TokenAuth): The authentication object.
        endpoint (Literal['products', 'packages']): The endpoint to call.
        patchQueue (Queue): The queue of patch IDs.
        responses (BaseList): The list to append responses to.
        LOCK (Lock): The threading lock.
        tracker (datetime): The datetime object to track time.
        error_flag (bool): The flag to track errors across threads.

    ## Kwargs:

            - any other kwargs from the calling function
    """

    kwargs = {} if not kwargs else kwargs

    if not kwargs.get("pageNumber") and endpoint == "packages":
        kwargs["pageNumber"] = 0
    try:  # use error_flag to prevent multiple threads from printing the same error. We can also return what we have so far if an error occurs.
        while not patchQueue.empty():
            # We dont need to differentiate the kwarg here, backend will handle it
            if error_flag:
                print("Error flag is set. Returning what was collected so far...")
                return
            kwargs["patchId"] = patchQueue.get_nowait()
            while True:
                response = _get_products_or_packages_in_patch(auth, endpoint, **kwargs)
                if response.status_code not in range(200, 299):
                    if response.text:
                        raise QualysAPIError(response.json())
                    elif response.status_code == 429:
                        raise QualysAPIError(
                            "Qualys has rate limited you. Please try again later."
                        )
                    else:
                        raise QualysAPIError(
                            f"Qualys returned status code {response.status_code}. {response.text}"
                        )
                j = response.json()
                for obj in j:
                    obj["patchId"] = kwargs["patchId"]
                    if endpoint == "products":
                        responses.append(AssociatedProduct(**obj))
                    elif endpoint == "packages":
                        responses.append(PackageDetail(**obj))
                # Or handles initial page number
                if kwargs.get("pageNumber") or kwargs.get("pageNumber") == 0:
                    kwargs["pageNumber"] += 1
                # Kind of a weird if statement admittedly, but we
                # do this to compensate for Windows patches endpoint
                # not having any kwargs, specifically pageNumber/pageSize:
                if (len(j) < kwargs.get("pageSize", 10)) or not j:
                    break
            # Depending on the patches and the len() of their associated
            # patches/products list, this print may fire at inconsistent intervals
            with LOCK:
                # Use lastReportedTime for printing how far we are every ~15 seconds
                if (datetime.now() - tracker).seconds >= 15:
                    print(f"{len(responses)} {endpoint} processed...")
                    tracker = datetime.now()
    except Exception as e:
        with LOCK:
            error_flag = True
            print(f"Error in thread: {e} Returning what was collected so far...")


def validate_threads_and_patches(patchId, threads):
    if type(patchId) not in [str, list, BaseList]:
        raise ValueError("patchId must be a string, list, or BaseList")

    if not isinstance(threads, int) or threads < 1:
        raise ValueError("threads must be an integer greater than 0")

    if isinstance(patchId, str) and "," in patchId:
        patchId = patchId.replace(" ", "").split(",")

    if not isinstance(patchId, (list, BaseList)):
        patchId = [patchId]
    return patchId


@overload
def get_packages_in_linux_patch(
    auth: TokenAuth, patchId: str, threads: int = 5, **kwargs
) -> BaseList[PackageDetail]:
    ...


@overload
def get_packages_in_linux_patch(
    auth: TokenAuth,
    patchId: Union[BaseList[str], list[str]],
    threads: int = 5,
    **kwargs,
) -> BaseList[PackageDetail]:
    ...


def get_packages_in_linux_patch(
    auth: TokenAuth,
    patchId: Union[str, BaseList[str], list[str]],
    threads: int = 5,
    **kwargs,
) -> BaseList[PackageDetail]:
    """
    Get a list of packages associated with a Linux patch.

    Args:
        auth (TokenAuth): The authentication object.
        patchId (Union[str, BaseList[str], list[str]]): The patch ID(s) to retrieve packages for. If a BaseList/list of patch IDs is provided, the SDK will use threading to speed up the process.
        threads (int): The number of threads to use. Default is 5.

    ## Kwargs:

            - filter (str): A filter to apply to the results. Patch QQL is supported.
            - PageNumber (int): The page number to retrieve. The SDK will automatically handle pagination unless page_count = 1, in which case it will return the page you specify.
            - PageSize (int): The number of results to return per page. Used for pagination (the SDK will automatically handle pagination). Default is 10.

    Returns:
        BaseList[PackageDetail]: A list of PackageDetail objects.
    """

    patchId = validate_threads_and_patches(patchId, threads)
    LOCK = Lock()
    patchQueue = Queue()
    timeTracker = datetime.now()
    error_in_thread = False
    for patch in patchId:
        patchQueue.put(patch)
    responses = BaseList()
    threadsList = []
    for i in range(threads):
        t = Thread(
            target=_thread_worker,
            args=(
                auth,
                "packages",
                patchQueue,
                responses,
                LOCK,
                timeTracker,
                error_in_thread,
            ),
            kwargs=kwargs,
            name=f"Linux-Thread-{i}",
        )
        t.start()
        threadsList.append(t)
    for t in threadsList:
        t.join()

    return responses


@overload
def get_products_in_windows_patch(
    auth: TokenAuth,
    patchId: str,
    threads: int = 5,
) -> BaseList[AssociatedProduct]:
    ...


@overload
def get_products_in_windows_patch(
    auth: TokenAuth,
    patchId: Union[BaseList[str], list[str]],
    threads: int = 5,
) -> BaseList[AssociatedProduct]:
    ...


def get_products_in_windows_patch(
    auth: TokenAuth,
    patchId: Union[str, BaseList[str], list[str]],
    threads: int = 5,
) -> BaseList[AssociatedProduct]:
    """
    Get a list of products associated with a Windows patch.

    Args:
        auth (TokenAuth): The authentication object.
        patchId (Union[str, BaseList[str], list[str]]): The patch ID(s) to retrieve products for. If a BaseList/list of patch IDs is provided, the SDK will use threading to speed up the process.
        threads (int): The number of threads to use. Default is 5.

    Returns:
        BaseList[PackageDetail]: A list of PackageDetail objects.
    """

    patchId = validate_threads_and_patches(patchId, threads)
    LOCK = Lock()
    patchQueue = Queue()
    timeTracker = datetime.now()
    error_in_thread = False
    for patch in patchId:
        patchQueue.put(patch)
    responses = BaseList()
    threadsList = []
    for i in range(threads):
        t = Thread(
            target=_thread_worker,
            args=(
                auth,
                "products",
                patchQueue,
                responses,
                LOCK,
                timeTracker,
                error_in_thread,
            ),
            name=f"Windows-Thread-{i}",
        )
        t.start()
        threadsList.append(t)
    for t in threadsList:
        t.join()

    return responses


from typing import Union, List, Literal, overload


@overload
def count_product_vulns(
    auth: TokenAuth,
    severityList: Union[
        Literal["Critical", "Important", "Moderate", "Low", "None"],
        List[Literal["Critical", "Important", "Moderate", "Low", "None"]],
    ] = None,
    tagUUIDs: str = None,
) -> BaseList[ProductVulnCount]:
    ...


@overload
def count_product_vulns(
    auth: TokenAuth,
    severityList: Union[
        Literal["Critical", "Important", "Moderate", "Low", "None"],
        List[Literal["Critical", "Important", "Moderate", "Low", "None"]],
    ] = None,
    tagUUIDs: List[str] = None,
) -> BaseList[ProductVulnCount]:
    ...


def count_product_vulns(
    auth: TokenAuth,
    severityList: Union[
        Literal["Critical", "Important", "Moderate", "Low", "None"],
        List[Literal["Critical", "Important", "Moderate", "Low", "None"]],
    ] = None,
    tagUUIDs: Union[str, List[str]] = None,
) -> BaseList[ProductVulnCount]:
    """
    Get a count of active and fixed product vulnerabilities.

    If no severityList value is passed, all severities will be returned (Critical, Important, Moderate, Low, None).

    Args:
        auth (TokenAuth): The authentication object.
        severityList (Union[str, List[str]]): The severity or severities to filter by.
            Can be a single value or a list of values. For all severities, leave this blank.
        tagUUIDs (Union[str, List[str]]): The tag UUIDs to filter by.

    Returns:
        BaseList[ProductVulnCount]: A list of ProductVulnCount objects.
    """
    # Normalize severityList to a list
    if severityList is None:
        severity_values = ["Critical", "Important", "Moderate", "Low", "None"]
    # check if the string or list contains all of the valid values
    elif isinstance(severityList, str) and set(
        [i.title() for i in severityList.split(",")]
    ) == set(["Critical", "Important", "Moderate", "Low", "None"]):
        severity_values = ["Critical", "Important", "Moderate", "Low", "None"]

    elif isinstance(severityList, (list, BaseList)) and set(severityList) == set(
        ["Critical", "Important", "Moderate", "Low", "None"]
    ):
        severity_values = ["Critical", "Important", "Moderate", "Low", "None"]

    elif isinstance(severityList, str):
        severity_values = [s.title().strip() for s in severityList.split(",")]

    elif isinstance(severityList, (list, BaseList)):
        severity_values = severityList

    else:
        raise ValueError(
            "Invalid severityList format. Must be a string or a list of strings."
        )

    results = BaseList()

    if tagUUIDs and isinstance(tagUUIDs, (list, BaseList)):
        tagUUIDs = ",".join(tagUUIDs)
    elif tagUUIDs and not isinstance(tagUUIDs, str):
        raise ValueError("tagUUIDs must be a string or a list of strings.")

    for severity in severity_values:
        response = call_api(
            auth,
            "pm",
            "count_product_vulns",
            params={"severityList": severity, "tagUUIDs": tagUUIDs},
        )

        if response.status_code not in range(200, 299):
            raise QualysAPIError(response.json())

        for entry in response.json():
            entry["severity"] = severity if severity else "All"
            results.append(ProductVulnCount(**entry))

    return results
