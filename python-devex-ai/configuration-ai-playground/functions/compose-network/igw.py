""" Compose Network Internet Gateway Resources """
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1
from .model.org.example.platform.ai.network import v1alpha1
from .model.io.upbound.aws.ec2.internetgateway import v1beta1 as internet_gateway_v1beta1


def compose_igw(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse, config):
    """Function composing Internet Gateway managed resources."""

    log=logging.get_logger()
    log.info("compose-igw")

    observed_xr=v1alpha1.Network(**req.observed.composite.resource)

    # InternetGateway
    igw=internet_gateway_v1beta1.InternetGateway(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="InternetGateway",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"]
            },
            name="igw"
        ),
        spec=internet_gateway_v1beta1.Spec(
            forProvider=internet_gateway_v1beta1.ForProvider(
                region=config["region"],
                vpcIdSelector=internet_gateway_v1beta1.VpcIdSelector(
                    matchControllerRef=True
                ),
                tags={
                    "Name": observed_xr.metadata.name,
                    "region": config["region"],
                    "last-reconcile-date": config["last_reconcile_date"]
                }
            ),
            providerConfig=internet_gateway_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["igw"], igw)
    config["is_verbose"] and log.info("igw updated")

    return rsp
