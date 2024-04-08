# DadBot

<div align="center">
  <img src="db_app/static/dad-dare_256x256.jpg" alt="DadBot Image">
</div>


# Local Testing

Configure `if __name__ == "__main__":` block in app.py to run the app locally.

### In terminal

Start venv

`source dad_venv/bin/activate`

Stop venv

`deactivate`

# AWS

AWS dynamically assign public IP addresses. This means that if you stop and start an EC2 instance, it will have a different public IP address. This will require you to update your DNS records: Update the A record for the subdomain **dadbot.followcrom.online** to point to the new IP address.

## SSH into the server

**Note:** The IP address will change each time the server is stopped and started.

```bash
ssh -i ~/.ssh/dad-bot-key.pem ubuntu@ec2-xx-xx-xx-xx.eu-west-2.compute.amazonaws.com
```

## Environment Variables

**Note:** When using a Systemd Service, you need to set environment variables in the service file. If you've saved your environment variables in ~/.bashrc, they'll be available in interactive bash shells. However, when systemd starts services like your Gunicorn service, it doesn't read variables from shell-specific files like ~/.bashrc.

### Temporary or session-specific variables

`export VAR_NAME="value"`

### Persistent Environment Variables:
For environment variables that persist across sessions and reboots, you can add them to the ~/.profile, ~/.bashrc, or /etc/environment file, depending on your specific needs.

- Use ~/.bashrc or ~/.profile for user-specific configurations, which is often preferred for a single user or application-specific settings.

```bash
nano ~/.bashrc
```

Add the export line at the end of the file:

```bash
export ELEVENLABS_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Save and close the file. For changes to take effect, either log out and log back in, or source the file:

```bash
source ~/.bashrc
```

- Use /etc/environment for system-wide environment variables that should affect all users and services. Be cautious with this file, as changes affect the entire system. 
```bash
sudo nano /etc/environment
```

Add the variable in the NAME="value" format (without the export keyword):

`VAR_NAME="value"`

Save and close the file. The changes will take effect at the next login or reboot.

## Run in EC2 on Flask dev server

`flask run --host=0.0.0.0 --port=5000`

Ensure the security group allows inbound traffic on port 5000

Then vist the public IP address of the EC2 instance on port 5000:

http://Your-EC2-Instance-Public-IP:5000


## Run on EC2 with Gunicorn

### Install Gunicorn

`pip install gunicorn`

### Run Gunicorn

Be sure to open port 8000 in the security group. Start Gunicorn with your Flask application:

`gunicorn --bind 0.0.0.0:8000 app:app`

(Replace app:app if they are different.)

With Gunicorn running, your Flask app should be accessible from your browser using your EC2 instance's public IP or domain name followed by :8000.

http://Your-EC2-Instance-Public-IP:8000

### Run on EC2 with Nginx

### Install Nginx

```bash
sudo apt-get update
sudo apt-get install nginx -y
```

## Configure Nginx
Create a new configuration file in /etc/nginx/sites-available/

```bash
cd /etc/nginx/sites-available
sudo nano dadapp
```

Add the Following Configuration:

```nginx
server {
    listen 80;
    server_name myapp.com;  # Replace with your domain or public IP

    location / {
        proxy_pass http://127.0.0.1:8000;  # Forward requests to Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Create a symbolic link of your configuration file to enable it. This will create a link in /etc/nginx/sites-enabled/ pointing to your configuration file in /etc/nginx/sites-available/.

```bash
sudo ln -s /etc/nginx/sites-available/dadapp /etc/nginx/sites-enabled
```

Test the Nginx Configuration:

`sudo nginx -t`

Restart Nginx:

`sudo systemctl restart nginx`

Check the status of Nginx:

`sudo systemctl status nginx`


## Setting Up a Systemd Service (Recommended for Production)
This will ensure your app starts automatically on boot and provides easy management commands (start, stop, restart, status).

To set up a systemd service for Gunicorn, create a new service file:

```bash
cd /etc/systemd/system
sudo nano dadapp.service
```

Add the following configuration:

```nginx
[Unit]
Description=Gunicorn instance to serve dad-bot
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Dad-Bot
ExecStart=/home/ubuntu/dad_venv/bin/gunicorn -b localhost:8000 app:app
Environment="ELEVENLABS_API_KEY=xxx"
Environment="OPENAI_API_KEY=xxx"
Environment="SECRET_KEY=xxx"
Restart=always

[Install]
WantedBy=multi-user.target
```

**Note**: The Environment variables need to be set in the systemd service file. If you've saved your environment variables in ~/.bashrc, they'll be available in interactive bash shells. However, when systemd starts services like your Gunicorn service, it doesn't read variables from shell-specific files like ~/.bashrc.

### Reload and Restart the Service
After making these changes, reload the systemd configuration and restart your service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart dadapp.service
```

### Enable and start the service

Use systemctl to manage the service (start, stop, restart, status).

`sudo systemctl enable dadapp.service`

`sudo systemctl start dadapp.service`

`sudo systemctl status dadapp.service`


## Point the IP address to a domain name

### In IONOS

- Go to Domains
- Select the domain
- Go to Subdomains
- Create a subdomain
- Click on DNS
- Point the A record to the IP address of the EC2 instance
- Edit A records for both @ and www to point to the IP address
- Save

**Note:** DNS changes can take some time to propagate across the internet. It's common to allow up to 24-48 hours, but often changes take effect much more quickly.

## Running your app on an HTTPS address

Make sure the security group associated with your EC2 instance allows inbound connections on port 443 (HTTPS).

Use **Let's Encrypt** - a free, automated, and open Certificate Authority - with **Certbot** - a client that fetches and deploys SSL/TLS certificates for your web server.

### Step 1: Install Certbot and the Nginx Plugin

```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx -y
```

### Step 2: Adjust Your Nginx Configuration

`cd /etc/nginx/sites-available/`

`sudo nano dadapp`

Ensure the server_name directive is set to your subdomain:

`server_name dadbot.followcrom.online;`

So:

```nginx
server {
    listen 80;
    server_name dadbot.followcrom.online;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Forward requests to Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 3: Test and Reload Nginx

`sudo nginx -t`

`sudo systemctl reload nginx`

### Step 4: Obtain and Install SSL Certificate

Run Certbot with the Nginx plugin to obtain and install an SSL certificate:

```bash
sudo certbot --nginx -d dadbot.followcrom.online
```

Certbot will guide you through the process.

### Step 5: Automatic Renewal
Let's Encrypt certificates are valid for 90 days. Certbot creates a cron job or systemd timer to handle renewals, so your certificates should renew automatically. To test the renewal process, you can run:

`sudo certbot renew --dry-run`

<br>

# Git / Github

```git
git checkout aws

git add .

git commit -m "Add changes for AWS deployment"

git push origin aws
```

# Eleven Labs API

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