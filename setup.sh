#!/usr/bin/env bash

# This is the installation script of USBAuth
# Author: Oliver Stochholm Neven
# Email: oliver@neven.dk
# Created on: 22. September 2016

INSTALL_PATH="/etc/usbauth"

# Check if script is run as root
echo "[+] Checking for root privileges..."
if [[ -z "$EUID" || "$EUID" != "0" ]]; then
	echo "Please run as root."
	exit 1
fi

# Check if an installation of usbauth already exists
echo "[+] Checking for previous installation ..."
if [ -d "$INSTALL_PATH" ]; then
	echo "It seems that an installation of usbauth already exists."
	while true; do
		read -p "Do you wish to reinstall? [Y/n] " yn
		case $yn in
			[Yy]* ) echo "[+] Removing files ..."; rm -rfv "$INSTALL_PATH"; grep -v "/etc/usbauth/usbauth start" "$HOME/.profile" > /tmp/usbauthrm && mv /tmp/usbauthrm "$HOME/.profile"; break;;
			[Nn]* ) exit 1;;
			* ) echo "Please answer yes or no.";;
		esac
	done
fi

# Move files
echo "[+] Copying source files ..."
mkdir "$INSTALL_PATH"
cp -rv ./src/* "$INSTALL_PATH"
cp -v ./README.md ./LICENSE.txt "$INSTALL_PATH"
cd "$INSTALL_PATH"

# Make the launch files executable
chmod 755 "usbauth"
chmod 755 "sudostart"

# Update the USB authentication password through the GUI
echo "[+] Setting password ..."
RESULT="False"
while [ "$RESULT" != "True" ]
do
    RESULT=$(python3 -c "from password import update_gui;print(update_gui())")
done

# Installation complete
echo "[+] Installation completed!"

# Instructions
echo "For help run /etc/usbauth/usbauth --help"
