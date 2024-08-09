"""
Authentication submodule for qualysdk. Contains classes for handling authentication.

Base class is Authentication

There are two subclasses of Authentication:
- BasicAuth
- TokenAuth

BasicAuth handles HTTP Basic Authentication, while TokenAuth handles JWT token authentication.
"""

from .basic import BasicAuth
from .token import TokenAuth
