"""
basic.py - contains the BasicAuth class, which handles API endpoints that require basic authentication
"""

from dataclasses import dataclass, field
from typing import Literal, Union

from requests import get

from .base import BaseAuthentication
from ..exceptions import AuthenticationError


@dataclass
class BasicAuth(BaseAuthentication):
    """
    BasicAuth - handles API endpoints that require basic authentication

    Subclass of .base.BaseAuthentication - provides the basic authentication for the API

    Attributes:
    ```
    platform: str - the platform for the basic authentication. Defaults to "qg3", but can be "qg[1-4]"
    ```
    Other attributes are inherited from BaseAuthentication - AKA username, password, token, and auth_type
    """

    platform: Literal["qg1", "qg2", "qg3", "qg4"] = field(default="qg3", init=True)

    def __post_init__(self) -> None:
        """
        Post-init method to determine auth_type based on if a token is passed or not.
        """
        if self.platform not in ["qg1", "qg2", "qg3", "qg4"]:
            raise ValueError("Platform must be one of 'qg1', 'qg2', 'qg3', or 'qg4'.")

        super().__post_init__()
        self.validate_type()
        # self.auth_type = "basic"
        if self.auth_type == "basic":  # account for TokenAuth
            self.test_login()

    def __str__(self) -> str:
        """
        String representation of the authentication object.
        """
        return f"Basic authentication object for {self.username} on {self.platform} platform."

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

        (
            print(
                f"Testing login for {self.username} on {self.platform} platform via {self.auth_type} authentication."
            )
            if not return_ratelimit
            else None
        )

        if self.platform != "qg1":
            url = f"https://qualysapi.{self.platform}.apps.qualys.com/msp/about.php"
        else:
            url = "https://qualysapi.qualys.com/msp/about.php"

        """Requires basic auth. JWT is not supported for this endpoint."""
        r = get(url, auth=(self.username, self.password))

        if r.status_code != 200:
            raise AuthenticationError(
                f"Failed to authenticate. Requests reporting: {r.text}"
            )

        rl = {
            # "X-RateLimit-Remaining": int(r.headers["X-RateLimit-Remaining"]),
            "X-RateLimit-Limit": int(r.headers["X-RateLimit-Limit"]),
            "X-Concurrency-Limit-Limit": int(r.headers["X-Concurrency-Limit-Limit"]),
            # "X-RateLimit-ToWait-Sec": int(r.headers["X-RateLimit-ToWait-Sec"]),
        }
        print(f"Success. Rate limit details: {rl}") if not return_ratelimit else None
        return rl if return_ratelimit else None

    def get_ratelimit(self) -> dict:
        """
        Return ratelimit details for the API.
        """
        return self.test_login(return_ratelimit=True)
