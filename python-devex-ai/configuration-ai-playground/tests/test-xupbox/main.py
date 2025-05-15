from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1
from .model.io.upbound.aws.ec2.ebssnapshot import v1beta1 as ebs_snapshot
from .model.io.upbound.aws.ec2.instance import v1beta1 as v1beta1instance
from .model.io.upbound.dev.meta.compositiontest import v1alpha1 as compositiontest

instance=v1beta1instance.Instance(
    apiVersion="ec2.aws.upbound.io/v1beta1",
    kind="Instance",
    metadata=metav1.ObjectMeta(
        annotations={
            "name": "test-upbox-id"
        },
        labels={
            "upbox.aws.platform.upbound.io/id": "test-upbox-id",
            "upbox.aws.platform.upbound.io/owner": "upbound"
        },
        name="test-upbox-id"
    ),
    spec=v1beta1instance.Spec(
        forProvider=v1beta1instance.ForProvider(
            region="us-east-1a",
            instanceType="small"
        )
    )
)

test = compositiontest.CompositionTest(
    metadata=k8s.ObjectMeta(
        name="test-xupbox",
    ),
    spec = compositiontest.Spec(
        assertResources=[instance.model_dump(exclude_unset=True)],
        compositionPath="apis/xupboxes/composition.yaml",
        xrPath="examples/upbox/ai-upbox-vm-us-east-1-xr.yaml",
        xrdPath="apis/xupboxes/definition.yaml",
        timeoutSeconds=120,
        validate=False,
    )
)
