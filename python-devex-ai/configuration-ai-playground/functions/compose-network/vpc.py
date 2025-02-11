""" Compose Network VPC Resources """
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from .model.org.example.platform.ai.network import v1alpha1
from .model.io.upbound.aws.ec2.vpc import v1beta1 as vpc_v1beta1


def compose_vpc(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse, config):
    """Function composing VPC managed resources."""

    log=logging.get_logger()
    log.info("compose-vpc")
    config["is_verbose"] and log.info(config)

    observed_xr=v1alpha1.Network(**req.observed.composite.resource)

    # VPC
    vpc=vpc_v1beta1.VPC(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="VPC",
        metadata=metav1.ObjectMeta(
            labels={
              "networks.aws.platform.upbound.io/id": config["network_id"]
            },
            name="vpc"
        ),
        spec=vpc_v1beta1.Spec(
            forProvider=vpc_v1beta1.ForProvider(
                cidrBlock=config["vpc_cidr_block"],
                enableDnsHostname=True,
                enableDnsSupport=True,
                region=config["region"],
                tags={
                    "Name": observed_xr.metadata.name,
                    "region": config["region"],
                    "last-reconcile-date": config["last_reconcile_date"]
                }
            ),
            providerConfig=vpc_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["vpc"], vpc)
    config["is_verbose"] and log.info("vpc updated")

    return rsp
