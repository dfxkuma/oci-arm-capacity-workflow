import oci
import json
import logging
import asyncio
from datetime import datetime

from loghook.discord import DiscordHook

log_hook = DiscordHook()

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
    memory_in_gbs: float,
    ocpus: float,
    ssh_authorized_public_key: str,
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
            "ssh_authorized_keys": ssh_authorized_public_key,
        },
        shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
            memory_in_gbs=memory_in_gbs,
            ocpus=ocpus,
        ),
        create_vnic_details=vnic_details,
    )

    instance_response = compute.launch_instance(create_instance_details)
    return instance_response


async def workflow():
    if await exist_instance_shape("VM.Standard.A1.Flex"):
        logging.warning("VM.Standard.A1.Flex 인스턴스가 이미 존재합니다.")
        logging.warning("이제 이 프로세스를 종료해도 됩니다.")
        datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await log_hook.send(f"{datetime_string} | VM.Standard.A1.Flex 인스턴스가 이미 존재합니다.")
    else:
        with open("./ssh_keys/ssh-key-2024-01-16.key.pub", "r") as public_key_file:
            public_key = public_key_file.read()
        try:
            response = await create_compute_instance(
                compartment_id=local_config["compartment_id"],
                availability_domain=local_config["availability_domain"],
                display_name=local_config["instance_display_name"],
                shape="VM.Standard.A1.Flex",
                subnet_id=local_config["subnet_id"],
                image_id=local_config["image_id"],
                memory_in_gbs=float(local_config["instance_memory_in_gbs"]),
                ocpus=float(local_config["instance_ocpus"]),
                ssh_authorized_public_key=public_key,
            )
            logging.warning(
                "%s 에 %s 인스턴스를 생성했습니다. (ID: %s)",
                response.data.availability_domain,
                response.data.display_name,
                response.data.id,
            )
            datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await log_hook.send(
                f"{datetime_string} | {response.data.availability_domain} 에 "
                f"{response.data.display_name} 인스턴스를 생성했습니다. (ID: {response.data.id})"
            )
        except oci.exceptions.ServiceError as err_data:
            if err_data.status == 500 and "Out of host capacity" in err_data.message:
                logging.warning(
                    "%s 인스턴스를 생성하지 못했습니다.", local_config["instance_display_name"]
                )
                logging.warning(
                    "InternalError(500): VM.Standard.A1.Flex 구성에 대한 용량이 부족합니다."
                )
                datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await log_hook.send(
                    f"{datetime_string} | {local_config['instance_display_name']} 인스턴스를 생성하지 못했습니다."
                )
            else:
                logging.warning("예기치 못한 오류가 발생했습니다.")
                logging.error(err_data)
                datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await log_hook.send(f"{datetime_string} | 예기치 못한 오류가 발생했습니다.")
                await log_hook.send(f"```\n{str(err_data)[:1500]}```")


asyncio.run(workflow())
