#!/bin/bash
# A small setup script for the installation of USBAuth source code.

# Check that the script is running as root.
check_for_root() {
	if (( $EUID != 0 )); then
		echo "[-] Please run setup script as root"
		exit
	fi
}

# Fetch the install directory from the python paths file.
get_install_dir() {
	INSTALL_DIR=$(python3 -c "from src.paths import Paths; print(Paths.INSTALL_DIR)")
	echo "[*] USBAuth will be installed in $INSTALL_DIR"
}

# Fetch and move to the directory this setup script is located in.
get_setup_dir() {
	cd $(dirname $0)
	SETUP_DIR=$(pwd)/
}

# Check if the install directory already exists, if so, assume that the program is already installed.
# If that is the case, ask for a reinstall, otherwise just create the directory.
create_install_dir() {
	if [ -d "$INSTALL_DIR" ]; then
		echo "[*] Previous installation of USBAuth already exists"
		while true; do
			read -p "Do you wish to reinstall? [Y/n]: " answer
			case $answer in
				[Yy]* ) remove_source_files; break;;
				[Nn]* ) exit;;
				*) 			;;
			esac
		done
	fi
	echo "[*] Created install directory"
	mkdir -p $INSTALL_DIR
}

# Removes everything from the installation directory
remove_source_files() {
	echo "[*] Removing source files ..."
	rm -rf $INSTALL_DIR
}

# Copies the source files to the installation directory.
copy_source_files() {
	echo "[*] Copying source files ..."
	copy0="LICENSE.txt"
	copy1="README.md"
	copy2="src/*"
	cp -r $SETUP_DIR$copy0 $SETUP_DIR$copy1 $SETUP_DIR$copy2 $INSTALL_DIR
}

# Sets the USB device authentication password
set_password() {
	echo "[*] Updating USB device authentication password ..."
	password="a"
	verify="b"
	while true; do
		echo "Enter a new authentication password:"
		read -s password
		echo "Verify the authentication password:"
		read -s verify
		if [[ $password != $verify ]]; then
			echo "[-] The passwords did not match, try agian."
		else
			break
		fi
	done
	python3 -c "from password_manager import PasswordManager; pm = PasswordManager(None); pm.update_password_hash('$password')"
}

check_for_root			# Check for root permissions
get_setup_dir				# Save the setup directory path in SETUP_DIR
get_install_dir			# Save the install directory path in INSTALL_DIR
create_install_dir	# Creates the install directory
copy_source_files		# Copy source files
cd $INSTALL_DIR
set_password				# Set a new authentication password
