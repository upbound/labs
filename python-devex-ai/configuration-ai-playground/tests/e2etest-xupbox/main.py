from .model.io.upbound.dev.meta.e2etest import v1alpha1 as e2etest
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s

from .model.io.upbound.aws.providerconfig import v1beta1 as providerconfig
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from .model.org.example.platform.ai.xupbox import v1alpha1 as xupbox
from .model.io.upbound.aws.ec2.ebssnapshot import v1beta1 as v1beta1ebssnapshot
from .model.io.upbound.aws.ec2.ebsvolume import v1beta1 as v1beta1ebsvolume
from .model.io.upbound.aws.ec2.instance import v1beta1 as v1beta1instance
from .model.io.upbound.aws.ec2.keypair import v1beta1 as v1beta1keypair

manifest = xupbox.XUpbox(
    metadata=k8s.ObjectMeta(
        name="ai-upbox-vm-us-east-1",
        namespace="default",
    ),
    spec=xupbox.Spec(
        name="markus-schweig",
        networkId="ai-upbox-net-us-east",
        region="us-east-1",
        zone="a",
        size="small",
        publicSshKey="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDPPnjJrm0lsdelQifFC7lbRk8g/au4gdFKHDHcMV0NESuYO4wp0eVInQNQZIpC7onNZVK8nWJc9gggrThS1dNSI5W7J6xTwOZVYkvVicjjSpw9QG3czdBnU1Ywg52bFXbW7PoR79mpTKfMH8uY06jLZZUoFRO0E3misQUQCit/4UM3+YJHDFwvgySSb88HRduVFNslUwGCKzIFl4Ogbk9qNkmcT1o6Je+DLf+PmnbFxWur3NWuu9yLqPmyBbD2pdoCvKfaHtkilUUxw3Jeamq20emHt8o7z+QPCjrrk/Z5Qi3XUsglwTzMkz9AuuLMXPI1eKmgaj5wMyZvONg53w1P40LcrqBW1GbAa28+DIT6ucmb92bgzh9lJM4C55ONKqFaaA6UR1DY/jAq/zDR/w8tIfbyl4iTuJSRMnHEprhZBSB2gmwvT1ZShktUIEp0leWoU1SQgMdol0d13MaynmQxGsTUq8IhI84QFfWw7XuFgd8cd5SKi85Qb3l4TGq6zX8= markuss@Markuss-MacBook-Pro.local"
    )
)


provider_config = providerconfig.ProviderConfig(
    metadata=k8s.ObjectMeta(
        name="default",
    ),
    spec=providerconfig.Spec(
        credentials=providerconfig.Credentials(
            source="Upbound",
            upbound=providerconfig.Upbound(
                webIdentity=providerconfig.WebIdentity(
                    roleARN="arn:aws:iam::782653212346:role/dev_app_upbound",
                ),
            ),
        ),
    ),
)

environment_config = {
    "apiVersion": "apiextensions.crossplane.io/v1beta1",
    "kind": "EnvironmentConfig",
    "metadata": {
        "labels": {
            "aws.schonfeld.com/category": "environment-config",
        },
        "name": "environment-config",
    },
    "data": {
        "isTestCase": True,
        "config": {
            "account": {
                "accountName": "Schonfeld NonProd - DevOps",
                "accountNumber": "782653212346",
                "enabledRegions": [
                    "us-east-1",
                ],
                "appUpboundRoleArn": "arn:aws:iam::782653212346:role/app_upbound",
            },
            "network": {
                "us-east-1": [
                    {
                        "vpc": {
                            "ownerId": "788324288930",
                            "vpcId": "vpc-0b56f09855aa79130",
                            "vpcName": "technology.dev",
                            "cidrBlock": "10.74.64.0/18",
                            "isDefault": False,
                        },
                        "routableSubnets": [
                            {
                                "ownerId": "788324288930",
                                "vpcId": "vpc-0b56f09855aa79130",
                                "subnetId": "subnet-0521eb9457501ee9e",
                                "subnetName": "technology.dev.devopsb",
                                "cidrBlock": "10.74.72.0/24",
                                "availabilityZone": "us-east-1b",
                                "isDefault": False,
                            },
                            {
                                "ownerId": "788324288930",
                                "vpcId": "vpc-0b56f09855aa79130",
                                "subnetId": "subnet-05a1fb222dcdc4f6e",
                                "subnetName": "technology.dev.devopsd",
                                "cidrBlock": "10.74.74.0/24",
                                "availabilityZone": "us-east-1d",
                                "isDefault": False,
                            },
                            {
                                "ownerId": "788324288930",
                                "vpcId": "vpc-0b56f09855aa79130",
                                "subnetId": "subnet-0e957fb644b40b255",
                                "subnetName": "technology.dev.devopsc",
                                "cidrBlock": "10.74.73.0/24",
                                "availabilityZone": "us-east-1c",
                                "isDefault": False,
                            },
                        ],
                        "nonRoutableSubnets": [
                            {
                                "ownerId": "788324288930",
                                "vpcId": "vpc-0b56f09855aa79130",
                                "subnetId": "subnet-0127318ed93afb3be",
                                "subnetName": "technology.dev.private_devopsd",
                                "cidrBlock": "100.64.4.0/23",
                                "availabilityZone": "us-east-1d",
                                "isDefault": False,
                            },
                            {
                                "ownerId": "788324288930",
                                "vpcId": "vpc-0b56f09855aa79130",
                                "subnetId": "subnet-051355c668daf83eb",
                                "subnetName": "technology.dev.private_devopsc",
                                "cidrBlock": "100.64.2.0/23",
                                "availabilityZone": "us-east-1c",
                                "isDefault": False,
                            },
                            {
                                "ownerId": "788324288930",
                                "vpcId": "vpc-0b56f09855aa79130",
                                "subnetId": "subnet-095474dd0a24e6ec7",
                                "subnetName": "technology.dev.private_devopsb",
                                "cidrBlock": "100.64.0.0/23",
                                "availabilityZone": "us-east-1b",
                                "isDefault": False,
                            },
                        ],
                        "otherSubnets": [],
                        "securityGroups": [
                            {
                                "securityGroupName": "default-infra-security-group",
                                "securityGroupId": "sg-0b8ea56ed033bf2e8",
                            },
                            {
                                "securityGroupName": "linux_default.vpc-0b56f09855aa79130",
                                "securityGroupId": "sg-012be04d5e42ec963",
                            },
                        ],
                    }
                ]
            },
            "ec2": {
                "ami": "ami-064026ad811ab2d19",
                "iamProfile": "iDefault",
                "instanceTypes": {
                    "default": "t3.nano",
                    "small": "t3.micro",
                    "medium": "t3.micro",
                    "large": "t3.micro",
                    "xlarge": "t3.micro",
                },
            },
        },
    },
}

deployment_runtime_config = {
    "apiVersion": "pkg.crossplane.io/v1beta1",
    "kind": "DeploymentRuntimeConfig",
    "metadata": {
        "name": "default",
    },
    "spec": {
        "deploymentTemplate": {
            "spec": {
                "selector": {},
                "template": {
                    "metadata": {
                        "annotations": {
                            "proidc.cloud-spaces.upbound.io/audience": "sts.amazonaws.com",
                        },
                    }
                }
            },
        }
    },
}

test = e2etest.E2ETest(
    metadata=k8s.ObjectMeta(
        name="e2etest-xupbox",
    ),
    spec = e2etest.Spec(
        crossplane=e2etest.Crossplane(
            autoUpgrade=e2etest.AutoUpgrade(
                channel="Rapid",
            ),
        ),
        defaultConditions=[
            "Ready",
        ],
        manifests=[manifest.model_dump()],
        extraResources=[deployment_runtime_config],
        skipDelete=False,
        timeoutSeconds=4500,
    )
)
