"""
basic.py - contains the BasicAuth class, which handles API endpoints that require basic authentication
"""

from dataclasses import dataclass, field
from typing import Literal, Union

from requests import get

from .base import BaseAuthentication
from ..exceptions import AuthenticationError
from .platform_picker import PlatformPicker


@dataclass
class BasicAuth(BaseAuthentication):
    """
    BasicAuth - handles API endpoints that require basic authentication

    override_platform is a dictionary containing custom platform URLs. If provided, this will override the platform attribute. Formatted like:

    {
        "api_url": str,
        "gateway_url": str,
        "qualysguard_url": str
    }
    Attributes:
    ```
    platform: str - the platform for the basic authentication. Defaults to "qg3", but can be any value in the PlatformPicker class.
    ```
    Other attributes are inherited from BaseAuthentication - AKA username, password, token, platform_override and auth_type
    """

    platform: Literal[
        "qg1", "qg2", "qg3", "qg4", "eu1", "eu2", "eu3", "in1", "ca1", "ae1", "uk1", "au1", "ksa1"
    ] = field(default="qg3", init=True)

    def __post_init__(self) -> None:
        """
        Post-init method to determine auth_type based on if a token is passed or not.
        """
        super().__post_init__()
        self.validate_type()
        # self.auth_type = "basic"
        if self.auth_type == "basic":  # account for TokenAuth
            self.test_login()

    def __str__(self) -> str:
        """
        String representation of the authentication object.
        """
        if not self.override_platform:
            return f"Basic authentication object for {self.username} on {self.platform} platform."
        else:
            return f"Basic authentication object for {self.username} on overridden {self.override_platform} platform."

    def to_dict(self) -> dict:
        """
        Convert the authentication object to a dictionary.
        """
        return {
            "username": self.username,
            "password": self.password,
            "token": self.token,
            "auth_type": self.auth_type,
            "platform": self.platform,
            "override_platform": self.override_platform,
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def test_login(self, return_ratelimit: bool = False) -> Union[dict, None]:
        """
        Get the rate limit for the API.

        Params:
        ```
        return_ratelimit: bool (default is False) - whether to return the rate limit details as a dict or not.
        You should call get_ratelimit() to get the rate limit details.
        ```

        Returns:
        ```
        {
            "X-RateLimit-Remaining": int,
            "X-RateLimit-Limit": int,
            "X-Concurrency-Limit-Limit": int,
            "X-RateLimit-ToWait-Sec": int
        }
        """
        if not self.override_platform:
            print(f"Using platform: {self.platform}") if not return_ratelimit else None
        else:
            print(
                f"Using overridden platform URL {self.override_platform['api_url']}"
            ) if not return_ratelimit else None

        url = (
            self.override_platform["api_url"]
            if self.override_platform
            else PlatformPicker.get_api_url(self.platform)
        ) + "/msp/about.php"

        """Requires basic auth. JWT is not supported for this endpoint."""
        r = get(url, auth=(self.username, self.password))

        if r.status_code != 200:
            raise AuthenticationError(f"Failed to authenticate. Requests reporting: {r.text}")

        rl = {
            "X-RateLimit-Limit": int(r.headers["X-RateLimit-Limit"]),
            "X-Concurrency-Limit-Limit": int(r.headers["X-Concurrency-Limit-Limit"]),
        }
        print(f"Success. Rate limit details: {rl}") if not return_ratelimit else None
        return rl if return_ratelimit else None

    def get_ratelimit(self) -> dict:
        """
        Return ratelimit details for the API.
        """
        return self.test_login(return_ratelimit=True)
