"""
uber.py - an Uber class that allows for easy access to all GAV API endpoints,
plus some extra functionality such as exporting API results to files/SQL databases.
"""

from typing import Union, Literal

from . import *
from ..base.call_schema import CALL_SCHEMA
from ..auth import *
from ..exceptions.Exceptions import *


class GAVUber:
    """
    The Uber class is a class that allows for easy access to all GAV API endpoints.
    """

    def __init__(self, auth: Union[TokenAuth, BasicAuth]):
        """
        Initialize the Uber class.
        """
        self.NON_ENDPOINTS = ["url_type"]  # may expand over time.. your move, Qualys.
        self.auth = auth
        self.valid_endpoints = [
            i for i in CALL_SCHEMA["gav"].keys() if i not in self.NON_ENDPOINTS
        ]  # grab actual endpoints

        # check if the auth type is valid:
        if self.auth.auth_type not in ["token", "basic"]:
            raise InvalidAuthTypeError(
                f"Invalid auth type: {self.auth.auth_type}. Acceptable auth types are: 'token' or 'basic'."
            )

    def __str__(self) -> str:
        return f"Uber class for GAV API with auth type: {self.auth.auth_type}."

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get(
        self,
        endpoint: Literal[
            "count_assets", "get_all_assets", "get_asset", "query_assets"
        ],
        **kwargs,
    ):
        """
        Call the appropriate endpoint based on passed endpoint.

        Params:
            endpoint (str): The endpoint to call. Must be one of the keys in CALL_SCHEMA["gav"].
            **kwargs: The keyword arguments to pass to the endpoint.

        Returns:
            The response from the API call.
        """

        match endpoint:
            case "count_assets":
                return count_assets(self.auth, **kwargs)
            case "get_all_assets":
                return get_all_assets(self.auth, **kwargs)
            case "get_asset":
                return get_asset(self.auth, **kwargs)
            case "query_assets":
                return query_assets(self.auth, **kwargs)
            case _:
                raise InvalidEndpointError(
                    f"Invalid endpoint: {endpoint}. Acceptable endpoints are: {self.valid_endpoints}."
                )
