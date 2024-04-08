#!/bin/bash

# Update the package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Clean up unused packages and free up disk space
sudo apt autoremove -y
sudo apt autoclean

# Reboot the VM (optional)
# sudo reboot