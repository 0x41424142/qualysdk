"""
Pull resources from a cloud provider account.
"""

from typing import Literal, Union

from ..base.call_api import call_api
from ..base.base_list import BaseList
from ..auth.token import BasicAuth
from ..exceptions.Exceptions import *
from .data_classes.AWSResources import *

VALID_RESOURCETYPES = {
    "aws": [
        "RDS",
        "NETWORK_ACL",
        "BUCKET",
        "IAM_USER",
        "VPC",
        "VPC_SECURITY_GROUP",
        "LAMBDA",
        "SUBNET",
        "INTERNET_GATEWAY",
        "LOAD_BALANCER",
        "EC2_INSTANCE",
        "ROUTE_TABLE",
        "EBS",
        "AUTO_SCALING_GROUP",
        "EKS_CLUSTER",
        "EKS_NODEGROUP",
        "EKS_FARGATE_PROFILE",
        "VPC_ENDPOINT",
        "VPC_ENDPOINT_SERVICE",
        "IAM_GROUP",
        "IAM_POLICY",
        "IAM_ROLE",
        "SAGEMAKER_NOTEBOOK",
        "CLOUDFRONT_DISTRIBUTION",
    ],
    "azure": [
        "SQL_SERVER",
        "FUNCTION_APP",
        "SQL_SERVER_DATABASE",
        "RESOURCE_GROUP",
        "VIRTUAL_NETWORK",
        "VIRTUAL_MACHINE",
        "NETWORK_SECURITY_GROUP",
        "WEB_APP",
        "NETWORK_INTERFACES",
        "POSTGRE_SINGLE_SERVER",
        "LOAD_BALANCER",
        "FIREWALL",
        "MYSQL",
        "STORAGE_ACCOUNT",
        "APPLICATION_GATEWAYS",
        "SECRETS",
        "MARIADB",
        "COSMODB",
        "NAT_GATEWAYS",
    ],
    "gcp": [
        "VM_INSTANCES",
        "NETWORKS",
        "FIREWALL_RULES",
        "SUBNETWORKS",
        "CLOUD_FUNCTIONS",
    ],
}

# Common names for resources to substitute for the user's convenience
COMMON_NAMES = {
    "aws": {
        "NETWORK_ACL": ["ACL"],
        "BUCKET": ["S3_BUCKET", "S3"],
        "IAM_USER": ["IAM"],
        "VPC_SECURITY_GROUP": ["SECURITY_GROUP", "SG"],
        "LAMBDA": ["LAMBDA_FUNCTION"],
        "INTERNET_GATEWAY": ["IG", "IGW", "GATEWAY"],
        "LOAD_BALANCER": ["ELB", "LB"],
        "EC2_INSTANCE": ["EC2", "INSTANCE"],
        "ROUTE_TABLE": ["ROUTE", "ROUTES"],
        "EBS": ["VOLUME", "VOLUMES", "EBS_VOLUME", "EBS_VOLUMES"],
        "AUTO_SCALING_GROUP": ["ASG"],
        "EKS_CLUSTER": ["EKS"],
        "EKS_NODEGROUP": ["NODE_GROUP", "EKSNG", "EKS_NODE_GROUP"],
        "EKS_FARGATE_PROFILE": ["FARGATE_PROFILE", "EKS_FARGATE", "FARGATE"],
        "VPC_ENDPOINT_SERVICE": ["ENDPOINT_SERVICE"],
        "IAM_GROUP": ["IAMGROUP"],
        "IAM_POLICY": ["POLICY", "IAMPOLICY"],
        "IAM_ROLE": ["ROLE", "IAMROLE"],
        "SAGEMAKER_NOTEBOOK": ["NOTEBOOK", "SAGEMAKER"],
        "CLOUDFRONT_DISTRIBUTION": ["CLOUDFRONT"],
    },
    "azure": {},
    "gcp": {},
}

# For dynamically creating the resource object based on the resource type
resource_map = {
    "RDS": AWSRDS,
    "NETWORK_ACL": AWSNetworkACL,
    "BUCKET": AWSBucket,
    "IAM_USER": AWSIAMUser,
    "VPC": AWSVPC,
    "VPC_SECURITY_GROUP": AWSSecurityGroup,
    "LAMBDA": AWSLambdaFunction,
    "SUBNET": AWSSubnet,
    "INTERNET_GATEWAY": AWSInternetGateway,
    "LOAD_BALANCER": AWSLoadBalancer,
    "EC2_INSTANCE": AWSEC2Instance,
    "ROUTE_TABLE": AWSRouteTable,
    "EBS": AWSEBSVolume,
    "AUTO_SCALING_GROUP": AWSAutoScalingGroup,
    "EKS_CLUSTER": AWSEKSCluster,
    "EKS_NODEGROUP": AWSEKSNodeGroup,
    "EKS_FARGATE_PROFILE": AWSEKSFargateProfile,
    "VPC_ENDPOINT": AWSVPCEndpoint,
    "VPC_ENDPOINT_SERVICE": AWSVPCEndpointService,
    "IAM_GROUP": AWSIAMGroup,
    "IAM_POLICY": AWSIAMPolicy,
    "IAM_ROLE": AWSIAMRole,
    "SAGEMAKER_NOTEBOOK": AWSSagemakerNotebook,
    "CLOUDFRONT_DISTRIBUTION": AWSCloudfrontDistribution,
}


def get_inventory(
    auth: BasicAuth,
    provider: Literal["aws", "azure", "gcp"],
    resourceType: str,
    page_count: Union[int, "all"] = "all",
    **kwargs,
) -> BaseList:
    """
    Get resources from a cloud provider account.

    Args:
        auth (BasicAuth): The authentication object.
        provider (Literal["aws", "azure", "gcp", "oci"]): The cloud provider to get resources from.
        resourceType (str): The type of resource to get. Valid resource types are:
            aws (str): ['RDS', 'NETWORK ACL', 'S3 BUCKET', 'IAM USER', 'VPC', 'SECURITY GROUP', 'LAMBDA FUNCTION', 'SUBNET', 'INTERNET GATEWAY', 'LOAD BALANCER', 'INSTANCE', 'ROUTE TABLE', 'EBS VOLUME', 'AUTO SCALING GROUP', 'EKS CLUSTER', 'EKS NODE GROUP', 'EKS FARGATE PROFILE', 'VPC ENDPOINT', 'VPC ENDPOINT SERVICE', 'IAM GROUP', 'IAM POLICY', 'IAM ROLE', 'SAGEMAKER NOTEBOOK', 'CLOUDFRONT DISTRIBUTION']

            azure (str): ['SQL SERVER', 'FUNCTION APP', 'SQL SERVER DATABASE', 'RESOURCE GROUP', 'VIRTUAL NETWORK', 'VIRTUAL MACHINE', 'NETWORK SECURITY GROUP', 'WEB APP', 'NETWORK INTERFACES', 'POSTGRE SINGLE SERVER', 'LOAD BALANCER', 'FIREWALL', 'MYSQL', 'STORAGE ACCOUNT', 'APPLICATION GATEWAYS', 'SECRETS', 'MARIADB', 'COSMODB', 'NAT GATEWAYS']

            gcp (str): ['VM INSTANCES', 'NETWORKS', 'FIREWALL RULES', 'SUBNETWORKS', 'CLOUD FUNCTIONS']

            oci (str): ['COMPUTE INSTANCE', 'IAM USERS', 'BUCKET', 'SECURITY LISTS']

    ## Kwargs:

        page_count (int): The number of pages to return. If 'all', return all pages. Default is 'all'.
        pageSize (int): The number of resources to get per page.
        pageNo (int): The page number to get if page_count is not 'all'. If page_count is 'all', this is the starting page number.
        sort (Literal['lastSyncedOn:asc', 'lastSyncedOn:desc']): Sort the resources by lastSyncedOn in ascending or descending order.
        updated (str): Filter resources by the last updated date. Format is Qualys QQL, like [2024-01-01 ... 2024-12-31], [2024-01-01 ... now-1m] (month), 2024-01-01, etc.
        filter (str): Filter resources by providing a query.

    Returns:
        BaseList: The response from the API as a BaseList of Resource objects.
    """

    # Check if the provider is valid
    provider = provider.lower()
    resourceType = resourceType.upper()

    # Check if the provider is valid
    if provider not in ["aws", "azure", "gcp"]:
        raise ValueError("Invalid provider. Must be 'aws', 'azure', 'gcp', or 'oci'.")

    # For convenience, allow the user to input 'common names': e.g. 'ACL' for 'NETWORK_ACL'
    if " " in resourceType:
        resourceType = resourceType.replace(" ", "_")

    for key, value in COMMON_NAMES[provider].items():
        if resourceType in value:
            resourceType = key
            break

    # Check if the resource type is valid
    if resourceType not in VALID_RESOURCETYPES[provider]:
        raise ValueError(
            f"Invalid resource type for provider {provider}. Valid resource types are: {VALID_RESOURCETYPES[provider]}"
        )

    results = BaseList()
    currentPage = 0

    while True:
        # Set the current page number and page size in kwargs
        kwargs["placeholder"] = resourceType
        kwargs["cloudprovider"] = provider.upper()
        kwargs["pageNo"] = currentPage

        # Make the API call
        response = call_api(
            auth=auth,
            module="cloudview",
            endpoint="get_inventory",
            params=kwargs,
        )

        if response.status_code != 200:
            if not response.text:
                raise QualysAPIError(
                    "An error occurred while retrieving the inventory Most likely, a parameter you set is incorrect."
                )
            else:
                raise QualysAPIError(response.json())

        j = response.json()

        if len(j["content"]) == 0:
            print(f"No items found for inventory type {resourceType}.")
            break

        for i in j["content"]:
            resource_class = resource_map.get(resourceType, None)
            if resource_class:
                # Some resources have a type key, which we will overwrite to _type:
                if "type" in i.keys():
                    i["_type"] = i.pop("type")
                i = resource_class(**i)

            else:
                raise ValueError(
                    f"Invalid resource type {resourceType} for provider {provider}. Valid resource types are:\n{VALID_RESOURCETYPES[provider]}"
                )
            results.append(i)

        # Print a message indicating the current page was retrieved successfully
        print(
            f"Page {currentPage+1} of {provider}-{resourceType} retrieved successfully."
        )
        currentPage += 1

        # Break the loop if all pages are retrieved or the requested number of pages are retrieved
        if (page_count != "all" and currentPage + 1 > page_count) or j["last"]:
            break

    # Print a message indicating all pages have been retrieved
    print(
        f"All pages complete. {str(len(results))} {provider} {resourceType} records retrieved."
    )
    return results
