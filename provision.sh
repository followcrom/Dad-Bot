# If not handled in user data:
# Update the package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Clean up unused packages and free up disk space
sudo apt autoremove -y
sudo apt autoclean


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
# sudo reboot


# Set Up a Virtual Environment
python3 -m venv dad_venv

# Activate the virtual environment
source dad_venv/bin/activate

# If you need to install these dependencies on another system (like your AWS EC2 instance), simply activate the virtual environment there and run:
pip install -r requirements.txt

# If you only need the environment variables for a single session (they'll be lost after you log out or close the terminal), you can export them directly in the terminal:
export ELEVENLABS_API_KEY=
export OPENAI_API_KEY=
export SECRET_KEY=

