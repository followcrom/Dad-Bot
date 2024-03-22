# If not handled in user data:
sudo apt-get update
sudo apt-get upgrade -y


# Most Ubuntu images come with Python pre-installed, but to make sure you have Python3 and Pip:
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y

# To check if Python is pre-installed on your system and to identify the installed version, you can use the following commands in your terminal:
python3 --version

# Install the Python 3 venv module
sudo apt-get install python3-venv -y

# Install a package with debian non-interactive mode
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y <package-name>

# Check if Reboot is Needed:
if [ -f /var/run/reboot-required ]; then
    echo 'A system reboot is required'
else
    echo 'No reboot is required'
fi

# If needed, reboot the system. This will log you out of the VM and restart it.
sudo reboot


# Set Up a Virtual Environment
python3 -m venv dad_venv

# Activate the virtual environment
source dad_venv/bin/activate
