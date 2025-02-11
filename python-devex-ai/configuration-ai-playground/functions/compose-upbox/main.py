"""Python Function Composing An AI Upbox."""
from datetime import datetime
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from .model.org.example.platform.ai.upbox import v1alpha1
from .model.io.upbound.aws.ec2.instance import v1beta1 as v1beta1instance
from .model.io.upbound.aws.ec2.keypair import v1beta1 as v1beta1keypair

# The command to connect to the composed instance is as follows:
# ssh ubuntu@$(k get instance <instance-name> -o jsonpath='{.status.atProvider.publicIp}')
def compose(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse):
    """Function composing managed resources."""

    log=logging.get_logger()
    company=name=network_id=owner=public_ssh_key=zone=''
    upbox_id="huggingface-deep-learning-neuron-"

    # Hugging Face Neuron Deep Learning AMI (Ubuntu 22.04)
    ami={
        "ap-southeast-1": "ami-0656d29e38200e4e8",  # Singapore
        "eu-central-1": "ami-0f3bcda2f4c27aafd",    # Frankfurt
        "eu-north-1": "ami-0a0856970d266884f",      # Stockholm
        "eu-west-1": "ami-0a8d59de8ed70e61c",       # Virginia
        "sa-east-1": "ami-01f5354d8e6c78c21",       # Sao Paulo
        "us-east-1": "ami-0f9a795e2d1186fe3",       # Oregon
        "us-west-2": "ami-0bede50341b2516c4",       # Ireland
    }

    # Casting the request to v1alpha1.Box performs an implicit schema validation
    observed_xr=v1alpha1.Upbox(**req.observed.composite.resource)
    log.info("observed_xr")
    log.info(observed_xr)

    # observed_xr.spec.region is an enum
    if observed_xr.spec.region is not None:
        region=str(observed_xr.spec.region).split(".")[1].replace("_", "-")

    if observed_xr.spec.zone is not None:
        zone=str(observed_xr.spec.zone).split(".")[1]

    # observed_xr.spec.size is an enum
    if observed_xr.spec.size is not None:
        size=str(observed_xr.spec.size).split(".")[1]

    if observed_xr.spec.company is not None:
        company=observed_xr.spec.company
        upbox_id=upbox_id+company + "-"

    if observed_xr.spec.name is not None:
        name=observed_xr.spec.name
        upbox_id=upbox_id + name

    if observed_xr.spec.networkId is not None:
        network_id=observed_xr.spec.networkId

    if observed_xr.spec.publicSshKey is not None:
        public_ssh_key=observed_xr.spec.publicSshKey
    else:
        raise Exception("spec.publicSshKey is a required parameter.")

    key_name="key-" + name

    instance_type="inf2.xlarge"
    if size is not None:
        match size:
            case "small":
                instance_type="inf2.xlarge"
            case "medium":
                instance_type="trn1.2xlarge"
            case "large":
                instance_type="inf2.8xlarge"
            case "xlarge":
                instance_type="inf2.24xlarge"
            case "premium":
                instance_type="inf2.48xlarge"
            case _:
                instance_type="inf2.xlarge"
    else:
        size="small"

    log.info("size: " + size)
    log.info("instance_type: " + instance_type)
    log.info("region: " + region)
    try:
        log.info("ami: " + ami[region])
    except:
        log.error("ami: internal server error")
        return rsp

    desired_subnet_id_selector_labels={
        "networks.aws.platform.upbound.io/id": network_id,
        "access": "public",
        "zone": region + zone
    }

    desired_vpc_security_group_id_selector_labels={
        "networks.aws.platform.upbound.io/id": network_id,
        "networks.aws.platform.upbound.io/type": "ssh"
    }

    keypair=v1beta1keypair.KeyPair(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="KeyPair",
        metadata=metav1.ObjectMeta(
            labels={
                "instances.aws.platform.upbound.io/id": key_name
            },
            name=key_name
        ),
        spec=v1beta1keypair.Spec(
            forProvider=v1beta1keypair.ForProvider(
                publicKey=public_ssh_key,
                region=region,
                tags={
                    "Name": observed_xr.metadata.name,
                    "last-reconcile-date":\
                        datetime.now().strftime("%A %Y-%m-%d %H:%M:%S UTC")
                }
            ),
            providerConfigRef=v1beta1keypair.ProviderConfigRef(
                name="default"
            )
        )
    )
    resource.update(rsp.desired.resources["keypair"], keypair)

    instance=v1beta1instance.Instance(
        apiVersion="ec2.aws.upbound.io/v1beta1",
        kind="Instance",
        metadata=metav1.ObjectMeta(
            annotations={
                "name": upbox_id
            },
            labels={
                "upbox.aws.platform.upbound.io/id": upbox_id,
                "upbox.aws.platform.upbound.io/owner": owner
            },
            name=upbox_id
        ),
        spec=v1beta1instance.Spec(
            forProvider=v1beta1instance.ForProvider(
                region=region,
                instanceType=instance_type,
                associatePublicIpAddress=True,
                ami=ami[region],
                keyName=key_name,
                subnetIdSelector=v1beta1instance.SubnetIdSelector(
                    matchLabels=desired_subnet_id_selector_labels
                ),
                vpcSecurityGroupIdSelector=v1beta1instance.VpcSecurityGroupIdSelector(
                    matchLabels=desired_vpc_security_group_id_selector_labels
                ),
                tags={
                    "Name": observed_xr.metadata.name,
                    "last-reconcile-date":\
                        datetime.now().strftime("%A %Y-%m-%d %H:%M:%S UTC")
                }
            ),
            providerConfigRef=v1beta1instance.ProviderConfigRef(
                name="default"
            )
        )
    )
    resource.update(rsp.desired.resources["instance"], instance)

    log.info("compose-upbox, upbox_id: " + upbox_id + ", key_name: " + key_name)

    return rsp
