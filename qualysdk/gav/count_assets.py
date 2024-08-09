"""
count_assets.py - contains the count_assets function for the Global AssetView API (GAV) module.

for a full list of Qualys QQL filters, see: https://docs.qualys.com/en/gav/2.18.0.0/search/how_to_search.htm
"""

from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import *


def count_assets(auth: TokenAuth, **kwargs) -> dict:
    """
    Count assets in the Global AssetView API based on a QQL filter.

    Params:
        auth (TokenAuth): The authentication object.

    :Kwargs:
        filter (str): The Qualys QQL filter to use.
        lastSeenAssetId (int): The last seen asset ID.
        lastModifiedDate (str): The last modified date.

    Returns:
        dict: The response from the API.
    """
    # despite the fact that this is a POST request, we still need to send stuff as a parameter
    # because Qualys is Qualys.

    # make the request:
    response = call_api(auth=auth, module="gav", endpoint="count_assets", params=kwargs)

    # parse the response:
    return response.json()
