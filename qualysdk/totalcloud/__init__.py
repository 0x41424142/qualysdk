"""
TotalCloud API module

This module contains ways to interact with the Qualys TotalCloud APIs. 
"""

from .get_connectors import (
    get_connectors,
    get_connector_details,
    get_aws_base_account,
)

from .get_metadata import get_control_metadata
from .evaluations import get_control_stats_by_resouce
from .get_inventory import get_inventory
