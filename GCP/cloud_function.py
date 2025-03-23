from google.cloud import compute_v1

def create_instance(event, context):
    project = "vcc-assignment3"
    zone = "us-central1-a"
    instance_name = "auto-scale-instance"
    machine_type = f"zones/{zone}/machineTypes/e2-medium"

    instance_client = compute_v1.InstancesClient()
    action = event["data"].decode()

    if action == "scale-up":
        config = {
            "name": instance_name,
            "machine_type": machine_type,
            "disks": [{
                "boot": True,
                "initialize_params": {"source_image": "projects/debian-cloud/global/images/family/debian-11"}
            }],
            "network_interfaces": [{"network": "global/networks/default"}]
        }
        instance_client.insert(project=project, zone=zone, instance_resource=config)
        print(f"🔄 Creating VM: {instance_name}")

    elif action == "scale-down":
        instance_client.delete(project=project, zone=zone, instance=instance_name)
        print(f"🔄 Deleting VM: {instance_name}")
