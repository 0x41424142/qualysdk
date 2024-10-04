"""
Contains code to ensure XML kwargs are parsed correctly
"""

from .filter_mappings import ENDPOINT_MAPPINGS, FILTER_MAPPING


def validate_kwargs(endpoint: str, **kwargs):
    """
    Ensures that the kwargs provided are valid for the given endpoint.
    """

    # Validate endpoint:
    if endpoint not in ENDPOINT_MAPPINGS:
        raise ValueError(
            f"Invalid endpoint: {endpoint}. Acceptable endpoints: {', '.join(ENDPOINT_MAPPINGS.keys())}"
        )

    # If the lastScan_status kwarg is provided, or if the key contains '_operator',
    # .upper() the value to ensure it's in the correct format:
    for key in kwargs.keys():
        if "lastScan_status" in key or "_operator" in key:
            kwargs[key] = str(kwargs[key]).upper()

    # Get the endpoint's filter data types.
    # ENDPOINT_MAPPINGS is a dictionary that for each endpoint,
    # contains the Qualys-expected data types for each field.
    # Combining this with FILTER_MAPPING, which contains the
    # operators available for each data type, we can validate
    # the provided kwargs.
    endpoint_dtypes = ENDPOINT_MAPPINGS[endpoint]

    # If a _operator key is provided, ensure that the
    # married kwarg is also provided:
    for key in [i for i in kwargs.keys() if "_operator" in i]:
        if key[:-9] not in kwargs:
            raise ValueError(f"Missing filter kwarg for {key[:-9]}")

    # Check if the provided kwargs are valid
    for key, value in kwargs.items():
        if "_operator" not in key and key not in endpoint_dtypes:
            raise ValueError(
                f"Invalid key: {key}. Acceptable keys: {endpoint_dtypes.keys()}"
            )

        if key.endswith("_operator"):
            if value not in FILTER_MAPPING[endpoint_dtypes[key[:-9]]]:
                raise ValueError(
                    f"Invalid operator for {key[:-9]}: {value}. Valid operators for {key[:-9]}: {FILTER_MAPPING[endpoint_dtypes[key[:-9]]]}"
                )

    # Lastly, convert any _s to .s in the keys:
    # Yikes...
    return {
        key.replace("_", ".") if key != "_operator" else key: value
        for key, value in kwargs.items()
    }
