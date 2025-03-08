"""
Patch Management APIs return data on asset patching status,
patches themselves and patching jobs.
"""

from .jobs import (
    list_jobs,
    get_job_results,
    get_job_runs,
    create_job,
    delete_job,
    change_job_status,
)

from .vulnerabilities import lookup_cves
from .version import get_version
from .patches import get_patches, get_patch_count
from .assets import get_assets, lookup_host_uuids
from .patchcatalog import (
    get_patch_catalog,
    get_packages_in_linux_patch,
    get_products_in_windows_patch,
    count_product_vulns,
)
