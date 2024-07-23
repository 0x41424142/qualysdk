"""
dataclasses module for VMDR module - contains the dataclasses for the VMDR module.
"""

from .software import Software
from .vendor_reference import VendorReference
from .kb_entry import KBEntry
from .bugtraq import Bugtraq
from .cve import CVEID
from .threat_intel import ThreatIntel
from .compliance import Compliance
from .tag import Tag, CloudTag
from .detection import Detection
from .qds_factor import QDSFactor
from .qds import QDS
from .asset_group import AssetGroup
from qualyspy.vmdr.data_classes.vmscan import VMScan

from .lists import BaseList
