import boto3

# Set up Lightsail client
lightsail = boto3.client("lightsail", region_name="your-region")


deployment = {
    'containers': {
        'your-container-name': {
            'image': "followcrom/dad_bot",  # This could be a Docker Hub public image or an Amazon ECR image
            'ports': {
                '80': 'HTTP'
            },
            # Include other configuration as necessary
        }
    },
    'publicEndpoint': {
        'containerName': 'your-container-name',
        'containerPort': 80,
        'healthCheck': {
            'path': '/',
            # Other health check configurations
        }
    }
}

response = lightsail.create_container_service_deployment(
    serviceName="dad-bot-cont",
    containers=deployment['containers'],
    publicEndpoint=deployment['publicEndpoint']
)