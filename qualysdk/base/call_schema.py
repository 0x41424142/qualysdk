"""
call_schema.py - contains the CALL_SCHEMA lookup for the qualysdk package.

The CALL_SCHEMA dictionary contains the schema for each Qualys API call.
This schema is used to determine what parameters are required for each call and where/how
they should be sent to the API.

To view each module's schema, look in ./call_schemas/
"""

from frozendict import frozendict

from .call_schemas import *

schemas = [
    CLOUDAGENT_SCHEMA,
    CS_SCHEMA,
    GAV_SCHEMA,
    PM_SCHEMA,
    TOTALCLOUD_SCHEMA,
    VMDR_SCHEMA,
    WAS_SCHEMA,
    CERTVIEW_SCHEMA,
    TAGGING_SCHEMA,
]

CALL_SCHEMA = dict()

for s in schemas:
    CALL_SCHEMA.update(s)

CALL_SCHEMA = frozendict(CALL_SCHEMA)
