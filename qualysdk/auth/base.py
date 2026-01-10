"""
base.py - base authentication class for qualysdk
"""

import json
from dataclasses import dataclass, field
from typing import Optional, Literal

from .platform_picker import PlatformPicker
from ..exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    InvalidAuthTypeError,
)


@dataclass
class BaseAuthentication:
    """
    Base class for authentication with qualysdk.

    Attributes:
    ```
    username: str - the username for the API
    password: str - the password for the API
    token: Optional[str] - the token for the API (if using token authentication)
    auth_type: Literal["basic", "token"] - the type of authentication being used
    platform: Optional[str] - the platform for the authentication. Defaults to None, but can be any value in the PlatformPicker class.
    override_platform: Optional[dict] - a dictionary containing custom platform URLs. If provided, this will override the platform attribute. Formatted like:
    {
        "api_url": str,
        "gateway_url": str,
        "qualysguard_url": str
    }
    ```
    """

    username: str
    password: str = field(
        repr=False
    )  # Hide password from repr. If the user wants to see it that badly, they can do so manually with the password attribute.
    token: Optional[str] = field(default=None, repr=False)  # same goes for token ^^
    auth_type: Literal["basic", "token"] = field(init=False)
    platform: Optional[str] = field(default=None, init=True)
    override_platform: Optional[dict[str, str]] = field(default=None, init=True)

    def __post_init__(self) -> None:
        """
        Post-init method to determine auth_type based on if a token is passed or not.
        """
        if self.token is None:
            self.auth_type = "basic"
        else:
            self.auth_type = "token"
        if self.override_platform and isinstance(self.override_platform, dict):
            if not all(  # Ensure all required keys are present and their values are strings:
                key in self.override_platform
                for key in ["api_url", "gateway_url", "qualysguard_url"]
            ) or not all(
                isinstance(self.override_platform[key], str)
                for key in ["api_url", "gateway_url", "qualysguard_url"]
            ):
                raise ValueError(
                    f"override_platform must contain 'api_url', 'gateway_url', and 'qualysguard_url' keys. Provided keys: {list(self.override_platform.keys())}"
                )
            print(f"Using overridden platform URLs for {self.username}.")
            self.platform = "CUSTOM"  # set platform to CUSTOM if override_platform is used
            # ensure each url starts with https://
            for key in self.override_platform:
                # Some basic sanitation:
                self.override_platform[key] = (
                    self.override_platform[key].strip().replace("http://", "https://")
                )
                if not self.override_platform[key].startswith("https://"):
                    self.override_platform[key] = "https://" + self.override_platform[key]
                if self.override_platform[key].endswith("/"):
                    self.override_platform[key] = self.override_platform[key][:-1]

        elif self.platform not in PlatformPicker.urls["api_urls"]:
            raise ValueError(
                f"Platform must be one of {list(PlatformPicker.urls['api_urls'].keys())} OR overriden with override_platform attribute."
            )

    def __str__(self) -> str:
        """
        String representation of the authentication object.
        """
        return f"Base authentication object for {self.username}"

    def validate_type(self):
        """
        Validate the authentication object.
        """
        if self.auth_type == "basic":
            if self.username is None or self.password is None:
                raise InvalidCredentialsError(
                    "Username and password must be provided for basic authentication."
                )
        elif self.auth_type == "token":
            if self.token is None:
                raise InvalidTokenError("Token must be provided for token authentication.")
        else:
            raise InvalidAuthTypeError("Invalid authentication type. Must be 'basic' or 'token'.")

    def to_dict(self) -> dict:
        """
        Convert the authentication object to a dictionary.
        """
        return {
            "username": self.username,
            "password": self.password,
            "token": self.token,
            "auth_type": self.auth_type,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an authentication object from a dictionary.
        """
        return cls(**data)

    @classmethod
    def from_json_string(cls, data: str):
        """
        Create an authentication object from a JSON string.
        """
        return cls.from_dict(json.loads(data))

    def to_json_string(self, pretty: bool = False) -> str:
        """
        Convert the authentication object to a JSON string.

        Params:
        ```
        pretty: bool (default is False) - whether to pretty print the JSON string or not.
        ```
        """
        return json.dumps(self.to_dict(), indent=4 if pretty else None)

    def __eq__(self, other):
        """
        Equality comparison for authentication objects.
        """
        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """
        Inequality comparison for authentication objects.
        """
        return self.to_dict() != other.to_dict()
