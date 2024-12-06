"""
Contains get_version function for Patch Management
"""

from ..base.call_api import call_api
from ..auth.token import TokenAuth
from ..exceptions.Exceptions import QualysAPIError


def get_version(auth: TokenAuth) -> str:
    """
    Returns the version of Patch Management
    """
    result = call_api(
        auth,
        "pm",
        "get_version",
    )

    if result.status_code != 200:
        raise QualysAPIError(result.json())

    return result.json().get("appVersion")
