"""
Contains functions to pull stats on control IDs on resources, 
evaluations per account, and resources evaluated for a control.
"""

from typing import Literal, Union

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.Evaluation import Evaluation


def get_evaluation(
    auth: BasicAuth,
    provider: Literal["aws", "azure"],
    controlId: Union[str, int],
    connectorId: str,
    resourceId: str,
) -> Evaluation:
    """
    Get datetime statistics on a single control ID on a single resource ID in a single cloud provider account.

    Args:
        auth (BasicAuth): The authentication object.
        provider (str): The cloud provider to get the control stats from.
        controlId (str): The control ID to get stats for.
        connectorId (str): The connector ID to get stats for.
        resourceId (str): The resource ID to get stats for.

    Returns:
        Evaluation: The response from the API as an Evaluation object.
    """

    # Check if the provider is valid
    provider = provider.lower()
    if provider not in ["aws", "azure"]:
        raise ValueError("Invalid provider. Must be 'aws' or 'azure'.")

    # Make the API call
    response = call_api(
        auth=auth,
        module="cloudview",
        endpoint="get_control_stats_by_resouce",
        params={
            "cloudprovider": provider,
            "controlid": controlId,
            "connectorid": connectorId,
            "resourceId": resourceId,
        },
    )

    if not response.json():
        raise QualysAPIError("No data found for the control on the resource.")

    return Evaluation.from_dict(response.json())
