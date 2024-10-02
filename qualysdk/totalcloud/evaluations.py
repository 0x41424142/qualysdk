"""
Contains functions to pull stats on control IDs on resources, 
evaluations per account, and resources evaluated for a control.
"""

from typing import Literal, Union

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.Evaluation import Evaluation, AccountLevelEvaluation
from .data_classes.Controls import AccountLevelControl


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


def get_account_evaluation(
    auth: BasicAuth,
    provider: Literal["aws", "azure"],
    accountId: Union[int, str],
    **kwargs,
) -> BaseList[Evaluation]:
    """
    Returns a list of control evaluations for a cloud account.

    Args:
        auth (BasicAuth): The authentication object.
        provider (str): The cloud provider to get the control stats from.
        accountId (str): The account/subscription ID to get stats for.

    ## Kwargs:
        filter (Optional[str]): Filter returned control evaluations based on Qualys ["Posture"](https://docs.qualys.com/en/cloudview/latest/search_tips/search_ui_monitor.htm) QQL.

    Returns:
        BaseList[Evaluation]: List of control evaluations for the account.
    """

    # Check if the provider is valid
    provider = provider.lower()
    if provider not in ["aws", "azure"]:
        raise ValueError("Invalid provider. Must be 'aws' or 'azure'.")

    params = {"cloudprovider": provider, "placeholder": accountId}

    if kwargs and kwargs.get("filter"):
        params["filter"] = kwargs.get("filter")

    responses = BaseList()

    # Make the API call
    response = call_api(
        auth=auth, module="cloudview", endpoint="get_account_evaluation", params=params
    )

    j = response.json()

    if not j:
        raise QualysAPIError("No data found for the requested account ID.")

    if j.get("empty"):
        print(f"No data found for account {accountId}")
        return responses

    # Normalize to list
    if isinstance(j["content"], dict):
        j["content"] = [j["content"]]

    for resp in j["content"]:
        responses.append(AccountLevelControl.from_dict(resp))

    return responses


def get_resources_evaluated_by_control(
    auth: BasicAuth,
    provider: Literal["aws", "azure"],
    accountId: Union[str, int],
    controlId: Union[str, int],
    **kwargs,
) -> BaseList[str]:
    """
    Get a list of resources evaluated for a specific control ID in a cloud account.

    Args:
        auth (BasicAuth): The authentication object.
        provider (str): The cloud provider to get the control stats from.
        accountId (str): The account/subscription ID to get stats for.
        controlId (str): The control ID to get stats for.

    ## Kwargs:
        filter (Optional[str]): Filter returned resources based on Qualys QQL defined [here](https://docs.qualys.com/en/cloudview/latest/search_tips/search_ui_monitor.htm).

    Returns:
        BaseList[str]: List of resource IDs evaluated for the control.
    """

    # Check if the provider is valid
    provider = provider.lower()
    if provider not in ["aws", "azure"]:
        raise ValueError("Invalid provider. Must be 'aws' or 'azure'.")

    params = {
        "cloudprovider": provider,
        "placeholder": accountId,
        "controlid": controlId,
    }

    if kwargs and kwargs.get("filter"):
        params["filter"] = kwargs.get("filter")

    responses = BaseList()

    # Make the API call
    response = call_api(
        auth=auth,
        module="cloudview",
        endpoint="get_resources_evaluated_by_control",
        params=params,
    )

    j = response.json()

    if not j:
        raise QualysAPIError("No data found for the requested account ID.")

    if j.get("empty"):
        print(f"No data found for account {accountId}")
        return responses

    # Normalize to list
    if isinstance(j["content"], dict):
        j["content"] = [j["content"]]

    for resp in j["content"]:
        responses.append(AccountLevelEvaluation.from_dict(resp))

    return responses
