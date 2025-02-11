""" Compose Route Related Network Resources """
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from .model.org.example.platform.ai.network import v1alpha1
from .model.io.upbound.aws.ec2.routetable import v1beta1 as route_table_v1beta1
from .model.io.upbound.aws.ec2.route import v1beta2 as route_v1beta2
from .model.io.upbound.aws.ec2.mainroutetableassociation import (
    v1beta1 as main_route_table_association_v1beta1
)
from .model.io.upbound.aws.ec2.routetableassociation import (
    v1beta1 as route_table_association_v1beta1
)


def compose_rt(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse, config, subnets):
    """Function composing managed resources."""

    log=logging.get_logger()
    log.info("compose-rt")

    observed_xr=v1alpha1.Network(**req.observed.composite.resource)

    # Route Table
    rt=route_table_v1beta1.RouteTable(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="RouteTable",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"]
            },
            name="rt"
        ),
        spec=route_table_v1beta1.Spec(
            forProvider=route_table_v1beta1.ForProvider(
                region=config["region"],
                vpcIdSelector=route_table_v1beta1.VpcIdSelector(
                    matchControllerRef=True
                ),
                tags={
                    "Name": observed_xr.metadata.name,
                    "region": config["region"],
                    "last-reconcile-date": config["last_reconcile_date"]
                }
            ),
            providerConfigRef=route_table_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["rt"], rt)
    config["is_verbose"] and log.info("rt updated")

    # Route
    route=route_v1beta2.Route(
        apiVersion="ec2.aws.upbound.io/v1beta2",
        kind="Route",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"]
            },
            name="route"
        ),
        spec=route_v1beta2.Spec(
            forProvider=route_v1beta2.ForProvider(
                destinationCidrBlock="0.0.0.0/0",
                gatewayIdSelector=route_v1beta2.GatewayIdSelector(
                    matchControllerRef=True
                ),
                routeTableIdSelector=route_v1beta2.RouteTableIdSelector(
                    matchControllerRef=True
                ),
                region=config["region"]
            ),
            providerConfigRef=route_v1beta2.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["route"], route)
    config["is_verbose"] and log.info("route updated")

    # Main Route Table Association
    mrta=main_route_table_association_v1beta1.MainRouteTableAssociation(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="MainRouteTableAssociation",
        metadata =metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"]
            },
            name="mrta"
        ),
        spec=main_route_table_association_v1beta1.Spec(
            forProvider=main_route_table_association_v1beta1.ForProvider(
                region=config["region"],
                routeTableIdSelector=main_route_table_association_v1beta1.RouteTableIdSelector(
                    matchControllerRef=True
                ),
                vpcIdSelector=main_route_table_association_v1beta1.VpcIdSelector(
                    matchControllerRef=True
                )
            ),
            providerConfigRef=main_route_table_association_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["mrta"], mrta)
    config["is_verbose"] and log.info("mrta updated")

    # Route Table Associations
    for subnet in subnets:
        access="public"
        if subnet.type == "private":
            access="private"

        rta=route_table_association_v1beta1.RouteTableAssociation(
            apiVersion="ec2.aws.upbound.io/v1beta1",
            kind="RouteTableAssociation",
            metadata=metav1.ObjectMeta(
                labels={
                    "networks.aws.platform.upbound.io/id": config["network_id"]
                },
                name="rta-" + subnet.availabilityZone + '-' + subnet.type
            ),
            spec=route_table_association_v1beta1.Spec(
                forProvider=route_table_association_v1beta1.ForProvider(
                    region=config["region"],
                    routeTableIdSelector=route_table_association_v1beta1.RouteTableIdSelector(
                        matchControllerRef=True
                    ),
                    subnetIdSelector=route_table_association_v1beta1.SubnetIdSelector(
                        matchControllerRef=True,
                        matchLabels={
                            "access": access,
                            "zone": subnet.availabilityZone
                        }
                    )
                ),
                providerConfigRef=route_table_association_v1beta1.ProviderConfigRef(
                    name=config["provider_config_name"]
                )
            )
        )
        resource.update(rsp.desired.resources[rta.metadata.name], rta)
        config["is_verbose"] and log.info(rta.metadata.name + " updated")

    return rsp
