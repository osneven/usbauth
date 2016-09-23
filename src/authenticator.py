'''

This is the USB device authenticator for USBAuth

Author: Oliver Stochholm Neven
Email: oliver@neven.dk
Created on: 22. September 2016

'''

import os.path
from password import Password

# Handles authentication of USB devices
class Authenticator:

	def __init__(self, path):
		global DEV_PATH, SYS_PATH, PASSWORD
		SYS_PATH = "/sys/bus/usb/devices/"
		DEV_PATH = SYS_PATH + path
		PASSWORD = Password()
		result = self.deauthenticate_device()
		if not result:
			return

	# Starts the authentication process for the device
	def authenticate(self):
		print("opening gui")
		if PASSWORD.verify_gui(DEV_PATH):
			print("Authentication success.")
			self.authenticate_device()
		else:
			print("Authentication failed, wrong password or action was canceled.")

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

	# Check if the directory provided actually exists
	def existence_of_directory(self):
		return os.path.isdir(DEV_PATH)