"""
SQL server integration for qualysdk
"""

from .base import db_connect, upload_json
from .vmdr import (
    upload_vmdr_ags,
    upload_vmdr_kb,
    upload_vmdr_hosts,
    upload_vmdr_ips,
    upload_vmdr_hld,
    upload_vmdr_scanners,
    upload_vmdr_static_search_lists,
    upload_vmdr_dynamic_search_lists,
    upload_vmdr_users,
    upload_vmdr_scan_list,
    upload_vmdr_report_list,
    upload_vmdr_scheduled_report_list,
    upload_vmdr_template_list,
    upload_vmdr_kb_qvs,
    upload_vmdr_activity_log,
    upload_vmdr_cve_hld,
)

from .gav import upload_gav_hosts

from .totalcloud import (
    upload_totalcloud_aws_connectors,
    upload_totalcloud_azure_connectors,
    upload_totalcloud_gcp_connectors,
    upload_totalcloud_control_metadata,
    upload_totalcloud_aws_ec2,
    upload_totalcloud_aws_s3,
    upload_totalcloud_aws_acl,
    upload_totalcloud_aws_rds,
    upload_totalcloud_aws_iamuser,
    upload_totalcloud_aws_vpc,
    upload_totalcloud_aws_securitygroup,
    upload_totalcloud_aws_lambda,
    upload_totalcloud_aws_subnet,
    upload_totalcloud_aws_internetgateway,
    upload_totalcloud_aws_loadbalancer,
    upload_totalcloud_aws_routetable,
    upload_totalcloud_aws_ebsvolume,
    upload_totalcloud_aws_autoscalinggroup,
    upload_totalcloud_aws_ekscluster,
    upload_totalcloud_aws_eksnodegroup,
    upload_totalcloud_aws_fargateprofile,
    upload_totalcloud_aws_vpcendpoint,
    upload_totalcloud_aws_vpcendpointservice,
    upload_totalcloud_aws_iamgroup,
    upload_totalcloud_aws_iampolicy,
    upload_totalcloud_aws_iamrole,
    upload_totalcloud_aws_sagemakernotebook,
    upload_totalcloud_aws_cloudfrontdistribution,
    upload_totalcloud_remediation_activities,
    upload_totalcloud_azure_vm,
    upload_totalcloud_azure_webapp,
    upload_totalcloud_azure_storageaccount,
)

from .cloud_agent import upload_cloud_agents
from .cs import upload_cs_containers, upload_cs_software, upload_cs_vulns
from .was import (
    upload_was_webapps,
    upload_was_authentication_records,
    upload_was_findings,
    upload_was_scans,
)
from .pm import (
    upload_pm_jobs,
    upload_pm_job_results,
    upload_pm_job_runs,
    upload_pm_cves,
    upload_pm_patches,
    upload_pm_assets,
    upload_pm_assetids_to_uuids,
    upload_pm_patch_catalog,
    upload_pm_linux_packages,
    upload_pm_windows_products,
    upload_pm_product_vuln_counts,
)
from .cert import upload_cert_certs

from .tagging import upload_tagging_tags
