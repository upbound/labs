""" Compose Network """
import ipaddress
import json
from datetime import datetime
from crossplane.function import logging, resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

# Add models as import
# Crossplane in cluster imports require leading dot

from .model.org.example.platform.ai.network import v1alpha1
from .igw import compose_igw
from .rt import compose_rt
from .sg import compose_sg
from .subnets import compose_subnets
from .vpc import compose_vpc

def get_config_info():
    try:
        with open('/venv/fn/lib/python3.11/site-packages/function/config.json', 'r') as file:
            data=json.load(file)
            if data["mode"] == "verbose":
                return True
            return False
    except FileNotFoundError:
        return False

def is_valid_cidr(cidr):
    ''' Validate CIDR block format '''

    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

def compose(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse):
    """Function composing managed resources."""

    log=logging.get_logger()
    log.info("compose-network")

    subnets=[]
    config={
        "provider_config_name": "",
        "network_id": "",
        "region": "",
        "vpc_cidr_block": "",
        "last_reconcile_date": datetime.now().strftime("%A %Y-%m-%d %H:%M:%S UTC"),
        "is_verbose": get_config_info()
    }


    # This will raise an exception for schema validations
    observed_xr=v1alpha1.Network(**req.observed.composite.resource)

    # Composite resource status for xnetwork
    # See apis/xnetworks/definition.yaml
    status_xr={
        "status": {
            "xnetwork": {
                "vpcCidrBlock": "",
                "subnets": {}
            }
        }
    }

    # Include the network id in config
    if observed_xr.spec.id is not None:
        config["network_id"]=observed_xr.spec.id
        config["is_verbose"] and log.info("network_id:" + config["network_id"])

    # providerConfig defaults to "default" if not specified
    if observed_xr.spec.providerConfigName is not None:
        config["provider_config_name"]=observed_xr.spec.providerConfigName
        config["is_verbose"] and log.info("provider_config_name:" + config["provider_config_name"])

    # Note that the region is an enum with those regions that offer a
    # Hugging Face Neuron Deep Learning AMI (Ubuntu 22.04)
    # for launch of Upboxes that depend on it. It defaults to us-east-1.
    if observed_xr.spec.region is not None:
        config["region"]=str(observed_xr.spec.region).split(".")[1].replace("_", "-")
        config["is_verbose"] and log.info("region:" + config["region"])

    # The vpcCidrBlock a required parameter.
    # A potentially invalid format is indicated in the xnetwork status.
    if observed_xr.spec.vpcCidrBlock is not None:
        config["vpc_cidr_block"]=observed_xr.spec.vpcCidrBlock
        config["is_verbose"] and log.info("vpc_cidr_block:" + config["vpc_cidr_block"])
        if is_valid_cidr(config["vpc_cidr_block"]):
            status_xr["status"]["xnetwork"]["vpcCidrBlock"]=config["vpc_cidr_block"]
        else:
            status_xr["status"]["xnetwork"]["vpcCidrBlock"]=\
                config["vpc_cidr_block"] + " format is invalid"

    # Potentially invalid subnet parameters are flagged
    # for all subnets in parallel.
    status_subnets=[]
    if observed_xr.spec.subnets is not None:
        subnets=observed_xr.spec.subnets
        config["is_verbose"] and log.info("subnets:")
        config["is_verbose"] and log.info(subnets)
        for subnet in subnets:
            status_subnet_cidr_block=subnet.cidrBlock
            status_subnet_type=subnet.type
            status_subnet_availability_zone=subnet.availabilityZone
            if not is_valid_cidr(subnet.cidrBlock):
                status_subnet_cidr_block+=" format is invalid"
            if subnet.type not in ["public", "private"]:
                status_subnet_type+=" should be public or private"
            if not subnet.availabilityZone.startswith(config["region"]):
                status_subnet_availability_zone+=\
                    " should be in region " + config["region"]
            status_subnets.append({
                "availabilityZone": status_subnet_availability_zone,
                "cidrBlock": status_subnet_cidr_block,
                "type": status_subnet_type
            })
        config["is_verbose"] and log.info(status_subnets)

    status_xr["status"]["xnetwork"]["subnets"] = status_subnets
    config["is_verbose"] and log.info(status_xr)

    # Update the xnetwork status
    # Merge the status from previous composition pipeline steps
    # because resouce.update performs a replace versus a merge.
    if "composite" in req.desired:
        if "resource" in req.desired.composite:
            if "status" in req.desired.composite.resource:
                status_xr|=req.desired.composite.resource["status"]
    resource.update(rsp.desired.composite, status_xr)

    # Compose managed resources for the composite xnetwork resource
    compose_vpc(req, rsp, config)
    compose_igw(req, rsp, config)
    compose_subnets(req, rsp, config, subnets)
    compose_rt(req, rsp, config, subnets)
    compose_sg(req, rsp, config)

    return rsp
