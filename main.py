import oci
import json
import paramiko

with open("config.json", "r", encoding="utf-8") as f:
    local_config = json.load(f)


oci_config = oci.config.from_file("./.oci/.config", "DEFAULT")

identity = oci.identity.IdentityClient(oci_config)
compute = oci.core.ComputeClient(oci_config)
virtual_network = oci.core.VirtualNetworkClient(oci_config)


async def exist_instance_shape(shape: str, /):
    instances = compute.list_instances(oci_config["tenancy"]).data
    for instance in instances:
        if instance.shape == shape:
            return True
    return False


async def create_compute_instance(
    compartment_id: str,
    availability_domain: str,
    display_name: str,
    shape: str,
    subnet_id: str,
    image_id: str,
    memory_in_gbs: int,
    ocpus: int,
    ssh_authorized_public_key: paramiko.RSAKey,
):
    vnic_details = oci.core.models.CreateVnicDetails(
        assign_ipv6_ip=False,
        assign_public_ip=True,
        subnet_id=subnet_id,
        assign_private_dns_record=True,
    )
    create_instance_details = oci.core.models.LaunchInstanceDetails(
        compartment_id=compartment_id,
        availability_domain=availability_domain,
        display_name=display_name,
        shape=shape,
        subnet_id=subnet_id,
        image_id=image_id,
        metadata={
            "ssh_authorized_keys": ssh_authorized_public_key.get_name()
            + " "
            + ssh_authorized_public_key.get_base64(),
        },
        shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
            memory_in_gbs=memory_in_gbs,
            ocpus=ocpus,
        ),
        create_vnic_details=vnic_details,
    )

    instance_response = compute.launch_instance(create_instance_details)
    return instance_response


async def main():
    if await exist_instance_shape("VM.Standard.A1.Flex"):
        print("이미 VM.Standard.A1.Flex 구성 인스턴스가 존재합니다.")
        print("이제 이 프로세스를 종료해도 됩니다.")
