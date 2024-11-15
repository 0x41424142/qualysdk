"""
Contains write_csv and write_excel functions,
which wrap pandas.DataFrame.to_csv and pandas.DataFrame.to_excel
to accurately export data to CSV and Excel files.
"""

import csv
from typing import Literal

from pandas import DataFrame

from ..sql.base import prepare_dataclass
from .base_list import BaseList


def write_csv(data: BaseList, file_path: str, **kwargs) -> None:
    """
    Write data to a CSV file.

    Args:
        data (BaseList): The data to write.
        file_path (str): The path to the file to write.

    ## Kwargs:

        - **kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_csv other than quoting, sep, and index.
    """

    data = backend_write(data, file_path, "csv", **kwargs)

    # If user path does not end in .csv, add it:
    if not file_path.lower().endswith(".csv"):
        file_path += ".csv"

    # Write to CSV:
    data.astype(str).to_csv(
        file_path,
        index=False,
        sep=",",
        quoting=csv.QUOTE_ALL,
        escapechar="\\",
        encoding="utf-8-sig",
        **kwargs,
    )
    print(f"Data written to {file_path}.")


def write_excel(data: BaseList, file_path: str, **kwargs) -> None:
    """
    Write data to an Excel file.

    Args:
        data (BaseList): The data to write.
        file_path (str): The path to the file to write.

    ## Kwargs:

        - **kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_excel other than index.
    """

    data = backend_write(data, file_path, "excel", **kwargs)

    # If user path does not end in .xlsx, add it:
    if not file_path.lower().endswith(".xlsx"):
        file_path += ".xlsx"

    # Write to Excel:
    data.to_excel(file_path, index=False, **kwargs)
    print(f"Data written to {file_path}.")


def backend_write(
    data: BaseList, file_path: str, file_type: Literal["csv", "excel"], **kwargs
) -> DataFrame:
    """
    Write data to a file.

    Args:
        data (BaseList): The data to write.
        file_path (str): The path to the file to write.

    ## Kwargs:

        - **kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_csv or pandas.DataFrame.to_excel other than index.
    """

    # Convert dataclass to dictionary if needed.
    # Check that all things in the BaseList have
    # the to_dict method.
    if all(hasattr(thing, "to_dict") for thing in data):
        data = [prepare_dataclass(thing) for thing in data]
    else:
        raise ValueError(
            "All items in the BaseList must have a to_dict method. Bad indexes: ",
            [i for i, thing in enumerate(data) if not hasattr(thing, "to_dict")],
        )

    # Convert to DataFrame if needed:
    if not isinstance(data, DataFrame):
        data = DataFrame(data)

    # Make any datetime cols timezone unaware:
    for col in data.columns:
        if data[col].dtype in [
            "datetime64[ns]",
            "datetime64[ns, tz]",
            "datetime64[ns, UTC]",
            "timedelta64[ns]",
        ]:
            data[col] = data[col].dt.tz_localize(None)

    return data
