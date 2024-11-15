"""
Checks that the pageSize value is not greater than a defined limit.
"""


def check_page_size_limit(page_size: int, limit=10_000) -> None:
    if not isinstance(page_size, (int, float)) or page_size > limit or page_size < 1:
        raise ValueError(
            f"pageSize must be an integer greater than 0 and less than or equal to {limit}"
        )
