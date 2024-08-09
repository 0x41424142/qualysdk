"""
help.py - Gives help on the different endpoints and what to expect from them.
"""

from json import dumps
from typing import Union

from .base.call_schema import CALL_SCHEMA


def schema_query(
    module: str, endpoint: str = None, pretty: bool = False
) -> Union[str, dict]:
    """
    Using the CALL_SCHEMA dictionary, this function will return the information for
    either a qualys module as a whole or a specific endpoint within a module.

    Params:
        module (str): The module to get help for.
        endpoint (str) [optional]: The endpoint to get help for.
        pretty (bool) [optional]: Whether to return the information as a string or as a dictionary. [False = return dict, True = return indented str]
    """

    module = module.lower()
    endpoint = endpoint.lower() if endpoint is not None else None

    # check if the module is in the CALL_SCHEMA:
    if module not in CALL_SCHEMA.keys():
        raise ValueError(
            f"Invalid module {module}. Available modules are: {CALL_SCHEMA.keys()}"
        )

    # if the endpoint is not provided, return the entire module schema:
    if endpoint is None:
        if pretty:
            return print(dumps(CALL_SCHEMA[module], indent=4))
        else:
            return CALL_SCHEMA[module]

    # if the endpoint is provided, return the schema for that endpoint:
    if endpoint not in CALL_SCHEMA[module].keys():
        raise ValueError(f"Invalid endpoint {endpoint} for module {module}.")

    if pretty:
        return print(dumps(CALL_SCHEMA[module][endpoint], indent=4))
    else:
        return CALL_SCHEMA[module][endpoint]
