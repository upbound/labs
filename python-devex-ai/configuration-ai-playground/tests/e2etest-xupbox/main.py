from .model.io.upbound.dev.meta.e2etest import v1alpha1 as e2etest
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s

test = e2etest.E2ETest(
    metadata=k8s.ObjectMeta(
        name="",
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
        manifests=[examples/upbox/ai-upbox-vm-us-east-1-xr.yaml],
        extraResources=[],
        skipDelete=False,
        timeoutSeconds=4500,
    )
)
