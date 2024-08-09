"""
Exceptions.py - Custom Exceptions for package.
"""


class AuthenticationError(Exception):
    """
    Basic exception class for qualysdk when dealing with authentication.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidCredentialsError(AuthenticationError):
    """
    Exception for when credentials are invalid.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidTokenError(AuthenticationError):
    """
    Exception for when token is invalid.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidAuthTypeError(AuthenticationError):
    """
    Exception for when auth type is invalid.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AuthTypeMismatchError(AuthenticationError):
    """
    Exception for when auth type is invalid.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidEndpointError(Exception):
    """
    Exception for when endpoint is invalid.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class QualysAPIError(Exception):
    """
    Basic exception class for qualysdk.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
