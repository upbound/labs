from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1
from .model.io.upbound.aws.ec2.ebssnapshot import v1beta1 as v1beta1ebssnapshot
from .model.io.upbound.aws.ec2.ebsvolume import v1beta1 as v1beta1ebsvolume
from .model.io.upbound.aws.ec2.instance import v1beta1 as v1beta1instance
from .model.io.upbound.aws.ec2.keypair import v1beta1 as v1beta1keypair
from .model.io.upbound.dev.meta.compositiontest import v1alpha1 as compositiontest

desired_subnet_id_selector_labels={
    "networks.aws.platform.upbound.io/id": "ai-upbox-net-us-east",
    "access": "public",
    "zone": "us-east-1a"
}

desired_vpc_security_group_id_selector_labels={
    "networks.aws.platform.upbound.io/id": "ai-upbox-net-us-east",
    "networks.aws.platform.upbound.io/type": "ssh"
}

ebsvolume=v1beta1ebsvolume.EBSVolume(
    apiVersion="ec2.aws.upbound.io/v1beta1",
    kind="EBSVolume",
    metadata=metav1.ObjectMeta(
        labels={
            "instances.aws.platform.upbound.io/id": "ebsvolume"
        }
    ),
    spec=v1beta1ebsvolume.Spec(
        forProvider=v1beta1ebsvolume.ForProvider(
            availabilityZone="us-east-1a",
            region="us-east-1"
        )
    )
)

ebssnapshot=v1beta1ebssnapshot.EBSSnapshot(
    apiVersion="ec2.aws.upbound.io/v1beta1",
    kind="EBSSnapshot",
    metadata=metav1.ObjectMeta(
        labels={
            "instances.aws.platform.upbound.io/id": "snapshot"
        }
    ),
    spec=v1beta1ebssnapshot.Spec(
        forProvider=v1beta1ebssnapshot.ForProvider(
            volumeIdSelector=v1beta1ebssnapshot.VolumeIdSelector(
                matchControllerRef=True,
                matchLabels={
                    "instances.aws.platform.upbound.io/id": "ebsvolume"
                }
            ),
            region="us-east-1",
        )
    )
)

keypair=v1beta1keypair.KeyPair(
    apiVersion="ec2.aws.upbound.io/v1beta1",
    kind="KeyPair",
    metadata=metav1.ObjectMeta(
        labels={
            "instances.aws.platform.upbound.io/id": "key-markus-schweig"
        },
        name="key-markus-schweig"
    ),
    spec=v1beta1keypair.Spec(
        forProvider=v1beta1keypair.ForProvider(
            publicKey="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDPPnjJrm0lsdelQifFC7lbRk8g/au4gdFKHDHcMV0NESuYO4wp0eVInQNQZIpC7onNZVK8nWJc9gggrThS1dNSI5W7J6xTwOZVYkvVicjjSpw9QG3czdBnU1Ywg52bFXbW7PoR79mpTKfMH8uY06jLZZUoFRO0E3misQUQCit/4UM3+YJHDFwvgySSb88HRduVFNslUwGCKzIFl4Ogbk9qNkmcT1o6Je+DLf+PmnbFxWur3NWuu9yLqPmyBbD2pdoCvKfaHtkilUUxw3Jeamq20emHt8o7z+QPCjrrk/Z5Qi3XUsglwTzMkz9AuuLMXPI1eKmgaj5wMyZvONg53w1P40LcrqBW1GbAa28+DIT6ucmb92bgzh9lJM4C55ONKqFaaA6UR1DY/jAq/zDR/w8tIfbyl4iTuJSRMnHEprhZBSB2gmwvT1ZShktUIEp0leWoU1SQgMdol0d13MaynmQxGsTUq8IhI84QFfWw7XuFgd8cd5SKi85Qb3l4TGq6zX8= markuss@Markuss-MacBook-Pro.local",
            region="us-east-1"
        )
    )
)

instance=v1beta1instance.Instance(
    apiVersion="ec2.aws.upbound.io/v1beta1",
    kind="Instance",
    metadata=metav1.ObjectMeta(
        annotations={
            "name": "huggingface-deep-learning-neuron-markus-schweig"
        },
        labels={
            "upbox.aws.platform.upbound.io/id": "huggingface-deep-learning-neuron-markus-schweig",
            "upbox.aws.platform.upbound.io/owner": ""
        },
        name="huggingface-deep-learning-neuron-markus-schweig"
    ),
    spec=v1beta1instance.Spec(
        forProvider=v1beta1instance.ForProvider(
            region="us-east-1",
            instanceType="inf2.xlarge",
            associatePublicIpAddress=True,
            ami="ami-0f9a795e2d1186fe3",
            keyName="key-markus-schweig",
            subnetIdSelector=v1beta1instance.SubnetIdSelector(
                matchLabels=desired_subnet_id_selector_labels
            ),
            vpcSecurityGroupIdSelector=v1beta1instance.VpcSecurityGroupIdSelector(
                matchLabels=desired_vpc_security_group_id_selector_labels
            ),
        )
    )
)

test = compositiontest.CompositionTest(
    metadata=k8s.ObjectMeta(
        name="test-xupbox",
    ),
    spec = compositiontest.Spec(
        assertResources=[instance.model_dump(exclude_unset=True),keypair.model_dump(exclude_unset=True),ebsvolume.model_dump(exclude_unset=True)],
        compositionPath="apis/xupboxes/composition.yaml",
        xrPath="examples/upbox/ai-upbox-vm-us-east-1-xr.yaml",
        xrdPath="apis/xupboxes/definition.yaml",
        timeoutSeconds=120,
        validate=False,
    )
)
