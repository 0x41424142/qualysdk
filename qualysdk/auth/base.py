"""
base.py - base authentication class for qualysdk
"""

import json
from dataclasses import dataclass, field
from typing import Optional, Literal, Self


from ..exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    InvalidAuthTypeError,
)


@dataclass
class BaseAuthentication:
    """
    Base class for authentication with qualysdk.
    """

    username: str
    password: str = field(
        repr=False
    )  # Hide password from repr. If the user wants to see it that badly, they can do so manually with the password attribute.
    token: Optional[str] = field(default=None, repr=False)  # same goes for token ^^
    auth_type: Literal["basic", "token"] = field(init=False)

    def __post_init__(self) -> None:
        """
        Post-init method to determine auth_type based on if a token is passed or not.
        """
        if self.token is None:
            self.auth_type = "basic"
        else:
            self.auth_type = "token"

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
                raise InvalidTokenError(
                    "Token must be provided for token authentication."
                )
        else:
            raise InvalidAuthTypeError(
                "Invalid authentication type. Must be 'basic' or 'token'."
            )

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
