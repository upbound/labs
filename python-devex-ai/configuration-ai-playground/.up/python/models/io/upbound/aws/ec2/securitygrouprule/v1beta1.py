# generated by datamodel-codegen:
#   filename:  workdir/ec2_aws_upbound_io_v1beta1_securitygrouprule.yaml

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import AwareDatetime, BaseModel, Field

from .....k8s.apimachinery.pkg.apis.meta import v1


class DeletionPolicy(Enum):
    Orphan = 'Orphan'
    Delete = 'Delete'


class Resolution(Enum):
    Required = 'Required'
    Optional = 'Optional'


class Resolve(Enum):
    Always = 'Always'
    IfNotPresent = 'IfNotPresent'


class Policy(BaseModel):
    resolution: Optional[Resolution] = 'Required'
    """
    Resolution specifies whether resolution of this reference is required.
    The default is 'Required', which means the reconcile will fail if the
    reference cannot be resolved. 'Optional' means this reference will be
    a no-op if it cannot be resolved.
    """
    resolve: Optional[Resolve] = None
    """
    Resolve specifies when this reference should be resolved. The default
    is 'IfNotPresent', which will attempt to resolve the reference only when
    the corresponding field is not present. Use 'Always' to resolve the
    reference on every reconcile.
    """


class CidrBlocksRef(BaseModel):
    name: str
    """
    Name of the referenced object.
    """
    policy: Optional[Policy] = None
    """
    Policies for referencing.
    """


class CidrBlocksSelector(BaseModel):
    matchControllerRef: Optional[bool] = None
    """
    MatchControllerRef ensures an object with the same controller reference
    as the selecting object is selected.
    """
    matchLabels: Optional[Dict[str, str]] = None
    """
    MatchLabels ensures an object with matching labels is selected.
    """
    policy: Optional[Policy] = None
    """
    Policies for selection.
    """


class Ipv6CidrBlocksRef(BaseModel):
    name: str
    """
    Name of the referenced object.
    """
    policy: Optional[Policy] = None
    """
    Policies for referencing.
    """


class Ipv6CidrBlocksSelector(BaseModel):
    matchControllerRef: Optional[bool] = None
    """
    MatchControllerRef ensures an object with the same controller reference
    as the selecting object is selected.
    """
    matchLabels: Optional[Dict[str, str]] = None
    """
    MatchLabels ensures an object with matching labels is selected.
    """
    policy: Optional[Policy] = None
    """
    Policies for selection.
    """


class PrefixListIdRef(BaseModel):
    name: str
    """
    Name of the referenced object.
    """
    policy: Optional[Policy] = None
    """
    Policies for referencing.
    """


class PrefixListIdSelector(BaseModel):
    matchControllerRef: Optional[bool] = None
    """
    MatchControllerRef ensures an object with the same controller reference
    as the selecting object is selected.
    """
    matchLabels: Optional[Dict[str, str]] = None
    """
    MatchLabels ensures an object with matching labels is selected.
    """
    policy: Optional[Policy] = None
    """
    Policies for selection.
    """


class SecurityGroupIdRef(BaseModel):
    name: str
    """
    Name of the referenced object.
    """
    policy: Optional[Policy] = None
    """
    Policies for referencing.
    """


class SecurityGroupIdSelector(BaseModel):
    matchControllerRef: Optional[bool] = None
    """
    MatchControllerRef ensures an object with the same controller reference
    as the selecting object is selected.
    """
    matchLabels: Optional[Dict[str, str]] = None
    """
    MatchLabels ensures an object with matching labels is selected.
    """
    policy: Optional[Policy] = None
    """
    Policies for selection.
    """


class SourceSecurityGroupIdRef(BaseModel):
    name: str
    """
    Name of the referenced object.
    """
    policy: Optional[Policy] = None
    """
    Policies for referencing.
    """


class SourceSecurityGroupIdSelector(BaseModel):
    matchControllerRef: Optional[bool] = None
    """
    MatchControllerRef ensures an object with the same controller reference
    as the selecting object is selected.
    """
    matchLabels: Optional[Dict[str, str]] = None
    """
    MatchLabels ensures an object with matching labels is selected.
    """
    policy: Optional[Policy] = None
    """
    Policies for selection.
    """


class ForProvider(BaseModel):
    cidrBlocks: Optional[List[str]] = None
    """
    List of CIDR blocks. Cannot be specified with source_security_group_id or self.
    """
    cidrBlocksRefs: Optional[List[CidrBlocksRef]] = None
    """
    References to VPC in ec2 to populate cidrBlocks.
    """
    cidrBlocksSelector: Optional[CidrBlocksSelector] = None
    """
    Selector for a list of VPC in ec2 to populate cidrBlocks.
    """
    description: Optional[str] = None
    """
    Description of the rule.
    """
    fromPort: Optional[float] = None
    """
    Start port (or ICMP type number if protocol is "icmp" or "icmpv6").
    """
    ipv6CidrBlocks: Optional[List[str]] = None
    """
    List of IPv6 CIDR blocks. Cannot be specified with source_security_group_id or self.
    """
    ipv6CidrBlocksRefs: Optional[List[Ipv6CidrBlocksRef]] = None
    """
    References to VPC in ec2 to populate ipv6CidrBlocks.
    """
    ipv6CidrBlocksSelector: Optional[Ipv6CidrBlocksSelector] = None
    """
    Selector for a list of VPC in ec2 to populate ipv6CidrBlocks.
    """
    prefixListIdRefs: Optional[List[PrefixListIdRef]] = None
    """
    References to ManagedPrefixList in ec2 to populate prefixListIds.
    """
    prefixListIdSelector: Optional[PrefixListIdSelector] = None
    """
    Selector for a list of ManagedPrefixList in ec2 to populate prefixListIds.
    """
    prefixListIds: Optional[List[str]] = None
    """
    List of Prefix List IDs.
    """
    protocol: Optional[str] = None
    """
    Protocol. If not icmp, icmpv6, tcp, udp, or all use the protocol number
    """
    region: str
    """
    Region is the region you'd like your resource to be created in.
    """
    securityGroupId: Optional[str] = None
    """
    Security group to apply this rule to.
    """
    securityGroupIdRef: Optional[SecurityGroupIdRef] = None
    """
    Reference to a SecurityGroup in ec2 to populate securityGroupId.
    """
    securityGroupIdSelector: Optional[SecurityGroupIdSelector] = None
    """
    Selector for a SecurityGroup in ec2 to populate securityGroupId.
    """
    self: Optional[bool] = None
    """
    Whether the security group itself will be added as a source to this ingress rule. Cannot be specified with cidr_blocks, ipv6_cidr_blocks, or source_security_group_id.
    """
    sourceSecurityGroupId: Optional[str] = None
    """
    Security group id to allow access to/from, depending on the type. Cannot be specified with cidr_blocks, ipv6_cidr_blocks, or self.
    """
    sourceSecurityGroupIdRef: Optional[SourceSecurityGroupIdRef] = None
    """
    Reference to a SecurityGroup in ec2 to populate sourceSecurityGroupId.
    """
    sourceSecurityGroupIdSelector: Optional[SourceSecurityGroupIdSelector] = None
    """
    Selector for a SecurityGroup in ec2 to populate sourceSecurityGroupId.
    """
    toPort: Optional[float] = None
    """
    End port (or ICMP code if protocol is "icmp").
    """
    type: Optional[str] = None
    """
    Type of rule being created. Valid options are ingress (inbound)
    or egress (outbound).
    """


class InitProvider(BaseModel):
    cidrBlocks: Optional[List[str]] = None
    """
    List of CIDR blocks. Cannot be specified with source_security_group_id or self.
    """
    cidrBlocksRefs: Optional[List[CidrBlocksRef]] = None
    """
    References to VPC in ec2 to populate cidrBlocks.
    """
    cidrBlocksSelector: Optional[CidrBlocksSelector] = None
    """
    Selector for a list of VPC in ec2 to populate cidrBlocks.
    """
    description: Optional[str] = None
    """
    Description of the rule.
    """
    fromPort: Optional[float] = None
    """
    Start port (or ICMP type number if protocol is "icmp" or "icmpv6").
    """
    ipv6CidrBlocks: Optional[List[str]] = None
    """
    List of IPv6 CIDR blocks. Cannot be specified with source_security_group_id or self.
    """
    ipv6CidrBlocksRefs: Optional[List[Ipv6CidrBlocksRef]] = None
    """
    References to VPC in ec2 to populate ipv6CidrBlocks.
    """
    ipv6CidrBlocksSelector: Optional[Ipv6CidrBlocksSelector] = None
    """
    Selector for a list of VPC in ec2 to populate ipv6CidrBlocks.
    """
    prefixListIdRefs: Optional[List[PrefixListIdRef]] = None
    """
    References to ManagedPrefixList in ec2 to populate prefixListIds.
    """
    prefixListIdSelector: Optional[PrefixListIdSelector] = None
    """
    Selector for a list of ManagedPrefixList in ec2 to populate prefixListIds.
    """
    prefixListIds: Optional[List[str]] = None
    """
    List of Prefix List IDs.
    """
    protocol: Optional[str] = None
    """
    Protocol. If not icmp, icmpv6, tcp, udp, or all use the protocol number
    """
    securityGroupId: Optional[str] = None
    """
    Security group to apply this rule to.
    """
    securityGroupIdRef: Optional[SecurityGroupIdRef] = None
    """
    Reference to a SecurityGroup in ec2 to populate securityGroupId.
    """
    securityGroupIdSelector: Optional[SecurityGroupIdSelector] = None
    """
    Selector for a SecurityGroup in ec2 to populate securityGroupId.
    """
    self: Optional[bool] = None
    """
    Whether the security group itself will be added as a source to this ingress rule. Cannot be specified with cidr_blocks, ipv6_cidr_blocks, or source_security_group_id.
    """
    sourceSecurityGroupId: Optional[str] = None
    """
    Security group id to allow access to/from, depending on the type. Cannot be specified with cidr_blocks, ipv6_cidr_blocks, or self.
    """
    sourceSecurityGroupIdRef: Optional[SourceSecurityGroupIdRef] = None
    """
    Reference to a SecurityGroup in ec2 to populate sourceSecurityGroupId.
    """
    sourceSecurityGroupIdSelector: Optional[SourceSecurityGroupIdSelector] = None
    """
    Selector for a SecurityGroup in ec2 to populate sourceSecurityGroupId.
    """
    toPort: Optional[float] = None
    """
    End port (or ICMP code if protocol is "icmp").
    """
    type: Optional[str] = None
    """
    Type of rule being created. Valid options are ingress (inbound)
    or egress (outbound).
    """


class ManagementPolicy(Enum):
    Observe = 'Observe'
    Create = 'Create'
    Update = 'Update'
    Delete = 'Delete'
    LateInitialize = 'LateInitialize'
    field_ = '*'


class ProviderConfigRef(BaseModel):
    name: str
    """
    Name of the referenced object.
    """
    policy: Optional[Policy] = None
    """
    Policies for referencing.
    """


class ConfigRef(BaseModel):
    name: str
    """
    Name of the referenced object.
    """
    policy: Optional[Policy] = None
    """
    Policies for referencing.
    """


class Metadata(BaseModel):
    annotations: Optional[Dict[str, str]] = None
    """
    Annotations are the annotations to be added to connection secret.
    - For Kubernetes secrets, this will be used as "metadata.annotations".
    - It is up to Secret Store implementation for others store types.
    """
    labels: Optional[Dict[str, str]] = None
    """
    Labels are the labels/tags to be added to connection secret.
    - For Kubernetes secrets, this will be used as "metadata.labels".
    - It is up to Secret Store implementation for others store types.
    """
    type: Optional[str] = None
    """
    Type is the SecretType for the connection secret.
    - Only valid for Kubernetes Secret Stores.
    """


class PublishConnectionDetailsTo(BaseModel):
    configRef: Optional[ConfigRef] = Field(
        default_factory=lambda: ConfigRef.model_validate({'name': 'default'})
    )
    """
    SecretStoreConfigRef specifies which secret store config should be used
    for this ConnectionSecret.
    """
    metadata: Optional[Metadata] = None
    """
    Metadata is the metadata for connection secret.
    """
    name: str
    """
    Name is the name of the connection secret.
    """


class WriteConnectionSecretToRef(BaseModel):
    name: str
    """
    Name of the secret.
    """
    namespace: str
    """
    Namespace of the secret.
    """


class Spec(BaseModel):
    deletionPolicy: Optional[DeletionPolicy] = 'Delete'
    """
    DeletionPolicy specifies what will happen to the underlying external
    when this managed resource is deleted - either "Delete" or "Orphan" the
    external resource.
    This field is planned to be deprecated in favor of the ManagementPolicies
    field in a future release. Currently, both could be set independently and
    non-default values would be honored if the feature flag is enabled.
    See the design doc for more information: https://github.com/crossplane/crossplane/blob/499895a25d1a1a0ba1604944ef98ac7a1a71f197/design/design-doc-observe-only-resources.md?plain=1#L223
    """
    forProvider: ForProvider
    initProvider: Optional[InitProvider] = None
    """
    THIS IS A BETA FIELD. It will be honored
    unless the Management Policies feature flag is disabled.
    InitProvider holds the same fields as ForProvider, with the exception
    of Identifier and other resource reference fields. The fields that are
    in InitProvider are merged into ForProvider when the resource is created.
    The same fields are also added to the terraform ignore_changes hook, to
    avoid updating them after creation. This is useful for fields that are
    required on creation, but we do not desire to update them after creation,
    for example because of an external controller is managing them, like an
    autoscaler.
    """
    managementPolicies: Optional[List[ManagementPolicy]] = ['*']
    """
    THIS IS A BETA FIELD. It is on by default but can be opted out
    through a Crossplane feature flag.
    ManagementPolicies specify the array of actions Crossplane is allowed to
    take on the managed and external resources.
    This field is planned to replace the DeletionPolicy field in a future
    release. Currently, both could be set independently and non-default
    values would be honored if the feature flag is enabled. If both are
    custom, the DeletionPolicy field will be ignored.
    See the design doc for more information: https://github.com/crossplane/crossplane/blob/499895a25d1a1a0ba1604944ef98ac7a1a71f197/design/design-doc-observe-only-resources.md?plain=1#L223
    and this one: https://github.com/crossplane/crossplane/blob/444267e84783136daa93568b364a5f01228cacbe/design/one-pager-ignore-changes.md
    """
    providerConfigRef: Optional[ProviderConfigRef] = Field(
        default_factory=lambda: ProviderConfigRef.model_validate({'name': 'default'})
    )
    """
    ProviderConfigReference specifies how the provider that will be used to
    create, observe, update, and delete this managed resource should be
    configured.
    """
    publishConnectionDetailsTo: Optional[PublishConnectionDetailsTo] = None
    """
    PublishConnectionDetailsTo specifies the connection secret config which
    contains a name, metadata and a reference to secret store config to
    which any connection details for this managed resource should be written.
    Connection details frequently include the endpoint, username,
    and password required to connect to the managed resource.
    """
    writeConnectionSecretToRef: Optional[WriteConnectionSecretToRef] = None
    """
    WriteConnectionSecretToReference specifies the namespace and name of a
    Secret to which any connection details for this managed resource should
    be written. Connection details frequently include the endpoint, username,
    and password required to connect to the managed resource.
    This field is planned to be replaced in a future release in favor of
    PublishConnectionDetailsTo. Currently, both could be set independently
    and connection details would be published to both without affecting
    each other.
    """


class AtProvider(BaseModel):
    cidrBlocks: Optional[List[str]] = None
    """
    List of CIDR blocks. Cannot be specified with source_security_group_id or self.
    """
    description: Optional[str] = None
    """
    Description of the rule.
    """
    fromPort: Optional[float] = None
    """
    Start port (or ICMP type number if protocol is "icmp" or "icmpv6").
    """
    id: Optional[str] = None
    """
    ID of the security group rule.
    """
    ipv6CidrBlocks: Optional[List[str]] = None
    """
    List of IPv6 CIDR blocks. Cannot be specified with source_security_group_id or self.
    """
    prefixListIds: Optional[List[str]] = None
    """
    List of Prefix List IDs.
    """
    protocol: Optional[str] = None
    """
    Protocol. If not icmp, icmpv6, tcp, udp, or all use the protocol number
    """
    securityGroupId: Optional[str] = None
    """
    Security group to apply this rule to.
    """
    securityGroupRuleId: Optional[str] = None
    """
    If the aws_security_group_rule resource has a single source or destination then this is the AWS Security Group Rule resource ID. Otherwise it is empty.
    """
    self: Optional[bool] = None
    """
    Whether the security group itself will be added as a source to this ingress rule. Cannot be specified with cidr_blocks, ipv6_cidr_blocks, or source_security_group_id.
    """
    sourceSecurityGroupId: Optional[str] = None
    """
    Security group id to allow access to/from, depending on the type. Cannot be specified with cidr_blocks, ipv6_cidr_blocks, or self.
    """
    toPort: Optional[float] = None
    """
    End port (or ICMP code if protocol is "icmp").
    """
    type: Optional[str] = None
    """
    Type of rule being created. Valid options are ingress (inbound)
    or egress (outbound).
    """


class Condition(BaseModel):
    lastTransitionTime: AwareDatetime
    """
    LastTransitionTime is the last time this condition transitioned from one
    status to another.
    """
    message: Optional[str] = None
    """
    A Message containing details about this condition's last transition from
    one status to another, if any.
    """
    observedGeneration: Optional[int] = None
    """
    ObservedGeneration represents the .metadata.generation that the condition was set based upon.
    For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9, the condition is out of date
    with respect to the current state of the instance.
    """
    reason: str
    """
    A Reason for this condition's last transition from one status to another.
    """
    status: str
    """
    Status of this condition; is it currently True, False, or Unknown?
    """
    type: str
    """
    Type of this condition. At most one of each condition type may apply to
    a resource at any point in time.
    """


class Status(BaseModel):
    atProvider: Optional[AtProvider] = None
    conditions: Optional[List[Condition]] = None
    """
    Conditions of the resource.
    """
    observedGeneration: Optional[int] = None
    """
    ObservedGeneration is the latest metadata.generation
    which resulted in either a ready state, or stalled due to error
    it can not recover from without human intervention.
    """


class SecurityGroupRule(BaseModel):
    apiVersion: Optional[str] = 'ec2.aws.upbound.io/v1beta1'
    """
    APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """
    kind: Optional[str] = 'SecurityGroupRule'
    """
    Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """
    metadata: Optional[v1.ObjectMeta] = None
    """
    Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    """
    spec: Spec
    """
    SecurityGroupRuleSpec defines the desired state of SecurityGroupRule
    """
    status: Optional[Status] = None
    """
    SecurityGroupRuleStatus defines the observed state of SecurityGroupRule.
    """


class SecurityGroupRuleList(BaseModel):
    apiVersion: Optional[str] = None
    """
    APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """
    items: List[SecurityGroupRule]
    """
    List of securitygrouprules. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md
    """
    kind: Optional[str] = None
    """
    Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """
    metadata: Optional[v1.ListMeta] = None
    """
    Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """