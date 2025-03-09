"""
Contains a simple parser to change datatypes for dataclasses
as needed
"""

from typing import Dict, List


def parse_fields(obj: object, source: Dict, prefix: str, fields: List[str]):
    if source:
        for field in fields:
            if field in source:
                setattr(obj, f"{prefix}_{field}", source.get(field))
