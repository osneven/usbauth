#!/usr/bin/python3

import pyudev
import os
from threading import Thread
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Listens for any new USB device connection
class Daemon:
	
	# Starts listening
	def start():
		ctx = pyudev.Context()
		mon = pyudev.Monitor.from_netlink(ctx)
		mon.start()

		print("Listening for USB devices ...")
		connected_paths = []
		for device in iter(mon.poll, None):
			thread = Thread(target=Daemon.connection, args=[device, connected_paths])
			thread.daemon = False
			thread.start()

	# Called as a new thread with the device connection
	def connection(device, connected_paths):
		insertion = device.get("ACTION") == "add"
		dev_path = device.get("DEVPATH").split("/")
		hub = dev_path[-2]	# The hub the USB is connected to
		port = dev_path[-1] # The port the USB is connected to
		if not hub[:3] == "usb": # Not the root connection of the USB
			return
		path = hub + "/" + port + "/"

		# If the USB was inserted into the computer
		if insertion:
			print("Connection at", path)
			connected_paths.append(path)
			auth = Authenticator(path)
			if auth.existence_of_directory():
				print("Device path found")
				auth.authenticate()
			else:
				print("Device path not found")

		# If the USB was removed from the computer
		else:
			print("Removal at", path)
			if path in connected_paths:
				connected_paths.remove(path)


# Handles authentication of USB devices
class Authenticator:
	global SYS_PATH
	SYS_PATH = "/sys/bus/usb/devices/"

	def __init__(self, path):
		global DEV_PATH
		DEV_PATH = SYS_PATH + path
		result = Authenticator.deauthenticate_device(self)
		if not result:
			return

	# Check if the directory provided actually exists
	def existence_of_directory(self):
		return os.path.isdir(DEV_PATH)

	# Starts the authentication process for the device
	def authenticate(self):
		password_bytes = Authenticator.prompt_for_password(self)
		if CREDENTIALS.verify(password_bytes):
			print("Authentication success.")
			Authenticator.authenticate_device(self)
		else:
			print("Authentication failed, wrong password.")

	# Authenticates the device on the system
	def authenticate_device(self):
		try:
			with open(DEV_PATH + "authorized", "wb") as file:
				file.write(b"1")
				file.close()
				return True
		except:
			print(DEV_PATH, "was not found")
			return False

	# De authenticates the device on the system
	def deauthenticate_device(self):
		try:
			with open(DEV_PATH + "authorized", "wb") as file:
				file.write(b"0")
				file.close()
				return True
		except:
			print(DEV_PATH, "was not found")
			return False

	# Prompts for a password and returns it as bytes
	def prompt_for_password(self):
		print("Please enter your USB authentication password.")
		return input().encode("UTF-8")
		
# Handles password verification
class CredentialsManager:
	global USBAUTH_PATH
	global PASSWORD_FILENAME
	USBAUTH_PATH = os.path.expanduser("~") + "/.usbauth/"
	PASSWORD_FILENAME = "passwd"

	def __init__(self):
		if not CredentialsManager.ensure_usbauth_path(self, PASSWORD_FILENAME, False):
			print("ERROR: Password file removed!")

	# Ensures that the USB_PATH exists, if create is set to true creates if it does not
	# Can also check if a sub file exists inside that main directory
	# Returns true if, and only if the main directory, and if set, and the sub file exists
	def ensure_usbauth_path(self, sub_file=None, create=True):
		if os.path.isdir(USBAUTH_PATH):
			if sub_file is not None:
				sub_file_full_path = USBAUTH_PATH + sub_file
				if not os.path.isfile(sub_file_full_path) and create:
					open(sub_file_full_path, "wb").close()	
					return False
			return True
		else:
			print("Creating the directory", USBAUTH_PATH, "...")
			if create:
				os.makedirs(USBAUTH_PATH)
				if sub_file is not None:
					print("Creating the file", sub_file, "...")
					open(USBAUTH_PATH + sub_file, "wb").close()
			return False

	# Verifies that the password bytes' hash matches the one stored in the file
	def verify(self, password_bytes):
		hashed_password_bytes = CredentialsManager.SHA512_of_bytes(self, password_bytes)

		# If the password file already exists, match the contents with the hashed password
		if CredentialsManager.ensure_usbauth_path(self, PASSWORD_FILENAME):
			with open(USBAUTH_PATH + PASSWORD_FILENAME, 'rb') as file:
				hash_bytes = file.read()
				match = hash_bytes == hashed_password_bytes
				file.close()
				return match

		# If the file doesn't exist
		else:
			print("ERROR: Password file removed!")
			return False

	# Simply returns the SHA512 values as bytes from the given message bytes
	def SHA512_of_bytes(self, message_bytes):
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(message_bytes)
		return digest.finalize()

	# Prompts user for a password change
	def change_password(self):
		print("Please set a USB authentication password.")
		hashed_password_bytes = CredentialsManager.SHA512_of_bytes(self, input().encode("UTF-8"))
		with open(USBAUTH_PATH + PASSWORD_FILENAME, "wb") as file:
			file.write(hashed_password_bytes)
			file.close()

	def get_PASSWORD_FILENAME(self):
		return PASSWORD_FILENAME

global CREDENTIALS
CREDENTIALS = CredentialsManager()

# Start the daemon
try:
	daemon = Daemon
	daemon.start()
except KeyboardInterrupt:
	print("\nExiting ...")
	exit()