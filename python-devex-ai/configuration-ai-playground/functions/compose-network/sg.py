""" Compose Security Group Related Resources """
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from .model.org.example.platform.ai.network import v1alpha1
from .model.io.upbound.aws.ec2.securitygroup import v1beta1 as security_group_v1beta1
from .model.io.upbound.aws.ec2.securitygrouprule import v1beta1 as security_group_rule_v1beta1


def compose_sg(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse, config):
    """Function composing security group related managed resources."""

    log=logging.get_logger()
    log.info("compose-sg")

    observed_xr=v1alpha1.Network(**req.observed.composite.resource)

    # Security Group
    sg=security_group_v1beta1.SecurityGroup(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="SecurityGroup",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"],
                "networks.aws.platform.upbound.io/type": "ssh"
            },
            name="sg"
        ),
        spec=security_group_v1beta1.Spec(
            forProvider=security_group_v1beta1.ForProvider(
                description="Allow SSH access to EC2 Instance",
                name="cloud-ai-box",
                region=config["region"],
                vpcIdSelector=security_group_v1beta1.VpcIdSelector(
                    matchControllerRef=True
                ),
                tags={
                    "Name": observed_xr.metadata.name,
                    "region": config["region"],
                    "last-reconcile-date": config["last_reconcile_date"]
                }
            ),
            providerConfigRef=security_group_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["sg"], sg)
    config["is_verbose"] and log.info("sg updated")

    # Security Group Rules
    sgrp_outbound_icmp=security_group_rule_v1beta1.SecurityGroupRule(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="SecurityGroupRule",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"],
                "networks.aws.platform.upbound.io/type": "icmp"
            },
            name="sgrp-outbound-icmp"
        ),
        spec=security_group_rule_v1beta1.Spec(
            forProvider=security_group_rule_v1beta1.ForProvider(
                cidrBlocks=["0.0.0.0/0"],
                description="icmp outbound",
                fromPort=-1,
                protocol="icmp",
                securityGroupIdSelector=security_group_rule_v1beta1.SecurityGroupIdSelector(
                    matchControllerRef=True
                ),
                toPort=-1,
                type="egress",
                region=config["region"]
            ),
            providerConfigRef=security_group_rule_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["sgrp-outbound-icmp"], sgrp_outbound_icmp)
    config["is_verbose"] and log.info("sgrp_outbound_icmp updated")

    sgrp_outbound_udp=security_group_rule_v1beta1.SecurityGroupRule(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="SecurityGroupRule",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"],
                "networks.aws.platform.upbound.io/type": "udp"
            },
            name="sgrp-outbound-udp"
        ),
        spec=security_group_rule_v1beta1.Spec(
            forProvider=security_group_rule_v1beta1.ForProvider(
                cidrBlocks=["0.0.0.0/0"],
                description="udp outbound",
                fromPort=0,
                protocol="udp",
                securityGroupIdSelector=security_group_rule_v1beta1.SecurityGroupIdSelector(
                    matchControllerRef=True
                ),
                toPort=65535,
                type="egress",
                region=config["region"]
            ),
            providerConfigRef=security_group_rule_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["sgrp-outbound-udp"], sgrp_outbound_udp)
    config["is_verbose"] and log.info("sgrp_outbound_udp updated")

    sgrp_outbound_tcp=security_group_rule_v1beta1.SecurityGroupRule(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="SecurityGroupRule",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"],
                "networks.aws.platform.upbound.io/type": "tcp"
            },
            name="sgrp-outbound-tcp"
        ),
        spec=security_group_rule_v1beta1.Spec(
            forProvider=security_group_rule_v1beta1.ForProvider(
                cidrBlocks=["0.0.0.0/0"],
                description="tcp outbound",
                fromPort=0,
                protocol="tcp",
                securityGroupIdSelector=security_group_rule_v1beta1.SecurityGroupIdSelector(
                    matchControllerRef=True
                ),
                toPort=65535,
                type="egress",
                region=config["region"]
            ),
            providerConfigRef=security_group_rule_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["sgrp-outbound-tcp"], sgrp_outbound_tcp)
    config["is_verbose"] and log.info("sgrp_outbound_tcp updated")

    sgrp_inbound_ssh=security_group_rule_v1beta1.SecurityGroupRule(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="SecurityGroupRule",
        metadata=metav1.ObjectMeta(
            labels={
                "networks.aws.platform.upbound.io/id": config["network_id"],
                "networks.aws.platform.upbound.io/type": "ssh"
            },
            name="sgrp-inbound-ssh"
        ),
        spec=security_group_rule_v1beta1.Spec(
            forProvider=security_group_rule_v1beta1.ForProvider(
                cidrBlocks=["0.0.0.0/0"],
                description="ssh inbound",
                fromPort=22,
                protocol="tcp",
                securityGroupIdSelector=security_group_rule_v1beta1.SecurityGroupIdSelector(
                    matchControllerRef=True
                ),
                toPort=22,
                type="ingress",
                region=config["region"]
            ),
            providerConfigRef=security_group_rule_v1beta1.ProviderConfigRef(
                name=config["provider_config_name"]
            )
        )
    )
    resource.update(rsp.desired.resources["sgrp-inbound-ssh"], sgrp_inbound_ssh)
    config["is_verbose"] and log.info("sgrp_inbound_ssh updated")

    return rsp
