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

from .lists import BaseList