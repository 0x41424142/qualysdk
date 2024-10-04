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
from .evaluations import (
    get_evaluation,
    get_account_evaluation,
    get_resources_evaluated_by_control,
)
from .get_inventory import get_inventory
from .get_resource_details import get_resource_details
from .remediation_log import get_remediation_activities
