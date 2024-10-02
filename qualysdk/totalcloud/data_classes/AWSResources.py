"""
Contains resource dataclasses for AWS, such as buckets, EC2s, etc.
"""

from dataclasses import dataclass, asdict
from typing import Union
from datetime import datetime
from json import loads
from urllib.parse import unquote

from ...base.base_list import BaseList
from .QID import QID


@dataclass
class BaseResource:
    """
    Base dataclass for all AWS resources in TotalCloud
    """

    resourceId: str = None
    name: str = None
    connectorUuids: BaseList[str] = None
    created: Union[str, datetime] = None
    cloudAccountId: int = None
    additionalDetails: dict = None
    uuid: str = None
    connectorUuid: str = None
    createdOn: Union[str, datetime] = None
    tags: BaseList[str] = None
    remediationEnabled: bool = None
    lastUpdated: Union[str, datetime] = None
    cloudType: str = None
    region: str = None
    resourceType: str = None
    accountAlias: str = None
    controlsFailed: int = None
    qualysTags: BaseList[str] = None

    def __post_init__(self):
        """
        __post_init__ - post initialization method for the BaseResource dataclass
        """
        DT_FIELDS = ["created", "createdOn", "lastUpdated"]
        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if self.additionalDetails:
            setattr(self, "additionalDetails", str(self.additionalDetails))

        if self.connectorUuids:
            data = self.connectorUuids
            bl = BaseList()
            for uuid in data:
                bl.append(uuid)
            setattr(self, "connectorUuids", bl)

        if self.tags:
            data = self.tags
            bl = BaseList()
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(f"{tag.get('key', None)}:{tag.get('value', None)}")
            setattr(self, "tags", bl)

        if self.qualysTags:
            data = self.qualysTags
            bl = BaseList()
            if isinstance(data, dict):
                data = [data]
            for tag in data:
                bl.append(tag["tagName"])
            setattr(self, "qualysTags", bl)

        if self.cloudAccountId:
            setattr(self, "cloudAccountId", int(self.cloudAccountId))

        if self.remediationEnabled:
            data = self.remediationEnabled
            if not isinstance(data, bool):
                setattr(self, "remediationEnabled", data.lower() == "true")

    def to_dict(self):
        """
        to_dict - return the BaseResource as a dictionary
        """
        return asdict(self)

    def keys(self):
        """
        keys - return the keys of the BaseResource
        """
        return self.to_dict().keys()

    def values(self):
        """
        values - return the values of the BaseResource
        """
        return self.to_dict().values()

    def items(self):
        """
        items - return the items of the BaseResource
        """
        return self.to_dict().items()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create a BaseResource object from a dictionary
        """
        return BaseResource(**data)


@dataclass
class AWSBucket(BaseResource):
    """
    Represents an S3 bucket in AWS
    """

    bucketName: str = None
    bucketCreationDateStr: Union[str, datetime] = None
    s3GrantList: BaseList[str] = None
    ownerName: str = None
    bucketPolicy: str = None
    bucketOwnerId: str = None

    def __post_init__(self):
        """
        __post_init__ - post initialization method for the AWSBucket dataclass
        """

        DT_FIELDS = ["bucketCreationDateStr"]
        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        if self.s3GrantList:
            data = self.s3GrantList
            bl = BaseList()
            for grant in data:
                bl.append(
                    f"(email: {grant.get('emailAddress', None)}, groupUri: {grant.get('groupUri', None)}, displayName: {grant.get('displayName', None)}, permission: {grant.get('permission', None)}, id: {grant.get('id', None)})"
                )
            setattr(self, "s3GrantList", bl)

        # For some reason, Qualys returns bool fields as strings for certain resources?
        BOOL_FIELDS = ["remediationEnabled"]
        for field in BOOL_FIELDS:
            data = getattr(self, field)
            if data and not isinstance(data, bool):
                setattr(self, field, data.lower() == "true")

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSBucket object from a dictionary
        """
        return AWSBucket(**data)


@dataclass
class AWSNetworkACL(BaseResource):
    """
    Represents a Network ACL in AWS
    """

    associations: BaseList[str] = None
    ipPermissionEgressList: BaseList[str] = None
    ipPermissionList: BaseList[str] = None
    isDefault: bool = None
    vpcId: str = None
    networkAclId: str = None

    def __post_init__(self):
        if self.associations:
            data = self.associations
            bl = BaseList()
            for association in data:
                bl.append(
                    f"(subnetId: {association.get('subnetId', None)}, networkAclAssociationId: {association.get('networkAclAssociationId', None)}, networkAclId: {association.get('networkAclId', None)})"
                )
            setattr(self, "associations", bl)

        if self.ipPermissionEgressList:
            data = self.ipPermissionEgressList
            bl = BaseList()
            for permission in data:
                portRange = permission.get("portRange", None)
                ruleAction = permission.get("ruleAction", None)
                protocol = permission.get("protocol", None)
                source = permission.get("source", None)
                _type = permission.get("type", None)
                s = f"(portRange: {portRange}, ruleAction: {ruleAction}, protocol: {protocol}, source: {source}, type: {_type})"
                bl.append(s)
            setattr(self, "ipPermissionEgressList", bl)

        if self.ipPermissionList:
            data = self.ipPermissionList
            bl = BaseList()
            for permission in data:
                portRange = permission.get("portRange", None)
                ruleAction = permission.get("ruleAction", None)
                protocol = permission.get("protocol", None)
                source = permission.get("source", None)
                _type = permission.get("type", None)
                s = f"(portRange: {portRange}, ruleAction: {ruleAction}, protocol: {protocol}, source: {source}, type: {_type})"
                bl.append(s)
            setattr(self, "ipPermissionList", bl)

        BOOL_FIELDS = ["isDefault"]
        for field in BOOL_FIELDS:
            data = getattr(self, field)
            if data and not isinstance(data, bool):
                setattr(self, field, data.lower() == "true")

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSNetworkACL object from a dictionary
        """
        return AWSNetworkACL(**data)


@dataclass
class AWSRDS(BaseResource):
    """
    Represents a Relational Database Service in AWS
    """

    subnetId: BaseList[str] = None
    subnetGroup: None = None  # Gets parsed out
    # subnetGroup is parsed out to below fields
    subnetGroup_dbSubnetGroupStatus: str = None
    subnetGroup_dbSubnetGroupName: str = None
    subnetGroup_dbSubnetVpcId: str = None
    subnetGroup_subnetList: BaseList[str] = None
    subnetGroup_dbsubnetGroupArn: str = None
    # end of subnetGroup fields
    dbName: str = None
    availabilityZone: str = None
    securityGroupId: BaseList[str] = None
    dbClusterIdentifier: str = None
    caCertificateIdentifier: str = None
    engineVersion: str = None
    masterUsername: str = None
    dbInstanceIdentifier: str = None
    dbSecurityGroupList: BaseList[str] = None
    # name: str = None
    backupRetentionPeriod: int = None
    kmsKeyId: str = None
    status: str = None
    latestRestorableTime: Union[str, datetime] = None
    dbInstancePort: int = None
    enhancedMonitoringEnabled: bool = None
    dbiResourceId: str = None
    preferredBackupWindow: str = None
    endpoint: None = None  # Gets parsed out
    # endpoint is parsed out to below fields
    endpoint_hostedZoneId: str = None
    endpoint_address: str = None
    endpoint_port: int = None
    # end of endpoint fields
    engine: str = None
    publiclyAccessible: bool = None
    arn: str = None
    instanceCreatedTime: Union[str, datetime] = None
    multiAZ: bool = None
    instanceClass: str = None
    encrypted: bool = None
    iamDatabaseAuthenticationEnabled: bool = None
    licenseModel: str = None
    preferredMaintenanceWindow: str = None
    storageType: str = None

    def __post_init__(self):
        if self.subnetId:
            data = self.subnetId
            bl = BaseList()
            for subnet in data:
                bl.append(subnet)
            setattr(self, "subnetId", bl)

        if self.subnetGroup:
            data = self.subnetGroup
            for key, value in data.items():
                if key == "subnetList":
                    bl = BaseList()
                    for subnet in value:
                        bl.append(
                            f"(identifier: {subnet.get('identifier', None)}, availabilityZone: {subnet.get('availabilityZone', None)}, status: {subnet.get('status', None)})"
                        )
                    setattr(self, "subnetGroup_subnetList", bl)
                else:
                    setattr(self, f"subnetGroup_{key}", value)
            setattr(self, "subnetGroup", None)

        if self.securityGroupId:
            data = self.securityGroupId
            bl = BaseList()
            for group in data:
                bl.append(group)
            setattr(self, "securityGroupId", bl)

        if self.dbSecurityGroupList:
            data = self.dbSecurityGroupList
            bl = BaseList()
            for group in data:
                bl.append(group)
            setattr(self, "dbSecurityGroupList", bl)

        if self.endpoint:
            data = self.endpoint
            for key, value in data.items():
                setattr(self, f"endpoint_{key}", value)
            setattr(self, "endpoint", None)

        DT_FIELDS = ["latestRestorableTime", "instanceCreatedTime"]
        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(self, field, datetime.fromisoformat(getattr(self, field)))

        BOOL_FIELDS = [
            "enhancedMonitoringEnabled",
            "multiAZ",
            "encrypted",
            "iamDatabaseAuthenticationEnabled",
            "publiclyAccessible",
        ]
        for field in BOOL_FIELDS:
            data = getattr(self, field)
            if data and not isinstance(data, bool):
                setattr(self, field, data.lower() == "true")

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSRDS object from a dictionary
        """
        return AWSRDS(**data)


@dataclass
class AWSIAMUser(BaseResource):
    """
    Represents an IAM User in AWS
    """

    userPolicies: BaseList[str] = None
    userAttachedPolicies: BaseList[str] = None
    userDto: None = None  # Gets parsed out
    # userDto is parsed out to below fields
    userDto_accessKey2Active: bool = None
    userDto_cert2LastRotated: Union[str, datetime] = None
    userDto_cert2Active: bool = None
    userDto_accessKey2LastRotated: Union[str, datetime] = None
    userDto_path: str = None
    userDto_accessKeys: BaseList[str] = None
    userDto_passwordLastUsed: Union[str, datetime] = None
    userDto_passwordNextRotation: Union[str, datetime] = None
    userDto_accessKey1LastUsedRegion: str = None
    userDto_arn: str = None
    userDto_userCreationTime: Union[str, datetime] = None
    userDto_accessKey1LastRotated: Union[str, datetime] = None
    userDto_cert1Active: bool = None
    userDto_mfaActive: bool = None
    userDto_accessKey2LastUsedService: str = None
    userDto_passwordEnabled: bool = None
    userDto_accessKey1Active: bool = None
    userDto_accessKey1LastUsed: Union[str, datetime] = None
    userDto_accessKey2LastUsed: Union[str, datetime] = None
    userDto_userId: str = None
    userDto_createdDate: Union[str, datetime] = None
    userDto_passwordLastChanged: Union[str, datetime] = None
    userDto_cert1LastRotated: Union[str, datetime] = None
    userDto_accessKey1LastUsedService: str = None
    userDto_accessKey2LastUsedRegion: str = None
    userDto_username: str = None
    # end of userDto fields
    userGroups: BaseList[str] = None
    classifications: BaseList[str] = None
    userInlinePolicies: BaseList[str] = None
    user: str = None

    def __post_init__(self):
        POLICY_FIELDS = ["userPolicies", "userAttachedPolicies"]
        for field in POLICY_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for policy in data:
                    if field == "userAttachedPolicies":
                        bl.append(
                            f"(policyArn: {policy.get('policyArn', None)}, policyName: {policy.get('policyName', None)})"
                        )
                    else:
                        bl.append(policy)

                setattr(self, field, bl)

        if self.userDto:
            data = self.userDto
            bl = BaseList()
            # First, parse out accessKeys:
            accessKeys = data.get("accessKeys", None)
            accessKeysbl = BaseList()
            for key in accessKeys:
                timestamp = key.get("createDate", None)
                if timestamp:  # format: 1703001007000
                    timestamp = datetime.fromtimestamp(int(timestamp) / 1000)
                status = key.get("status", None)
                accessKeyId = key.get("accessKeyId", None)
                accessKeysbl.append(
                    f"(accessKeyId: {accessKeyId}, createDate: {timestamp}, status: {status})"
                )
            setattr(self, "userDto_accessKeys", accessKeysbl)
            # Now we can parse the rest of the fields
            for key, value in data.items():
                if key == "accessKeys":
                    continue
                else:
                    setattr(self, f"userDto_{key}", value)
            setattr(self, "userDto", None)

        if self.userGroups:
            data = self.userGroups
            bl = BaseList()
            for group in data:
                groupArn = group.get("groupArn", None)
                path = group.get("path", None)
                groupName = group.get("groupName", None)
                createdDate = group.get("createdDate", None)
                if createdDate:
                    createdDate = datetime.fromtimestamp(int(createdDate) / 1000)
                groupId = group.get("groupId", None)
                bl.append(
                    f"(groupArn: {groupArn}, path: {path}, groupName: {groupName}, createdDate: {createdDate}, groupId: {groupId})"
                )
            setattr(self, "userGroups", bl)

        if self.classifications:
            data = self.classifications
            bl = BaseList()
            for classification in data:
                bl.append(classification)
            setattr(self, "classifications", bl)

        if self.userInlinePolicies:
            data = self.userInlinePolicies
            bl = BaseList()
            for policy in data:
                policyDocument = policy.get("policyDocument", None)
                policyName = policy.get("policyName", None)
                bl.append(
                    f"(policyDocument: {policyDocument}, policyName: {policyName})"
                )
            setattr(self, "userInlinePolicies", bl)

        DT_FIELDS = [
            "userDto_cert2LastRotated",
            "userDto_accessKey2LastRotated",
            "userDto_passwordLastUsed",
            "userDto_passwordNextRotation",
            "userDto_userCreationTime",
            "userDto_accessKey1LastRotated",
            "userDto_createdDate",
            "userDto_passwordLastChanged",
            "userDto_cert1LastRotated",
            "userDto_accessKey1LastUsed",
            "userDto_accessKey2LastUsed",
        ]
        for field in DT_FIELDS:
            if getattr(self, field) and not isinstance(getattr(self, field), datetime):
                setattr(
                    self,
                    field,
                    datetime.fromtimestamp(int(getattr(self, field)) / 1000),
                )

        BOOL_FIELDS = [
            "userDto_accessKey2Active",
            "userDto_cert2Active",
            "userDto_cert1Active",
            "userDto_mfaActive",
            "userDto_passwordEnabled",
            "userDto_accessKey1Active",
        ]
        for field in BOOL_FIELDS:
            data = getattr(self, field)
            if data and not isinstance(data, bool):
                setattr(self, field, data.lower() == "true")

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSIAMUser object from a dictionary
        """
        return AWSIAMUser(**data)


@dataclass
class AWSVPC(BaseResource):
    """
    Represents a Virtual Private Cloud in AWS
    """

    instanceTenancy: str = None
    cidrBlock: str = None
    isDefault: bool = None
    vpcId: str = None
    ipv6CidrBlockAssociationSet: BaseList[str] = None

    def __post_init__(self):
        if self.ipv6CidrBlockAssociationSet:
            data = self.ipv6CidrBlockAssociationSet
            bl = BaseList()
            for association in data:
                associationId = association.get("associationId", None)
                ipv6CidrBlockState = association.get("ipv6CidrBlockState", None)
                ipv6CidrBlock = association.get("ipv6CidrBlock", None)
                bl.append(
                    f"(associationId: {associationId}, ipv6CidrBlockState: {ipv6CidrBlockState}, ipv6CidrBlock: {ipv6CidrBlock})"
                )
            setattr(self, "ipv6CidrBlockAssociationSet", bl)

        BOOL_FIELDS = ["isDefault"]
        for field in BOOL_FIELDS:
            data = getattr(self, field)
            if data and not isinstance(data, bool):
                setattr(self, field, data.lower() == "true")

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSVPC object from a dictionary
        """
        return AWSVPC(**data)


@dataclass
class AWSSecurityGroup(BaseResource):
    """
    Represents a security group in AWS
    """

    groupId: str = None
    description: str = None
    vulnerable: bool = None
    vpcId: str = None
    ipPermissionList: BaseList[str] = None
    ipPermissionEgressList: BaseList[str] = None
    groupName: str = None

    def __post_init__(self):
        if self.ipPermissionList:
            data = self.ipPermissionList
            bl = BaseList()
            for permission in data:
                portRange = permission.get("portRange", None)
                ruleAction = permission.get("ruleAction", None)
                protocol = permission.get("protocol", None)
                source = permission.get("source", None)
                _type = permission.get("type", None)
                s = f"(portRange: {portRange}, ruleAction: {ruleAction}, protocol: {protocol}, source: {source}, type: {_type})"
                bl.append(s)
            setattr(self, "ipPermissionList", bl)

        if self.ipPermissionEgressList:
            data = self.ipPermissionEgressList
            bl = BaseList()
            for permission in data:
                portRange = permission.get("portRange", None)
                ruleAction = permission.get("ruleAction", None)
                protocol = permission.get("protocol", None)
                source = permission.get("source", None)
                _type = permission.get("type", None)
                s = f"(portRange: {portRange}, ruleAction: {ruleAction}, protocol: {protocol}, source: {source}, type: {_type})"
                bl.append(s)
            setattr(self, "ipPermissionEgressList", bl)

        # For some reason, Qualys returns bool fields as strings for certain resources?
        BOOL_FIELDS = ["vulnerable"]
        for field in BOOL_FIELDS:
            data = getattr(self, field)
            if data and not isinstance(data, bool):
                setattr(self, field, data.lower() == "true")

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSSecurityGroup object from a dictionary
        """
        return AWSSecurityGroup(**data)


@dataclass
class AWSLambdaFunction(BaseResource):
    """
    Represents a Lambda function in AWS
    """

    associations: BaseList[str] = None
    handler: str = None
    rawFunctionPolicy: str = None
    masterArn: str = None
    aliases: BaseList[str] = None
    assumeRolePolicyDocument: str = None
    kmsKeyArn: str = None
    tracingConfig: str = None
    description: str = None
    inlinePolicies: BaseList[str] = None
    codeSize: int = None
    timeout: int = None
    codeSha256: str = None
    roleArn: str = None
    vpcId: str = None
    layers: BaseList[str] = None
    functionArn: str = None
    functionVersions: BaseList[str] = None
    functionName: str = None
    runtime: str = None
    functionUrlConfigs: BaseList[str] = None
    revisionId: str = None
    classifications: BaseList[str] = None
    managedPolicies: BaseList[str] = None
    memorySize: int = None
    eventSourceMappings: BaseList[str] = None
    roleName: str = None
    lastModified: Union[str, datetime] = None
    version: str = None

    def __post_init__(self):
        # all fields above with a comment should be investigated!

        if self.aliases:
            data = self.aliases
            bl = BaseList()
            for alias in data:
                revisionId = alias.get("revisionId", None)
                aliasArn = alias.get("aliasArn", None)
                routingConfigAdditionalVersion = alias.get(
                    "routingConfigAdditionalVersion", None
                )
                functionVersion = alias.get("functionVersion", None)
                name = alias.get("name", None)
                description = alias.get("description", None)
                routingConfigAdditionalVersionWeight = alias.get(
                    "routingConfigAdditionalVersionWeight", None
                )
                bl.append(
                    f"(revisionId: {revisionId}, aliasArn: {aliasArn}, routingConfigAdditionalVersion: {routingConfigAdditionalVersion}, functionVersion: {functionVersion}, name: {name}, description: {description}, routingConfigAdditionalVersionWeight: {routingConfigAdditionalVersionWeight})"
                )
            setattr(self, "aliases", bl)

        if self.inlinePolicies:
            data = self.inlinePolicies
            bl = BaseList()
            for policy in data:
                policyDocument_version = policy["policyDocument"]
                policyDocument_policyName = policy.get("policyName", None)
                policyDocument = f"(version: {policyDocument_version}, policyName: {policyDocument_policyName})"
                bl.append(policyDocument)
            setattr(self, "inlinePolicies", bl)

        if self.layers:
            data = self.layers
            bl = BaseList()
            for layer in data:
                name = layer.get("name", None)
                version = layer.get("version", None)
                codeSize = layer.get("codeSize", None)
                bl.append(f"(name: {name}, version: {version}, codeSize: {codeSize})")
            setattr(self, "layers", bl)

        if self.functionVersions:
            data = self.functionVersions
            bl = BaseList()
            for version in data:
                role = version.get("role", None)
                memorySize = version.get("memorySize", None)
                runtime = version.get("runtime", None)
                lastModified = version.get("lastModified", None)
                _version = version.get("version", None)
                codeSize = version.get("codeSize", None)
                bl.append(
                    f"(role: {role}, memorySize: {memorySize}, runtime: {runtime}, lastModified: {lastModified}, version: {_version}, codeSize: {codeSize})"
                )
            setattr(self, "functionVersions", bl)

        if self.functionUrlConfigs:
            data = self.functionUrlConfigs
            bl = BaseList()
            for config in data:
                lastModifiedTime = config.get("lastModifiedTime", None)
                cors = config.get("cors", None)
                creationTime = config.get("creationTime", None)
                functionUrl = config.get("functionUrl", None)
                authType = config.get("authType", None)
                functionArn = config.get("functionArn", None)
                bl.append(
                    f"(lastModifiedTime: {lastModifiedTime}, cors: {cors}, creationTime: {creationTime}, functionUrl: {functionUrl}, authType: {authType}, functionArn: {functionArn})"
                )
            setattr(self, "functionUrlConfigs", bl)

        if self.classifications:
            data = self.classifications
            bl = BaseList()
            for classification in data:
                bl.append(classification)
            setattr(self, "classifications", bl)

        if self.managedPolicies:
            data = self.managedPolicies
            bl = BaseList()
            for policy in data:
                policyArn = policy.get("policyArn", None)
                policyDocument = policy.get("policyDocument", None)
                policyName = policy.get("policyName", None)
                bl.append(
                    f"(policyArn: {policyArn}, policyDocument: {policyDocument}, policyName: {policyName})"
                )
            setattr(self, "managedPolicies", bl)

        if self.eventSourceMappings:
            data = self.eventSourceMappings
            bl = BaseList()
            for mapping in data:
                eventSourceArn = mapping.get("eventSourceArn", None)
                lastProcessingResult = mapping.get("lastProcessingResult", None)
                state = mapping.get("state", None)
                lastModified = mapping.get("lastModified", None)
                _type = mapping.get("type", None)
                bl.append(
                    f"(eventSourceArn: {eventSourceArn}, lastProcessingResult: {lastProcessingResult}, state: {state}, lastModified: {lastModified}, type: {_type})"
                )
            setattr(self, "eventSourceMappings", bl)

        if self.lastModified:
            if not isinstance(self.lastModified, datetime):
                setattr(self, "lastModified", datetime.fromisoformat(self.lastModified))

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSLambdaFunction object from a dictionary
        """
        return AWSLambdaFunction(**data)


@dataclass
class AWSSubnet(BaseResource):
    """
    Represents a subnet in AWS
    """

    subnetId: str = None
    availabilityZone: str = None
    assignIpv6AddressOnCreation: bool = None
    vpcId: str = None
    ipv6CidrBlockAssociationSet: BaseList[str] = None
    cidrBlock: str = None
    availableIpAddressCount: int = None
    mapPublicIpOnLaunch: bool = None
    defaultForAz: bool = None

    def __post_init__(self):
        if self.ipv6CidrBlockAssociationSet:
            data = self.ipv6CidrBlockAssociationSet
            bl = BaseList()
            for association in data:
                if isinstance(association, dict):
                    # None of the subnets i have seen have this field,
                    # but we can take a guess?
                    # Get the keys, and add to a string
                    s = ""
                    for key in association.keys():
                        s += f"{key}: {association[key]}, "
                    # Take out the last comma and space, and wrap s in ()s
                    s = f"({s[:-2]})"
                    bl.append(s)
                else:
                    bl.append(str(association))
            setattr(self, "ipv6CidrBlockAssociationSet", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSSubnet object from a dictionary
        """
        return AWSSubnet(**data)


@dataclass
class AWSInternetGateway(BaseResource):
    """
    Represents an Internet Gateway in AWS
    """

    attachments: BaseList[str] = None
    internetGatewayId: str = None

    def __post_init__(self):
        if self.attachments:
            data = self.attachments
            bl = BaseList()
            for attachment in data:
                s = ""
                for key in attachment.keys():
                    s += f"{key}: {attachment[key]}, "
                s = f"({s[:-2]})"
                bl.append(s)
            setattr(self, "attachments", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSInternetGateway object from a dictionary
        """
        return AWSInternetGateway(**data)


@dataclass
class AWSLoadBalancer(BaseResource):
    """
    Represents a Load Balancer in AWS
    """

    loadBalancerArn: str = None
    scheme: str = None
    instances: BaseList[str] = None  # ???
    subnetAvailabilityZonePair: BaseList[str] = None
    dnsName: str = None
    availabilityZones: BaseList[str] = None
    _type: str = None
    loadBalancerName: str = None
    createdTime: Union[str, datetime] = None
    subnets: BaseList[str] = None
    state: str = None
    listeners: BaseList[str] = None
    ipAddressType: str = None
    vpcid: str = None
    securityGroups: BaseList[AWSSecurityGroup] = None  # Double check!

    def __post_init__(self):
        BL_STR_FIELDS = [
            "subnetAvailabilityZonePair",
            "availabilityZones",
            "subnets",
            "instances",
            "securityGroups",
        ]
        for field in BL_STR_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for item in data:
                    bl.append(item)
                setattr(self, field, bl)

        if self.listeners:
            data = self.listeners
            bl = BaseList()
            for listener in data:
                s = ""
                for key in listener.keys():
                    s += f"{key}: {listener[key]}, "
                s = f"({s[:-2]})"
                bl.append(s)
            setattr(self, "listeners", bl)

        if self.createdTime:
            if not isinstance(self.createdTime, datetime):
                setattr(self, "createdTime", datetime.fromisoformat(self.createdTime))

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSLoadBalancer object from a dictionary
        """
        return AWSLoadBalancer(**data)


@dataclass
class AWSEC2Instance(BaseResource):
    """
    Represents an EC2 Instance in AWS
    """

    subnetId: str = None
    arsScore: int = None
    availabilityZone: str = None
    instanceId: str = None
    instanceState: str = None
    networkInterfaceAddresses: BaseList[str] = None
    vulnerabilityStats: None = None
    # vulnerabilityStats is parsed out to below fields
    vulnerabilityStats_severity_1: int = 0
    vulnerabilityStats_severity_2: int = 0
    vulnerabilityStats_severity_3: int = 0
    vulnerabilityStats_severity_4: int = 0
    vulnerabilityStats_severity_5: int = 0
    vulnerabilityStats_typeDetected_Confirmed: int = 0
    vulnerabilityStats_typeDetected_Potential: int = 0
    vulnerabilityStats_typeDetected_Informational: int = 0
    vulnerabilityStats_typeDetected_totalVulnerability: int = 0
    # end of vulnerabilityStats fields
    vpcId: str = None
    events: BaseList[str] = None  # ???
    iamInstanceProfileRoleDetails: None = None
    # iamInstanceProfileRoleDetails is parsed out to below fields
    iamInstanceProfileRoleDetails_profileName: str = None
    iamInstanceProfileRoleDetails_profileArn: str = None
    iamInstanceProfileRoleDetails_roleArn: str = None
    iamInstanceProfileRoleDetails_roleName: str = None
    # end of iamInstanceProfileRoleDetails fields
    imageId: str = None
    publicIpAddress: str = None
    instanceType: str = None
    ipAddress: str = None
    publicDnsName: str = None
    instanceStatus: str = None
    iamInstanceProfile: None = None
    # iamInstanceProfile is parsed out to below fields
    iamInstanceProfile_name: str = None
    iamInstanceProfile_id: str = None
    iamInstanceProfile_arn: str = None
    # end of iamInstanceProfile fields
    privateIpAddress: str = None
    launchTime: Union[str, datetime] = None
    classifications: BaseList[str] = None
    spotInstanceRequestId: str = None
    elasticIpAddress: str = None
    secondaryPrivateIpAddress: str = None
    securityGroups: BaseList[str] = None
    privateDnsName: str = None
    criticalityScore: int = None
    # vulns are an empty list unless resource details API is called:
    vulnerabilities: BaseList[str] = None

    def __post_init__(self):
        DICT_BL_FIELDS = ["networkInterfaceAddresses", "securityGroups"]
        STR_BL_FIELDS = ["events", "classifications"]
        PARSE_OUT_FIELDS = ["iamInstanceProfileRoleDetails", "iamInstanceProfile"]

        for field in DICT_BL_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for item in data:
                    s = ""
                    for key in item.keys():
                        s += f"{key}: {item[key]}, "
                    s = f"({s[:-2]})"
                    bl.append(s)
                setattr(self, field, bl)

        for field in STR_BL_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for item in data:
                    bl.append(item)
                setattr(self, field, bl)

        if self.vulnerabilityStats:
            data = self.vulnerabilityStats
            severity = data.get("severity", None)
            typeDetected = data.get("typeDetected", None)
            totalVulnerability = data.get("totalVulnerability", None)
            if severity:
                for key in severity.keys():
                    setattr(self, f"vulnerabilityStats_severity_{key}", severity[key])
            if typeDetected:
                for key in typeDetected.keys():
                    setattr(
                        self,
                        f"vulnerabilityStats_typeDetected_{key}",
                        typeDetected[key],
                    )
            if totalVulnerability:
                setattr(
                    self,
                    "vulnerabilityStats_typeDetected_totalVulnerability",
                    totalVulnerability,
                )

            setattr(self, "vulnerabilityStats", None)

        for field in PARSE_OUT_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                for key, value in data.items():
                    setattr(self, f"{field}_{key}", value)
                setattr(self, field, None)

        if self.launchTime:
            if not isinstance(self.launchTime, datetime):
                setattr(self, "launchTime", datetime.fromisoformat(self.launchTime))

        if self.vulnerabilities:
            data = self.vulnerabilities
            if isinstance(data, dict):
                data = [data]
            bl = BaseList()
            for vuln in data:
                bl.append(QID(**vuln))
            setattr(self, "vulnerabilities", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSEC2Instance object from a dictionary
        """
        return AWSEC2Instance(**data)


@dataclass
class AWSRouteTable(BaseResource):
    """
    Represents a Route Table in AWS
    """

    associations: BaseList[str] = None
    routeDtos: BaseList[str] = None
    routes: BaseList[str] = None
    vpcId: str = None
    routeTableId: str = None

    def __post_init__(self):
        BL_FIELDS = ["associations", "routeDtos", "routes"]

        for field in BL_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for item in data:
                    s = ""
                    for key in item.keys():
                        s += f"{key}: {item[key]}, "
                    s = f"({s[:-2]})"
                    bl.append(s)
                setattr(self, field, bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSRouteTable object from a dictionary
        """
        return AWSRouteTable(**data)


@dataclass
class AWSEBSVolume(BaseResource):
    """
    Represents an EBS Volume in AWS
    """

    volumeType: str = None
    attachments: BaseList[str] = None
    availabilityZone: str = None
    volumeId: str = None
    iops: int = None
    state: str = None
    snapshotId: str = None
    encrypted: bool = None
    size: str = None
    createTime: Union[str, datetime] = None
    kmsKeyId: str = None

    def __post_init__(self):
        if self.attachments:
            data = self.attachments
            bl = BaseList()
            for attachment in data:
                s = ""
                for key in attachment.keys():
                    s += f"{key}: {attachment[key]}, "
                s = f"({s[:-2]})"
                bl.append(s)
            setattr(self, "attachments", bl)

        if self.createTime:
            if not isinstance(self.createTime, datetime):
                setattr(self, "createTime", datetime.fromisoformat(self.createTime))

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSEBSVolume object from a dictionary
        """
        return AWSEBSVolume(**data)


@dataclass
class AWSAutoScalingGroup(BaseResource):
    """
    Represents an Auto Scaling Group in AWS
    """

    healthCheckType: str = None
    instances: BaseList[str] = None  # list of strs
    autoScalingGroupARN: str = None
    availabilityZones: BaseList[str] = None  # list of strs
    launchConfigurationName: str = None
    autoScalingGroupName: str = None
    createdTime: Union[str, datetime] = None
    loadBalancerNames: BaseList[str] = None  # list of ???

    def __post_init__(self):
        STR_BL_FIELDS = [
            "instances",
            "availabilityZones",
            "loadBalancerNames",
            "loadBalancerNames",
        ]

        for field in STR_BL_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for item in data:
                    bl.append(item)
                setattr(self, field, bl)

        if self.createdTime:
            if not isinstance(self.createdTime, datetime):
                setattr(self, "createdTime", datetime.fromisoformat(self.createdTime))

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSAutoScalingGroup object from a dictionary
        """
        return AWSAutoScalingGroup(**data)


@dataclass
class AWSEKSCluster(BaseResource):
    """
    Represents an EKS Cluster in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    associations: None = None  # parse out to below fields
    # associations is parsed out to below fields
    associations_resourcesVpcConfig_clusterSecurityGroupId: str = None
    assiciations_resourcesVpcConfig_securityGroupIds: BaseList[str] = None
    associations_resourcesVpcConfig_vpcId: str = None
    associations_resourcesVpcConfig_subnetIds: BaseList[str] = None
    version: float = None
    endpoint: str = None
    resourcesVpcConfig: None = None  # parse out to below fields
    # resourcesVpcConfig is parsed out to below fields
    resourcesVpcConfig_endpointPrivateAccess: bool = None
    resporcesVpcConfig_endpointPublicAccess: bool = None
    # end of resourcesVpcConfig fields
    roleArn: str = None
    identity: None = None  # parse out to below fields
    # identity is parsed out to below fields
    identity_oidc_issuer: str = None
    # end of identity fields
    platformVersion: str = None
    roleName: str = None
    logging: None = None  # parse out to below fields
    # logging is parsed out to below fields
    logging_clusterLogging: BaseList[str] = None
    # end of logging fields
    arn: str = None
    status: str = None

    def __post_init__(self):
        if self.version:
            setattr(self, "version", float(self.version))

        if self.associations:
            data = self.associations.get("resourcesVpcConfig", None)
            if data:
                for key, value in data.items():
                    if key == "securityGroupIds":
                        bl = BaseList()
                        for group in value:
                            bl.append(group)
                        setattr(
                            self, "associations_resourcesVpcConfig_securityGroupIds", bl
                        )
                    elif key == "subnetIds":
                        bl = BaseList()
                        for subnet in value:
                            bl.append(subnet)
                        setattr(self, "associations_resourcesVpcConfig_subnetIds", bl)
                    else:
                        setattr(self, f"associations_resourcesVpcConfig_{key}", value)
            setattr(self, "associations", None)

        if self.resourcesVpcConfig:
            data = self.resourcesVpcConfig
            for key, value in data.items():
                setattr(self, f"resourcesVpcConfig_{key}", value)
            setattr(self, "resourcesVpcConfig", None)

        if self.identity:
            data = self.identity.get("oidc", None)
            if data:
                data = data.get("issuer", None)
                if data:
                    setattr(self, "identity_oidc_issuer", data)
            setattr(self, "identity", None)

        if self.logging:
            data = self.logging.get("clusterLogging", None)[0]
            if data:
                bl = BaseList()
                i = data.get("types", None)
                for item in i:
                    bl.append(item)
                setattr(self, "logging_clusterLogging", bl)
            setattr(self, "logging", None)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSEKSCluster object from a dictionary
        """
        return AWSEKSCluster(**data)


@dataclass
class AWSEKSNodeGroup(BaseResource):
    """
    Represents an EKS Node Group in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    associations: None = None  # parse out to below fields
    # associations is parsed out to below fields
    associations_clusterArn: str = None
    associations_clusterName: str = None
    associations_subnets: BaseList[str] = None
    associations_resources_autoScalingGroups: BaseList[str] = None
    # end of associations fields
    nodeRoleName: str = None
    scalingConfig: None = None  # parse out to below fields
    # scalingConfig is parsed out to below fields
    scalingConfig_maxSize: int = None
    scalingConfig_desiredSize: int = None
    scalingConfig_minSize: int = None
    # end of scalingConfig fields
    capacityType: str = None
    instanceTypes: BaseList[str] = None
    releaseVersion: str = None
    version: float = None
    labels: BaseList[str] = None
    diskSize: int = None
    nodeRole: str = None
    launchTemplate: None = None  # parse out to below fields
    # launchTemplate is parsed out to below fields
    launchTemplate_name: str = None
    launchTemplate_id: str = None
    launchTemplate_version: str = None
    # end of launchTemplate fields
    amiType: str = None
    status: str = None
    health: BaseList[str] = None

    def __post_init__(self):
        if self.version:
            setattr(self, "version", float(self.version))

        if self.associations:
            data = self.associations
            setattr(self, "associations_clusterArn", data.get("clusterArn", None))
            setattr(self, "associations_clusterName", data.get("clusterName", None))
            subnets = data.get("subnets", None)
            if subnets:
                bl = BaseList()
                for subnet in subnets:
                    bl.append(subnet)
                setattr(self, "associations_subnets", bl)
            resources = data.get("resources", None)
            if resources:
                if resources.get("autoScalingGroups", None):
                    bl = BaseList()
                    for group in resources["autoScalingGroups"]:
                        bl.append(group.get("name", None))
                    setattr(self, "associations_resources_autoScalingGroups", bl)
            setattr(self, "associations", None)

        if self.scalingConfig:
            data = self.scalingConfig
            if data.get("maxSize", None):
                setattr(self, "scalingConfig_maxSize", int(data.get("maxSize", None)))
            if data.get("desiredSize", None):
                setattr(
                    self,
                    "scalingConfig_desiredSize",
                    int(data.get("desiredSize", None)),
                )
            if data.get("minSize", None):
                setattr(self, "scalingConfig_minSize", int(data.get("minSize", None)))
            setattr(self, "scalingConfig", None)

        if self.labels:
            data = self.labels
            bl = BaseList()
            for k, v in data.items():
                bl.append(f"({k}: {v})")

        if self.launchTemplate:
            data = self.launchTemplate
            setattr(self, "launchTemplate_name", data.get("name", None))
            setattr(self, "launchTemplate_id", data.get("id", None))
            setattr(self, "launchTemplate_version", data.get("version", None))
            setattr(self, "launchTemplate", None)

        if self.health:
            data = self.health.get("issues", None)
            if data:
                bl = BaseList()
                for issue in data:
                    code = issue.get("code", None)
                    message = issue.get("message", None)
                    resourceIds = issue.get("resourceIds", None)
                    resourcebl = BaseList()
                    if resourceIds:
                        for resourceId in resourceIds:
                            resourcebl.append(resourceId)
                    bl.append(
                        f"(code: {code}, message: {message}, resourceIds: {resourcebl})"
                    )

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSEKSNodeGroup object from a dictionary
        """
        return AWSEKSNodeGroup(**data)


@dataclass
class AWSEKSFargateProfile(BaseResource):
    """
    Represents an EKS Fargate Profile in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    associations: None = None  # parse out to below fields
    # associations is parsed out to below fields
    associations_clusterArn: str = None
    associations_clusterName: str = None
    associations_subnets: BaseList[str] = None
    # end of associations fields
    podExecutionRoleArn: str = None
    selectors: BaseList[str] = None
    podExecutionRoleName: str = None
    status: str = None

    def __post_init__(self):
        if self.associations:
            data = self.associations
            setattr(self, "associations_clusterArn", data.get("clusterArn", None))
            setattr(self, "associations_clusterName", data.get("clusterName", None))
            subnets = data.get("subnets", None)
            if subnets:
                bl = BaseList()
                for subnet in subnets:
                    bl.append(subnet)
                setattr(self, "associations_subnets", bl)
            setattr(self, "associations", None)

        if self.selectors:
            data = self.selectors
            bl = BaseList()
            for selector in data:
                s = ""
                namespace = selector.get("namespace", None)
                labels = selector.get("labels", None)
                if labels:
                    for k, v in labels.items():
                        s += f"{k}: {v}, "
                    # Take out the last comma and space
                    s = f"[{s[:-2]}]"

                bl.append(f"(namespace: {namespace}, labels: {s})")
            setattr(self, "selectors", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSEKSFargateProfile object from a dictionary
        """
        return AWSEKSFargateProfile(**data)


@dataclass
class AWSVPCEndpoint(BaseResource):
    """
    Represents a VPC Endpoint in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    policyDocument: str = None  # needs parsed with json.loads
    dnsOption: str = None
    serviceName: str = None
    securityGroupSet: BaseList[str] = None  # list of dicts
    privateDnsEnabled: bool = None
    requesterManaged: bool = None
    ipAddressType: str = None
    routeTableIds: BaseList[str] = None  # ???
    vpcEndpointType: str = None
    vpcId: str = None
    state: str = None
    dnsEntrySets: BaseList[str] = None  # list of dicts
    networkInterfaceIds: BaseList[str] = None  # list of strs
    subnetIds: BaseList[str] = None  # list of strs

    def __post_init__(self):
        STR_BL_FIELDS = ["routeTableIds", "networkInterfaceIds", "subnetIds"]

        for field in STR_BL_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for item in data:
                    bl.append(item)
                setattr(self, field, bl)

        if self.policyDocument:
            data = loads(self.policyDocument).get("Statement", None)
            if data:
                bl = BaseList()
                for statement in data:
                    s = ""
                    for key in statement.keys():
                        s += f"{key}: {statement[key]}, "
                    s = f"({s[:-2]})"
                    bl.append(s)
                setattr(self, "policyDocument", bl)

        if self.securityGroupSet:
            data = self.securityGroupSet
            bl = BaseList()
            for group in data:
                groupName = group.get("groupName", None)
                groupId = group.get("groupId", None)
                bl.append(f"(groupName: {groupName}, groupId: {groupId})")
            setattr(self, "securityGroupSet", bl)

        if self.dnsEntrySets:
            data = self.dnsEntrySets
            bl = BaseList()
            for entry in data:
                hostedZoneId = entry.get("hostedZoneId", None)
                dnsName = entry.get("dnsName", None)
                bl.append(f"(hostedZoneId: {hostedZoneId}, dnsName: {dnsName})")
            setattr(self, "dnsEntrySets", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSVPCEndpoint object from a dictionary
        """
        return AWSVPCEndpoint(**data)


@dataclass
class AWSVPCEndpointService(BaseResource):
    """
    Represents a VPC Endpoint Service in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    owner: str = None
    acceptanceRequired: bool = None
    managesVpcEndpoints: bool = None
    availabilityZone: BaseList[str] = None  # list of strs
    baseEndpointDnsName: BaseList[str] = None  # list of strs
    supportedIpAddressType: str = None
    serviceTypes: str = None
    privateDnsName: str = None
    privateDnsNameVerificationState: str = None
    vpcEndpointPolicySupported: bool = None

    def __post_init__(self):
        STR_BL_FIELDS = ["availabilityZone", "baseEndpointDnsName"]

        for field in STR_BL_FIELDS:
            if getattr(self, field):
                data = getattr(self, field)
                bl = BaseList()
                for item in data:
                    bl.append(item)
                setattr(self, field, bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSVPCEndpointService object from a dictionary
        """
        return AWSVPCEndpointService(**data)


@dataclass
class AWSIAMGroup(BaseResource):
    """
    Represents an IAM Group in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    classifications: BaseList[str] = None  # list of strs
    groupId: str = None
    GroupPolicyList: BaseList[str] = None  # list of dicts
    AttachedManagedPolicies: BaseList[str] = None  # list of dicts
    arn: str = None

    def __post_init__(self):
        if self.classifications:
            data = self.classifications
            bl = BaseList()
            for classification in data:
                bl.append(classification)

        if self.GroupPolicyList:
            data = self.GroupPolicyList
            bl = BaseList()
            for policy in data:
                policyName = policy.get("PolicyName", None)
                policyDocument = loads(policy.get("PolicyDocument", None))
                if policyDocument:
                    policyDocument_version = policyDocument.get("Version", None)
                    policyDocument_statement = policyDocument.get("Statement", None)
                    if policyDocument_statement:
                        statementbl = BaseList()
                        if isinstance(policyDocument_statement, list):
                            for statement in policyDocument_statement:
                                action = statement.get("Action", None)
                                resource = statement.get("Resource", None)
                                effect = statement.get("Effect", None)
                                statementbl.append(
                                    f"(Action: {action}, Resource: {resource}, Effect: {effect})"
                                )
                        else:
                            action = policyDocument_statement.get("Action", None)
                            resource = policyDocument_statement.get("Resource", None)
                            effect = policyDocument_statement.get("Effect", None)
                            statementbl.append(
                                f"(Action: {action}, Resource: {resource}, Effect: {effect})"
                            )

                        policyDocument = f"(Version: {policyDocument_version}, Statement: {statementbl})"
                bl.append(
                    f"(policyName: {policyName}, policyDocument: {policyDocument})"
                )
            setattr(self, "GroupPolicyList", bl)

        if self.AttachedManagedPolicies:
            data = self.AttachedManagedPolicies
            bl = BaseList()
            for policy in data:
                policyArn = policy.get("PolicyArn", None)
                policyName = policy.get("PolicyName", None)
                bl.append(f"(PolicyArn: {policyArn}, PolicyName: {policyName})")
            setattr(self, "AttachedManagedPolicies", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSIAMGroup object from a dictionary
        """
        return AWSIAMGroup(**data)


@dataclass
class AWSIAMPolicy(BaseResource):
    """
    Represents an IAM Policy in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    IsAttachable: bool = None
    PermissionsBoundaryUsageCount: int = None
    AttachmentCount: int = None
    DefaultVersionId: str = None
    defaultPolicyVersion: None = None  # parse out to below fields
    # defaultPolicyVersion is parsed out to below fields
    defaultPolicyVersion_VersionId: str = None
    defaultPolicyVersion_IsDefaultVersion: bool = None
    defaultPolicyVersion_Document_Version: str = None
    defaultPolicyVersion_Document_Statement: BaseList[str] = None  # list of dicts
    defaultPolicyVersion_CreateDate: Union[str, datetime] = None
    # end of defaultPolicyVersion fields
    _type: str = None
    path: str = None
    classifications: BaseList[str] = None  # list of strs
    policyId: str = None
    arn: str = None

    def __post_init__(self):
        if self.defaultPolicyVersion:
            data = self.defaultPolicyVersion
            setattr(self, "defaultPolicyVersion_VersionId", data.get("VersionId", None))
            setattr(
                self,
                "defaultPolicyVersion_IsDefaultVersion",
                data.get("IsDefaultVersion", None),
            )
            createDate = data.get("CreateDate", None)
            if createDate:
                setattr(
                    self,
                    "defaultPolicyVersion_CreateDate",
                    datetime.fromtimestamp(createDate),
                )
            document = data.get("Document", None)
            if document:
                document = loads(document)
                setattr(
                    self,
                    "defaultPolicyVersion_Document_Version",
                    document.get("Version", None),
                )
                statement = document.get("Statement", None)
                if statement:
                    bl = BaseList()
                    if isinstance(statement, list):
                        for stmt in statement:
                            resource = stmt.get("Resource", None)
                            stmt.pop("Resource", None)
                            effect = stmt.get("Effect", None)
                            stmt.pop("Effect", None)
                            # For the remaining key (either Action or Condition),
                            # it is a list of strings. We need to convert to BaseList
                            # for consistency
                            is_action = True if "Action" in stmt else False
                            rule = stmt.get("Action", None)
                            stmt.pop("Action", None)
                            if not rule:
                                rule = stmt.get("Condition", None)
                                stmt.pop("Condition", None)
                            if rule:
                                rulebl = BaseList()
                                for r in rule:
                                    rulebl.append(r)
                                rule = rulebl
                    else:
                        resource = statement.get("Resource", None)
                        statement.pop("Resource", None)
                        effect = statement.get("Effect", None)
                        statement.pop("Effect", None)
                        is_action = True if "Action" in statement else False
                        rule = statement.get("Action", None)
                        statement.pop("Action", None)
                        if not rule:
                            rule = statement.get("Condition", None)
                            statement.pop("Condition", None)
                        if rule:
                            rulebl = BaseList()
                            for r in rule:
                                rulebl.append(r)
                            rule = rulebl

                        # Now we have the resource, effect, and rule
                        # Add them to the statement
                        s = f"(Resource: {resource}, Effect: {effect}, {'Action' if is_action else 'Condition'}: {str(rule)})"
                        bl.append(s)
                    setattr(self, "defaultPolicyVersion_Document_Statement", bl)
            setattr(self, "defaultPolicyVersion", None)

        if self.classifications:
            data = self.classifications
            bl = BaseList()
            for classification in data:
                bl.append(classification)
            setattr(self, "classifications", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSIAMPolicy object from a dictionary
        """
        return AWSIAMPolicy(**data)


@dataclass
class AWSIAMRole(BaseResource):
    """
    Represents an IAM Role in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    AttachedManagedPolicies: BaseList[str] = None  # list of dicts
    RoleLastUsed: str = None
    arn: str = None
    roleId: str = None
    PermissionsBoundary: None = None  # parse out to below fields
    # PermissionsBoundary is parsed out to below fields
    PermissionsBoundary_PermissionsBoundaryArn: str = None
    PermissionsBoundary_PermissionsBoundaryType: str = None
    # end of PermissionsBoundary fields
    path: str = None
    classifications: BaseList[str] = None  # list of strs
    AssumeRolePolicyDocument: None = None
    # AssumeRolePolicyDocument is parsed out to below fields
    AssumeRolePolicyDocument_Version: str = None
    AssumeRolePolicyDocument_Statement: BaseList[str] = None
    # end of AssumeRolePolicyDocument fields
    trustedEntities: BaseList[str] = None  # list of strs {'AWS Service': ['ops']}
    RolePolicyList: BaseList[str] = None  # list of dicts
    InstanceProfileList: BaseList[str] = None  # list of dicts

    def __post_init__(self):
        if self.AttachedManagedPolicies:
            data = self.AttachedManagedPolicies
            bl = BaseList()
            for policy in data:
                policyArn = policy.get("PolicyArn", None)
                policyName = policy.get("PolicyName", None)
                bl.append(f"(PolicyArn: {policyArn}, PolicyName: {policyName})")
            setattr(self, "AttachedManagedPolicies", bl)

        if self.PermissionsBoundary:
            data = self.PermissionsBoundary
            setattr(
                self,
                "PermissionsBoundary_PermissionsBoundaryArn",
                data.get("PermissionsBoundaryArn", None),
            )
            setattr(
                self,
                "PermissionsBoundary_PermissionsBoundaryType",
                data.get("PermissionsBoundaryType", None),
            )
            setattr(self, "PermissionsBoundary", None)

        if self.classifications:
            data = self.classifications
            bl = BaseList()
            for classification in data:
                bl.append(classification)
            setattr(self, "classifications", bl)

        if self.AssumeRolePolicyDocument:
            data = loads(self.AssumeRolePolicyDocument)
            setattr(self, "AssumeRolePolicyDocument_Version", data.get("Version", None))
            statement = data.get("Statement", None)
            if statement:
                bl = BaseList()
                for stmt in statement:
                    effect = stmt.get("Effect", None)
                    stmt.pop("Effect", None)
                    principal = stmt.get("Principal", None)
                    stmt.pop("Principal", None)
                    action = stmt.get("Action", None)
                    stmt.pop("Action", None)
                    resource = stmt.get("Resource", None)
                    stmt.pop("Resource", None)
                    s = f"(Effect: {effect}, Principal: {principal}, Action: {action}, Resource: {resource})"
                    bl.append(s)
                setattr(self, "AssumeRolePolicyDocument_Statement", bl)
            setattr(self, "AssumeRolePolicyDocument", None)

        if self.trustedEntities:
            data = self.trustedEntities
            for k, v in data.items():
                formatted = f"{k}: {v}"
            setattr(self, "trustedEntities", formatted)

        if self.RolePolicyList:
            data = self.RolePolicyList
            bl = BaseList()
            for policy in data:
                policyName = policy.get("PolicyName", None)
                policyDocument = loads(policy.get("PolicyDocument", None))
                if policyDocument:
                    policyDocument_version = policyDocument.get("Version", None)
                    policyDocument_statement = policyDocument.get("Statement", None)
                    if policyDocument_statement:
                        if isinstance(policyDocument_statement, list):
                            statementbl = BaseList()
                            for statement in policyDocument_statement:
                                action = statement.get("Action", None)
                                resource = statement.get("Resource", None)
                                effect = statement.get("Effect", None)
                                statementbl.append(
                                    f"(Action: {action}, Resource: {resource}, Effect: {effect})"
                                )
                            policyDocument = f"(Version: {policyDocument_version}, Statement: {statementbl})"
                        else:
                            policyDocument = f"(Version: {policyDocument_version}, Statement: {policyDocument_statement})"
                bl.append(
                    f"(policyName: {policyName}, policyDocument: {policyDocument})"
                )
            setattr(self, "RolePolicyList", bl)

        if self.InstanceProfileList:
            data = self.InstanceProfileList
            bl = BaseList()
            for profile in data:
                path = profile.get("Path", None)
                instanceProfileName = profile.get("InstanceProfileName", None)
                InstanceProfileId = profile.get("InstanceProfileId", None)
                arn = profile.get("Arn", None)
                CreateDate = profile.get("CreateDate", None)  # timestamp
                if CreateDate and not isinstance(CreateDate, datetime):
                    CreateDate = datetime.fromtimestamp(CreateDate)
                roles = profile.get("Roles", None)
                if roles:
                    rolebl = BaseList()
                    for role in roles:
                        rolepath = role.get("Path", None)
                        rolename = role.get("RoleName", None)
                        roleassumeRolePolicyDocument = role.get(
                            "AssumeRolePolicyDocument", None
                        )
                        if roleassumeRolePolicyDocument:
                            roleassumeRolePolicyDocument = unquote(
                                roleassumeRolePolicyDocument
                            )
                        rolearn = role.get("Arn", None)
                        rolecreateDate = role.get("CreateDate", None)
                        if rolecreateDate and not isinstance(rolecreateDate, datetime):
                            rolecreateDate = datetime.fromtimestamp(rolecreateDate)
                        roleId = role.get("RoleId", None)
                        rolestr = f"(Path: {rolepath}, RoleName: {rolename}, Arn: {rolearn}, CreateDate: {rolecreateDate}, RoleId: {roleId}, AssumeRolePolicyDocument: {roleassumeRolePolicyDocument})"
                        rolebl.append(rolestr)
                    roles = rolebl
                s = f"(Path: {path}, InstanceProfileName: {instanceProfileName}, InstanceProfileId: {InstanceProfileId}, Arn: {arn}, CreateDate: {CreateDate}, Roles: {roles})"
                bl.append(s)
            setattr(self, "InstanceProfileList", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSIAMRole object from a dictionary
        """
        return AWSIAMRole(**data)


@dataclass
class AWSSagemakerNotebook(BaseResource):
    """
    Represents a SageMaker Notebook in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    subnetId: str = None
    networkInterfaceId: str = None
    volumeSizeInGB: float = None
    rootAccess: bool = None
    instanceType: str = None
    platformId: str = None
    url: str = None
    directInternetAccess: str = None
    roleArn: str = None
    securityGroups: BaseList[str] = None  # list of strs
    status: str = None
    defaultCodeRepository: str = None
    kmsKeyId: str = None

    def __post_init__(self):
        if self.securityGroups:
            data = self.securityGroups
            bl = BaseList()
            for group in data:
                bl.append(group)
            setattr(self, "securityGroups", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSSagemakerNotebook object from a dictionary
        """
        return AWSSagemakerNotebook(**data)


@dataclass
class AWSCloudfrontDistribution(BaseResource):
    """
    Represents a Cloudfront Distribution in AWS
    """

    connectorId: str = None
    customerId: str = None
    scanId: str = None
    displayName: str = None
    defaultCacheBehavior: None = None  # parse out to below fields
    defaultCacheBehavior_Compress: bool = None
    defaultCacheBehavior_FunctionAssociations_Quantity: int = None
    defaultCacheBehavior_FunctionAssociations_Items: BaseList[str] = None
    defaultCacheBehavior_LambdaFunctionAssociations_Quantity: int = None
    defaultCacheBehavior_LambdaFunctionAssociations_Items: BaseList[str] = None
    defaultCacheBehavior_TargetOriginId: str = None
    defaultCacheBehavior_ViewerProtocolPolicy: str = None
    defaultCacheBehavior_TrustedSigners_Enabled: bool = (
        None  # parsed out of trustedsigners dict
    )
    defaultCacheBehavior_TrustedSigners_Quantity: int = None  # ^^^
    defaultCacheBehavior_FieldLevelEncryptionId: str = None
    defaultCacheBehavior_DefaultTTL: int = None
    defaultCacheBehavior_TrustedKeyGroups_Enabled: bool = (
        None  # parsed out of trustedkeygroups dict
    )
    defaultCacheBehavior_TrustedKeyGroups_Quantity: int = None  # ^^^
    defaultCacheBehavior_AllowedMethods_CachedMethods_Quantity: int = (
        None  # parsed out of allowedmethods dict
    )
    defaultCacheBehavior_AllowedMethods_CachedMethods_Items: BaseList[str] = None  # ^^^
    defaultCacheBehavior_AllowedMethods_Items_Method: BaseList[str] = None  # ^^^
    defaultCacheBehavior_SmoothStreaming: bool = None
    defaultCacheBehavior_MinTTL: int = None
    defaultCacheBehavior_MaxTTL: int = None
    # end of defaultCacheBehavior fields
    loggingEnabled: bool = None
    isIpv6Enabled: bool = None
    includeCookies: bool = None
    geoRestriction: None = None  # parse out to below fields
    geoRestriction_RestrictionType: str = None  # parsed out of georestriction dict
    geoRestriction_Quantity: int = None  # ^^^
    # end of geoRestriction fields
    enabled: bool = None
    webAclId: str = None
    minimumProtocolVersion: str = None
    httpVersion: str = None
    priceClass: str = None
    loggingBucket: str = None
    origins: BaseList[str] = None  # list of dicts
    comment: str = None
    id: str = None
    arn: str = None
    staging: bool = None
    status: str = None
    loggingBucketPrefix: str = None
    acmCertificateARN: str = None

    def __post_init__(self):
        if self.defaultCacheBehavior:
            # Sigh...
            data = self.defaultCacheBehavior
            setattr(self, "defaultCacheBehavior_Compress", data.get("Compress", None))
            setattr(
                self,
                "defaultCacheBehavior_TargetOriginId",
                data.get("TargetOriginId", None),
            )
            setattr(
                self,
                "defaultCacheBehavior_ViewerProtocolPolicy",
                data.get("ViewerProtocolPolicy", None),
            )
            if data.get("TrustedSigners", None):
                setattr(
                    self,
                    "defaultCacheBehavior_TrustedSigners_Enabled",
                    data["TrustedSigners"].get("Enabled", None),
                )
                setattr(
                    self,
                    "defaultCacheBehavior_TrustedSigners_Quantity",
                    data["TrustedSigners"].get("Quantity", None),
                )
            setattr(
                self,
                "defaultCacheBehavior_FieldLevelEncryptionId",
                data.get("FieldLevelEncryptionId", None),
            )
            setattr(
                self, "defaultCacheBehavior_DefaultTTL", data.get("DefaultTTL", None)
            )
            if data.get("TrustedKeyGroups", None):
                setattr(
                    self,
                    "defaultCacheBehavior_TrustedKeyGroups_Enabled",
                    data["TrustedKeyGroups"].get("Enabled", None),
                )
                setattr(
                    self,
                    "defaultCacheBehavior_TrustedKeyGroups_Quantity",
                    data["TrustedKeyGroups"].get("Quantity", None),
                )

            if data.get("FunctionAssociations", None):
                setattr(
                    self,
                    "defaultCacheBehavior_FunctionAssociations_Quantity",
                    data["FunctionAssociations"].get("Quantity", None),
                )
                if data["FunctionAssociations"].get("Items", None):
                    bl = BaseList()
                    for item in data["FunctionAssociations"]["Items"]:
                        bl.append(item)
                    setattr(self, "defaultCacheBehavior_LambdaFunctionAssociations", bl)

            if data.get("LambdaFunctionAssociations", None):
                setattr(
                    self,
                    "defaultCacheBehavior_LambdaFunctionAssociations_Quantity",
                    data["LambdaFunctionAssociations"].get("Quantity", None),
                )
                if data["LambdaFunctionAssociations"].get("Items", None):
                    bl = BaseList()
                    for item in data["LambdaFunctionAssociations"]["Items"]:
                        bl.append(item)
                    setattr(self, "defaultCacheBehavior_LambdaFunctionAssociations", bl)

            if data.get("AllowedMethods", None):
                if data["AllowedMethods"].get("CachedMethods", None):
                    setattr(
                        self,
                        "defaultCacheBehavior_AllowedMethods_CachedMethods_Quantity",
                        data["AllowedMethods"]["CachedMethods"].get("Quantity", None),
                    )
                    if data["AllowedMethods"]["CachedMethods"].get("Items", None):
                        bl = BaseList()
                        for item in data["AllowedMethods"]["CachedMethods"]["Items"][
                            "Method"
                        ]:
                            bl.append(item)
                        setattr(
                            self,
                            "defaultCacheBehavior_AllowedMethods_CachedMethods_Items",
                            bl,
                        )
                if data["AllowedMethods"].get("Items", None):
                    bl = BaseList()
                    for item in data["AllowedMethods"]["Items"]["Method"]:
                        bl.append(item)
                    setattr(
                        self, "defaultCacheBehavior_AllowedMethods_Items_Method", bl
                    )

            setattr(
                self,
                "defaultCacheBehavior_SmoothStreaming",
                data.get("SmoothStreaming", None),
            )
            setattr(self, "defaultCacheBehavior_MinTTL", data.get("MinTTL", None))
            setattr(self, "defaultCacheBehavior_MaxTTL", data.get("MaxTTL", None))
            setattr(self, "defaultCacheBehavior", None)

        if self.geoRestriction:
            restriction = (
                self,
                "geoRestriction_RestrictionType",
                self.geoRestriction.get("RestrictionType", None),
            )
            if restriction == "none":
                restriction = None
            setattr(self, "geoRestriction_RestrictionType", restriction)
            setattr(self, "geoRestriction", None)

        if self.origins:
            data = self.origins
            bl = BaseList()
            for origin in data:
                if isinstance(origin, list):
                    for o in origin:
                        connectionTimeout = o.get("ConnectionTimeout", None)
                        originAccessControlId = o.get("OriginAccessControlId", None)
                        connectionAttempts = o.get("ConnectionAttempts", None)
                        domainName = o.get("DomainName", None)
                        originPath = o.get("OriginPath", None)
                        Id = o.get("Id", None)
                        s = f"(ConnectionTimeout: {connectionTimeout}, OriginAccessControlId: {originAccessControlId}, ConnectionAttempts: {connectionAttempts}, DomainName: {domainName}, OriginPath: {originPath}, Id: {Id})"
                        bl.append(s)
                else:
                    connectionTimeout = origin.get("ConnectionTimeout", None)
                    originAccessControlId = origin.get("OriginAccessControlId", None)
                    connectionAttempts = origin.get("ConnectionAttempts", None)
                    domainName = origin.get("DomainName", None)
                    originPath = origin.get("OriginPath", None)
                    Id = origin.get("Id", None)
                    s = f"(ConnectionTimeout: {connectionTimeout}, OriginAccessControlId: {originAccessControlId}, ConnectionAttempts: {connectionAttempts}, DomainName: {domainName}, OriginPath: {originPath}, Id: {Id})"
                    bl.append(s)
            setattr(self, "origins", bl)

        super().__post_init__()

    @staticmethod
    def from_dict(data):
        """
        from_dict - create an AWSCloudfrontDistribution object from a dictionary
        """
        return AWSCloudfrontDistribution(**data)
