# DadBot

<div align="center">
  <img src="static/dad-dare_256x256.jpg" alt="DadBot Image">
</div>


## Local Testing

Uncomment the line to 'Run locally on any port above 1024'.

### In terminal

Start venv

`source dad_venv/bin/activate`

SSH into the server

ssh -i ~/.ssh/dad-bot-key.pem ubuntu@ec2-public-IP-address.eu-west-2.compute.amazonaws.com

### In Docker

Open Docker Desktop and wait for it to initialize and show a status of 'Running'. This allows Docker commands to be recognized in the Linux terminal.

Navigate to the DadBot app's directory.

Step 1: **Build Docker Image**

Ensure you have a `Dockerfile` in the root of your app project. Then, run the following command in your terminal to build the image:

   ```sh
   docker build -t dad_bot:dev .
   ```

Here, dad_bot:dev is the name and tag for your Docker image, and the . specifies the current directory where your Dockerfile is located.

Step 2: **Run Your Docker Container**

After building the image, you can run it as a container. Use the following command to start your Flask app inside a Docker container:

```
docker run -p 5000:5000 --env-file ./.env dad_bot:dev
```

This command tells Docker to run the container and map port 5000 of the container to port 5000 on your host machine. This way, you can access your Flask app by visiting http://localhost:5000 in your web browser.

Step 3: **List Running Containers**

Open your terminal and run the following command to list all currently running Docker containers:

```
docker ps -a
```
This command will show you a table of all active containers, including their CONTAINER ID, IMAGE, COMMAND, CREATED, STATUS, PORTS, and NAMES.

Step 4: **Stop the Container**

Once you've identified the CONTAINER ID or NAME of your app container from the list, you can stop it using:

```
docker stop [CONTAINER_ID_OR_NAME]
```

This command will send a stop signal to your Docker container, allowing it to gracefully shut down.

Step 4: **Removing Stopped Containers**

After stopping your Docker container, it will still be in the system in a stopped state. If you wish to remove it completely:

```
docker rm [CONTAINER_ID_OR_NAME]
```

This step is optional and can be useful for cleanup, especially during development, to keep your environment tidy.

## Building for Production

Step 1: **Build Your Docker Image**

```
docker build -t dad_bot:latest .
```

Step 2: **Tag Your Docker Image for Registry**

Before pushing your Docker image to Docker Hub, tag it with the registry's URL:

```
docker tag dad_bot:latest followcrom/dad_bot:latest
```

Step 3: **Push Your Docker Image to the Registry**

```
docker push followcrom/dadbot:latest
```


## Deploy Your Docker Image

[AWS Docs: push container images from your local machine to your Lightsail container service](https://docs.aws.amazon.com/en_us/lightsail/latest/userguide/amazon-lightsail-pushing-container-images.html)

Enter the following command to push the container image on your local machine to your container service:

`aws lightsail push-container-image --region eu-west-2 --service-name dad-bot --label dad-bot --image followcrom/dad_bot:latest`

`aws lightsail push-container-image --region <Region> --service-name <ContainerServiceName> --label <ContainerImageLabel> --image <LocalContainerImageName>:<ImageTag>`

Create a new deployment for your container service using the following command:

```
aws lightsail create-container-service-deployment --service-name dad-bot --containers '{"dad-bot-cont": {"image": ":dad-bot.dad-bot.3", "environment": {"ELEVENLABS_API_KEY": "${{ secrets.ELEVENLABS_API_KEY }}", "OPENAI_API_KEY": "${{ secrets.OPENAI_API_KEY }}", "SECRET_KEY": "${{ secrets.SECRET_KEY }}"}, "ports": {"80": "HTTP"}}}' --public-endpoint '{"containerName": "dad-bot-cont", "containerPort": 80, "healthCheck": {"path": "/"}}'
```

Here's how you can use this command to check the status of your container service:

`aws lightsail get-container-services --service-name dad-bot`

Filtering the Output
If you're looking for specific information and want to filter the output, you can use the --query option with the AWS CLI command. For example, to get just the state of the container service, you can run:

`aws lightsail get-container-services --service-name dad-bot --query 'containerServices[0].state'`

Watching the Status
If you're waiting for a deployment to complete or for the service state to change, you might find it useful to repeatedly check the status. You can do this in a bash loop or use the watch command in Linux/Unix environments:

bash
Copy code
watch -n 10 'aws lightsail get-container-services --service-name dad-bot --query "containerServices[0].state"'
This command uses watch to rerun the AWS CLI command every 10 seconds, showing you the latest state each time.





### Docker cmds

`docker images`

`docker rmi xxx`

`docker stop xxx`

`docker rm xxx`


### Get voices

- Go to https://elevenlabs.io/docs/api-reference/get-voices

- Enter API key as the Header and click Send

- The returned body contain the voices


### Big Al voice

<details>
  <summary>Click to expand!</summary>

 {
      "voice_id": "NsManPzvLKKRvmmOUBOo",
      "name": "BigAl",
      "samples": [
        {
          "sample_id": "MqrVIspxOUECXVFqYWxM",
          "file_name": "Dad-voice_IVC-clip4.mp3",
          "mime_type": "audio/mpeg",
          "size_bytes": 1590044,
          "hash": "cf7e764205b0efd368198c1594f5e422"
        },
        {
          "sample_id": "Rtv01mQDsSrhKfsIOBrz",
          "file_name": "Dad-voice_IVC-clip.mp3",
          "mime_type": "audio/mpeg",
          "size_bytes": 6185732,
          "hash": "186cceb2ba60adb0ced152bd30b59ed1"
        },
        {
          "sample_id": "ecbNj3FiaWCkwCAV8f1C",
          "file_name": "Dad-voice_IVC-clip2.mp3",
          "mime_type": "audio/mpeg",
          "size_bytes": 2128748,
          "hash": "d128a4581860e8af3072ca5f08b8afc5"
        },
        {
          "sample_id": "g5mtd6KXs17gcOFbLBND",
          "file_name": "Dad-voice_IVC-clip3.mp3",
          "mime_type": "audio/mpeg",
          "size_bytes": 1200632,
          "hash": "600ce9e7aa6239aa3a0936cdc487e12d"
        }
      ],
      "category": "cloned",
      "fine_tuning": {
        "is_allowed_to_fine_tune": false,
        "finetuning_state": "not_started",
        "verification_failures": [],
        "verification_attempts_count": 0,
        "manual_verification_requested": false,
        "language": null,
        "finetuning_progress": {},
        "message": null,
        "dataset_duration_seconds": null,
        "verification_attempts": null,
        "slice_ids": null,
        "manual_verification": null
      },
      "labels": {
        "accent": "British"
      },
      "description": "An older male British voice, cheerful and avuncular.",
      "preview_url": "https://storage.googleapis.com/eleven-public-prod/RHNfC3IAUsbDNnLzSzNz3skaMJk1/voices/NsManPzvLKKRvmmOUBOo/da9c1606-20e5-4706-bf3b-4e7ccf3409a0.mp3",
      "available_for_tiers": [],
      "settings": null,
      "sharing": null,
      "high_quality_base_model_ids": [],
      "safety_control": null,
      "voice_verification": {
        "requires_verification": false,
        "is_verified": false,
        "verification_failures": [],
        "verification_attempts_count": 0,
        "language": null,
        "verification_attempts": null
      }
    },

</details>

 ### Other voices:
"voice_id": "z9ULidXEujRLhPKDEh8q",
    "name": "Prajnatara",