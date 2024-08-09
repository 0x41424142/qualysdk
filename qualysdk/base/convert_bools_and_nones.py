"""
convert_bools_and_nones.py - Contains functions to convert bools and Nones to 1/0 and 'None' respectively. 

Used with the various kwargs an API endpoint accepts to get them into a requests friendly format.
"""


def convert_bools_and_nones(kwargs: dict) -> dict:
    """
    Converts bools to 1/0 and Nones to 'None' in a dictionary.

    Params:
        kwargs (dict): Dictionary of keyword arguments.

    Returns:
        dict: Dictionary with bools converted to 1/0 and Nones converted to 'None'.
    """
    # If any kwarg is a bool, convert it to 1 or 0
    for key in kwargs:
        if isinstance(kwargs[key], bool):
            kwargs[key] = 1 if kwargs[key] else 0

    # If any kwarg is None, set it to 'None'
    for key in kwargs:
        if kwargs[key] is None:
            kwargs[key] = "None"

        # if host_metadata is specified and set to a non-"all" or non-NoneType, lower() it:
        if key == "host_metadata" and kwargs[key] not in ["all", None]:
            kwargs[key] = kwargs[key].lower()

    return kwargs
