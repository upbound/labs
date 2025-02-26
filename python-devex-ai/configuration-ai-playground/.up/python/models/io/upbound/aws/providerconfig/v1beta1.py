# generated by datamodel-codegen:
#   filename:  workdir/aws_upbound_io_v1beta1_providerconfig.yaml

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import AwareDatetime, BaseModel

from ....k8s.apimachinery.pkg.apis.meta import v1


class Tag(BaseModel):
    key: str
    """
    Name of the tag.
    Key is a required field
    """
    value: str
    """
    Value of the tag.
    Value is a required field
    """


class AssumeRoleChainItem(BaseModel):
    externalID: Optional[str] = None
    """
    ExternalID is the external ID used when assuming role.
    """
    roleARN: Optional[str] = None
    """
    AssumeRoleARN to assume with provider credentials
    """
    tags: Optional[List[Tag]] = None
    """
    Tags is list of session tags that you want to pass. Each session tag consists of a key
    name and an associated value. For more information about session tags, see
    Tagging STS Sessions
    (https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html).
    """
    transitiveTagKeys: Optional[List[str]] = None
    """
    TransitiveTagKeys is a list of keys for session tags that you want to set as transitive. If you set a
    tag key as transitive, the corresponding key and value passes to subsequent
    sessions in a role chain. For more information, see Chaining Roles with Session Tags
    (https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html#id_session-tags_role-chaining).
    """


class Env(BaseModel):
    name: str
    """
    Name is the name of an environment variable.
    """


class Fs(BaseModel):
    path: str
    """
    Path is a filesystem path.
    """


class SecretRef(BaseModel):
    key: str
    """
    The key to select.
    """
    name: str
    """
    Name of the secret.
    """
    namespace: str
    """
    Namespace of the secret.
    """


class Source(Enum):
    None_ = 'None'
    Secret = 'Secret'
    IRSA = 'IRSA'
    WebIdentity = 'WebIdentity'
    PodIdentity = 'PodIdentity'
    Upbound = 'Upbound'


class SourceModel(Enum):
    Secret = 'Secret'
    Filesystem = 'Filesystem'


class TokenConfig(BaseModel):
    fs: Optional[Fs] = None
    """
    Fs is a reference to a filesystem location that contains credentials that
    must be used to obtain the web identity token.
    """
    secretRef: Optional[SecretRef] = None
    """
    A SecretRef is a reference to a secret key that contains the credentials
    that must be used to obtain the web identity token.
    """
    source: SourceModel
    """
    Source is the source of the web identity token.
    """


class WebIdentity(BaseModel):
    roleARN: Optional[str] = None
    """
    AssumeRoleARN to assume with provider credentials
    """
    roleSessionName: Optional[str] = None
    """
    RoleSessionName is the session name, if you wish to uniquely identify this session.
    """
    tokenConfig: Optional[TokenConfig] = None
    """
    TokenConfig is the Web Identity Token config to assume the role.
    """


class Upbound(BaseModel):
    webIdentity: Optional[WebIdentity] = None
    """
    WebIdentity defines the options for assuming an IAM role with a Web
    Identity.
    """


class Credentials(BaseModel):
    env: Optional[Env] = None
    """
    Env is a reference to an environment variable that contains credentials
    that must be used to connect to the provider.
    """
    fs: Optional[Fs] = None
    """
    Fs is a reference to a filesystem location that contains credentials that
    must be used to connect to the provider.
    """
    secretRef: Optional[SecretRef] = None
    """
    A SecretRef is a reference to a secret key that contains the credentials
    that must be used to connect to the provider.
    """
    source: Source
    """
    Source of the provider credentials.
    """
    upbound: Optional[Upbound] = None
    """
    Upbound defines the options for authenticating using Upbound as an identity provider.
    """
    webIdentity: Optional[WebIdentity] = None
    """
    WebIdentity defines the options for assuming an IAM role with a Web Identity.
    """


class SourceModel1(Enum):
    ServiceMetadata = 'ServiceMetadata'
    Custom = 'Custom'


class Protocol(Enum):
    http = 'http'
    https = 'https'


class Dynamic(BaseModel):
    host: str
    """
    Host is the address of the main host that the resolver will use to
    prepend protocol, service and region configurations.
    For example, the final URL for EC2 in us-east-1 looks like https://ec2.us-east-1.amazonaws.com
    You would need to use "amazonaws.com" as Host and "https" as protocol
    to have the resolver construct it.
    """
    protocol: Protocol
    """
    Protocol is the HTTP protocol that will be used in the URL. Currently,
    only http and https are supported.
    """


class Type(Enum):
    Static = 'Static'
    Dynamic = 'Dynamic'
    Auto = 'Auto'


class Url(BaseModel):
    dynamic: Optional[Dynamic] = None
    """
    Dynamic lets you configure the behavior of endpoint URL resolver.
    """
    static: Optional[str] = None
    """
    Static is the full URL you'd like the AWS SDK to use.
    Recommended for using tools like localstack where a single host is exposed
    for all services and regions.
    """
    type: Type
    """
    You can provide a static URL that will be used regardless of the service
    and region by choosing Static type. Alternatively, you can provide
    configuration for dynamically resolving the URL with the config you provide
    once you set the type as Dynamic.
    """


class Endpoint(BaseModel):
    hostnameImmutable: Optional[bool] = None
    """
    Specifies if the endpoint's hostname can be modified by the SDK's API
    client.


    If the hostname is mutable the SDK API clients may modify any part of
    the hostname based on the requirements of the API, (e.g. adding, or
    removing content in the hostname). Such as, Amazon S3 API client
    prefixing "bucketname" to the hostname, or changing the
    hostname service name component from "s3." to "s3-accesspoint.dualstack."
    for the dualstack endpoint of an S3 Accesspoint resource.


    Care should be taken when providing a custom endpoint for an API. If the
    endpoint hostname is mutable, and the client cannot modify the endpoint
    correctly, the operation call will most likely fail, or have undefined
    behavior.


    If hostname is immutable, the SDK API clients will not modify the
    hostname of the URL. This may cause the API client not to function
    correctly if the API requires the operation specific hostname values
    to be used by the client.


    This flag does not modify the API client's behavior if this endpoint
    will be used instead of Endpoint Discovery, or if the endpoint will be
    used to perform Endpoint Discovery. That behavior is configured via the
    API Client's Options.
    Note that this is effective only for resources that use AWS SDK v2.
    """
    partitionId: Optional[str] = None
    """
    The AWS partition the endpoint belongs to.
    """
    services: Optional[List[str]] = None
    """
    Specifies the list of services you want endpoint to be used for
    """
    signingMethod: Optional[str] = None
    """
    The signing method that should be used for signing the requests to the
    endpoint.
    """
    signingName: Optional[str] = None
    """
    The service name that should be used for signing the requests to the
    endpoint.
    """
    signingRegion: Optional[str] = None
    """
    The region that should be used for signing the request to the endpoint.
    For IAM, which doesn't have any region, us-east-1 is used to sign the
    requests, which is the only signing region of IAM.
    """
    source: Optional[SourceModel1] = None
    """
    The source of the Endpoint. By default, this will be ServiceMetadata.
    When providing a custom endpoint, you should set the source as Custom.
    If source is not provided when providing a custom endpoint, the SDK may not
    perform required host mutations correctly. Source should be used along with
    HostnameImmutable property as per the usage requirement.
    Note that this is effective only for resources that use AWS SDK v2.
    """
    url: Url
    """
    URL lets you configure the endpoint URL to be used in SDK calls.
    """


class Spec(BaseModel):
    assumeRoleChain: Optional[List[AssumeRoleChainItem]] = None
    """
    AssumeRoleChain defines the options for assuming an IAM role
    """
    credentials: Credentials
    """
    Credentials required to authenticate to this provider.
    """
    endpoint: Optional[Endpoint] = None
    """
    Endpoint is where you can override the default endpoint configuration
    of AWS calls made by the provider.
    """
    s3_use_path_style: Optional[bool] = None
    """
    Whether to enable the request to use path-style addressing, i.e., https://s3.amazonaws.com/BUCKET/KEY.
    """
    skip_credentials_validation: Optional[bool] = None
    """
    Whether to skip credentials validation via the STS API.
    This can be useful for testing and for AWS API implementations that do not have STS available.
    """
    skip_metadata_api_check: Optional[bool] = None
    """
    Whether to skip the AWS Metadata API check
    Useful for AWS API implementations that do not have a metadata API endpoint.
    """
    skip_region_validation: Optional[bool] = None
    """
    Whether to skip validation of provided region name.
    Useful for AWS-like implementations that use their own region names or to bypass the validation for
    regions that aren't publicly available yet.
    """
    skip_requesting_account_id: Optional[bool] = None
    """
    Whether to skip requesting the account ID.
    Useful for AWS API implementations that do not have the IAM, STS API, or metadata API
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
    conditions: Optional[List[Condition]] = None
    """
    Conditions of the resource.
    """
    users: Optional[int] = None
    """
    Users of this provider configuration.
    """


class ProviderConfig(BaseModel):
    apiVersion: Optional[str] = 'aws.upbound.io/v1beta1'
    """
    APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """
    kind: Optional[str] = 'ProviderConfig'
    """
    Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """
    metadata: Optional[v1.ObjectMeta] = None
    """
    Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    """
    spec: Spec
    """
    A ProviderConfigSpec defines the desired state of a ProviderConfig.
    """
    status: Optional[Status] = None
    """
    A ProviderConfigStatus reflects the observed state of a ProviderConfig.
    """


class ProviderConfigList(BaseModel):
    apiVersion: Optional[str] = None
    """
    APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """
    items: List[ProviderConfig]
    """
    List of providerconfigs. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md
    """
    kind: Optional[str] = None
    """
    Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """
    metadata: Optional[v1.ListMeta] = None
    """
    Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """