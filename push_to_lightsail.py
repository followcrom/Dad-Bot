import boto3

# Set up Lightsail client
lightsail = boto3.client("lightsail")

# Image details (replace with your image details)
docker_hub_image = "followcrom/dad_bot"
image_tag = "latest"
container_service_name = "dad-bot-cont"

# Push image to Lightsail
lightsail.push_container_image(
    service_name=container_service_name,
    label=image_tag,
    image=docker_hub_image + ":" + image_tag,
)
