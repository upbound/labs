""" Compose Network - VPC """
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from .model.org.example.platform.ai.network import v1alpha1
from .model.io.upbound.aws.ec2.vpc import v1beta1 as vpc_v1beta1


def compose(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse):
    """Function composing managed resources."""

    log=logging.get_logger()
    log.info("upbound-compose-network")

    network_id=provider_config_name=region=vpc_cidr_block=''
    subnets=[]

    observed_xr=v1alpha1.Network(**req.observed.composite.resource)

    # Setting status in case this function is used in combination with an XRD that
    # does not set the id field to be required.
    if observed_xr.spec.id is not None:
        network_id=observed_xr.spec.id
        log.info("network_id:", network_id)
    else:
        resource.update(rsp.desired.composite.resource, {
            "status": {
                "warning": "Please specify spec.id. It is used as the name and identifier of the network",
            },
        })

    # providerConfig defaults to "default" if not specified
    if observed_xr.spec.providerConfigName is not None:
        provider_config_name=observed_xr.spec.providerConfigName
        log.info("provider_config_name:", provider_config_name)

    if observed_xr.spec.region is not None:
        region=observed_xr.spec.region
        log.info("region:", region)

    if observed_xr.spec.vpcCidrBlock is not None:
        vpc_cidr_block=observed_xr.spec.vpcCidrBlock
        log.info("vpc_cidr_block:", vpc_cidr_block)

    if observed_xr.spec.subnets is not None:
        subnets=observed_xr.spec.subnets
        log.info("subnets:", subnets)

    # VPC
    vpc=vpc_v1beta1.VPC(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="VPC",
        metadata=metav1.ObjectMeta(
            labels={
              "networks.aws.platform.upbound.io/id": network_id
            },
            name="vpc"
        ),
        spec=vpc_v1beta1.Spec(
            forProvider=vpc_v1beta1.ForProvider(
                cidrBlock=vpc_cidr_block,
                enableDnsHostname=True,
                enableDnsSupport=True,
                region=region,
                tags={
                    "Name": observed_xr.metadata.name,
                    "region": region
                }
            ),
            providerConfig=vpc_v1beta1.ProviderConfigRef(
                name=provider_config_name
            )
        )
    )
    resource.update(rsp.desired.resources["vpc"], vpc)
    log.info("vpc updated")

    return rsp
