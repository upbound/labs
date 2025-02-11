""" Compose Network Subnet Resources """
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from .model.org.example.platform.ai.network import v1alpha1
from .model.io.upbound.aws.ec2.subnet import v1beta1 as subnet_v1beta1


def compose_subnets(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse, config, subnets):
    """Function composing Subnet managed resources."""

    log=logging.get_logger()
    log.info("compose-subnets")

    observed_xr=v1alpha1.Network(**req.observed.composite.resource)

    # Subnets
    for subnet in subnets:
        config["is_verbose"] and log.info(subnet)
        tags={
            "Name": observed_xr.metadata.name,
            "region": config["region"],
            "last-reconcile-date": config["last_reconcile_date"]
        }
        if subnet.type == "private":
            access="private"
            tags["kubernetes.io/role/internal-elb"]="1"
        else:
            access=subnet.type
            tags["kubernetes.io/role/elb"]="1"
        map_public_ip_on_launch=False
        if subnet.type == "public":
            map_public_ip_on_launch=True
            tags["networks.aws.platform.upbound.io/id"]=config["network_id"]

        sn=subnet_v1beta1.Subnet(
            apiVersion="ec2.aws.upbound.io/v1beta1",
            kind="Subnet",
            metadata=metav1.ObjectMeta(
                labels={
                    "zone": subnet.availabilityZone,
                    "access": access,
                    "networks.aws.platform.upbound.io/id": config["network_id"]
                },
                name="subnet-" + subnet.availabilityZone + '-' + subnet.type
            ),
            spec=subnet_v1beta1.Spec(
                forProvider=subnet_v1beta1.ForProvider(
                    access=access,
                    availabilityZone=subnet.availabilityZone,
                    cidrBlock=subnet.cidrBlock,
                    mapPublicIpOnLaunch=map_public_ip_on_launch,
                    region=config["region"],
                    tags=tags,
                    vpcIdSelector=subnet_v1beta1.VpcIdSelector(
                        matchControllerRef=True
                    )
                ),
                providerConfigRef=subnet_v1beta1.ProviderConfigRef(
                    name=config["provider_config_name"]
                )
            )
        )
        resource.update(rsp.desired.resources[sn.metadata.name], sn)
        config["is_verbose"] and log.info(sn.metadata.name + " updated")

    return rsp
