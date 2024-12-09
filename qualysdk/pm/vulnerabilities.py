"""
Contains the lookup_cves function for Patch Management.
"""

from typing import Union, overload
from threading import Thread, Lock
from queue import Queue

from .data_classes.PMVulnerability import PMVulnerability

from ..base.base_list import BaseList
from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import QualysAPIError


def _thread_worker(
    queue: Queue, responses: BaseList, auth: TokenAuth, LOCK: Lock
) -> None:
    """
    Backend thread worker for lookup_cves.

    Chunks up QIDs in the queue into equal parts (or as close as possible),
    then sends the chunks to the API for processing.

    Should not be called directly.

    Args:
        queue (Queue): The queue of QIDs.
        responses (BaseList): The list of responses.
        auth (TokenAuth): The authentication object.
        LOCK (Lock): The threading lock.

    Returns:
        None
    """

    while not queue.empty():
        qids = []
        for i in range(1000):
            if not queue.empty():
                qids.append(queue.get())

        payload = {"qids": qids}

        response = call_api(
            auth=auth,
            module="pm",
            endpoint="vulnerabilities",
            jsonbody=payload,
        )
        if response.status_code not in range(200, 299):
            raise QualysAPIError(response.text)
        with LOCK:
            responses.extend(
                [PMVulnerability.from_dict(qid) for qid in response.json()]
            )


@overload
def lookup_cves(
    auth: TokenAuth, qids: list[Union[str, int]], threads: int = 5
) -> BaseList[PMVulnerability]:
    ...


@overload
def lookup_cves(
    auth: TokenAuth, qids: Union[str, int], threads: int = 5
) -> BaseList[PMVulnerability]:
    ...


def lookup_cves(
    auth: TokenAuth, qids: Union[str, int, list[Union[str, int]]], threads: int = 5
) -> BaseList[PMVulnerability]:
    """
    Look up CVE IDs, severity, title, type,
    & detectedDate associated with a given QID(s).

    Args:
        auth (TokenAuth): The authentication object.
        qids (Union[str, int, list[Union[str, int]]]): The QID(s) to look up.
        threads (int): The number of threads to use. Default is 5. Value is ignored if the number of QIDs is less than 1K.

    Returns:
        BaseList[PMVulnerability]: The list of vulnerabilities.
    """

    if not isinstance(qids, (list, BaseList)):
        # If the user passed a comma-separated string, split it:
        if isinstance(qids, str) and "," in qids:
            qids = qids.replace(" ", "").split(",")
        else:
            qids = [qids]

    payload = {"qids": qids}

    # Handle larger qid lists:
    if len(qids) >= 1000 and (isinstance(threads, int) and threads > 1):
        responses = BaseList()
        queue = Queue()
        LOCK = Lock()
        threadCount = 0  # Name the threads
        threadList = []
        for qid in qids:
            queue.put(qid)

        for i in range(threads):
            threadList.append(
                Thread(
                    target=_thread_worker,
                    kwargs={
                        "queue": queue,
                        "responses": responses,
                        "auth": auth,
                        "LOCK": LOCK,
                    },
                )
            )
            threadCount += 1
        [thread.start() for thread in threadList]
        [thread.join() for thread in threadList]
        return responses

    else:
        response = call_api(
            auth=auth,
            module="pm",
            endpoint="vulnerabilities",
            jsonbody=payload,
        )

        if response.status_code not in range(200, 299):
            raise QualysAPIError(response.text)

        return BaseList([PMVulnerability.from_dict(qid) for qid in response.json()])
