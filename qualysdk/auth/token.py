"""
token.py - contains the TokenAuth class, which handles API endpoints that require JWT authentication
"""

from dataclasses import dataclass, field
from datetime import datetime

from requests import post

from .basic import BasicAuth
from ..exceptions import AuthenticationError


@dataclass
class TokenAuth(BasicAuth):
    """
    TokenAuth - handles API endpoints that require JWT authentication.
    This class will take the username, password, and platform attributes from BasicAuth and use them to generate a JWT token via the Qualys JWT-generatio API.

    Attributes:
    ```
    token: str - the JWT token for the API
    generated_on: datetime - the datetime the token was generated. Tokens are valid for 4 hours.
    ```
    Subclass of .basic.BasicAuth - provides the JWT authentication for the API
    """

    # JWT token
    token: str = field(init=False, repr=False)
    generated_on: datetime = field(init=False, default=datetime)

    def __post_init__(self):
        """
        generates the JWT token for the API
        """
        self.auth_type = "token"
        self.token = "placeholder"
        super().__post_init__()
        self.token = self.get_token()

    def get_token(self) -> str:
        """
        generates the JWT token from the Qualys API
        """
        url = f"https://gateway.{self.platform}.apps.qualys.com/auth"

        payload = {
            "username": self.username,
            "password": self.password,
            "permissions": "true",
            "token": "true",
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        print(f"Generating token for {self.username} on {self.platform} platform.")

        r = post(url, headers=headers, data=payload)

        if r.status_code != 201:
            raise AuthenticationError(
                f"Failed to generate token. Requests reporting: {r.text}"
            )
        print("Success.")
        self.generated_on = datetime.now()
        return r.text

    def as_header(self) -> dict:
        """
        returns the headers for the API request
        """
        return {"Authorization": f"Bearer {self.token}"}

    @classmethod
    def from_dict(cls, data: dict):
        """
        provided the dictionary keys 'username', 'password', and 'platform' are present,
        creates a TokenAuth object from the dictionary
        """
        if all(key in data for key in ["username", "password"]):
            return cls(data["username"], data["password"])
        else:
            raise AuthenticationError(
                "Missing required keys 'username' or 'password' in dictionary."
            )
