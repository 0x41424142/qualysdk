"""
Global AssetView API (GAV) module

This module contains ways to interact with the Qualys Global AssetView API (GAV). Valid endpoints are defined in the CALL_SCHEMA dictionary.

GAV QQL Syntax help: https://docs.qualys.com/en/gav/2.18.0.0/search/how_to_search.htm
"""

from .count_assets import count_assets
from .get_all_assets import get_all_assets
from .get_asset import get_asset
from .query_assets import query_assets
from .uber import GAVUber
