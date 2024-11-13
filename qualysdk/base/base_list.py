"""
Contains the BaseList class for the qualysdk package.

The BaseList class is used to contain custom class objects in a list.
"""


class BaseList(list):
    """
    BaseList - represents a base list class for the qualysdk package.

    Essentially, this is a regular Python list but with a custom __str__ method for better DB representation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        # instead of returning "[...]", return a comma-separated string of the objects in the list
        return ", ".join(str(obj) for obj in self) if self else "[]"
