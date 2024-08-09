"""
get_asset.py - get a specific asset from the Global AssetView API via its asset ID.
"""

from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *
from .hosts import Host


def get_asset(auth: TokenAuth, **kwargs) -> Host:
    """
    Get a specific host from the Global AssetView API.

    Params:
        auth (TokenAuth): The authentication object.

    :Kwargs:
        assetId (int): The asset ID to get.
        lastSeenAssetId (int): The last seen asset ID.
        lastModifiedDate (str): The last modified date.

    Returns:
        Host: The Host object.
    """
    # despite the fact that this is a POST request, we still need to send stuff as a parameter
    # because Qualys is Qualys.

    # make the request:
    response = call_api(auth=auth, module="gav", endpoint="get_asset", params=kwargs)

    # check for 204 response:
    if response.status_code == 204:
        raise ValueError(f"No asset found with ID {kwargs['assetId']}.")

    # parse the response:
    j = response.json()

    return Host(**j["assetListData"]["asset"][0])
