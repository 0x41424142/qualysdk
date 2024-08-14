"""
qualysdk - Qualys API SDK for Python

This package aims to make it easier to interact with the Qualys API across all of the different modules that Qualys provides.
"""

from .help import schema_query
from .auth import BasicAuth, TokenAuth

from .gav.uber import GAVUber
from . import gav

from .vmdr import query_kb, get_host_list, get_hld
from . import vmdr

from .sql import db_connect

# surprise!
__surprise__ = b"\xe2\x9c\xa8\xe2\x9c\xa8\xe2\x9c\xa8 Have a great day!".decode("utf-8")
