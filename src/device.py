'''
USBAuth, a USB device authentication tool.
Copyright (C) 2016  Oliver Stochholm Neven

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For any further information contact me at oliver@neven.dk
'''
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from paths import Paths

# A class containg different information about a connected USB device and handles authentication on the system level
class Device:

	# Initializes the USB device using the root of its path and gathers information about it, and saves it all as bytes like objects
	def __init__(self, device_path):
		global PATH, CONNECTED
		PATH = device_path
		CONNECTED = True
		self.read_device_information()
		self.generate_device_hash()

	# Reads the following information about the device and stores it in variables:
	#	vendor name, vendor id, product name, product id and serial
	def read_device_information(self):
		global VENDOR, VENDOR_ID, PRODUCT, PRODUCT_ID, SERIAL

		# Pre-define the need files, all of them needs to be prefixed by the root of the device's path
		information_files = ["manufacturer", "idVendor", "product", "idProduct", "serial"]
		information = []

		# Read the files
		for file_name in information_files:
			with open(PATH + file_name, "rb") as f:
				information.append(f.read())
				f.close()

		# Set the information variables
		VENDOR		= information[0]
		VENDOR_ID	= information[1]
		PRODUCT		= information[2]
		PRODUCT_ID	= information[3]
		SERIAL		= information[4]

	# Generates a SHA512 hash using the information gathered about the device and stores it in the hash variable
	def generate_device_hash(self):
		global HASH
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(VENDOR + VENDOR_ID + PRODUCT + PRODUCT_ID + SERIAL)
		HASH = digest.finalize()

	# Authenticates the device
	def authenticate(self):
		global AUTHENTICATED
		if CONNECTED:
			with open(PATH + Paths.AUTHORIZED_FILENAME, "wb") as f:
				f.write("1".encode("UTF-8"))
				f.close()
				AUTHENTICATED = True

	# Deauthenticates the device
	def deauthenticate(self):
		global AUTHENTICATED
		if CONNECTED:
			with open(PATH + Paths.AUTHORIZED_FILENAME, "wb") as f:
				f.write("0".encode("UTF-8"))
				f.close()
				AUTHENTICATED = False

	# Whitelists the device if the state is true, removes it from the whitelist if not
	def update_whitelist(self, state):
		global WHITELISTED
		WHITELISTED = state

	# Some getters for the device's information
	def get_path(self):
		return PATH
	def get_vendor(self):
		return VENDOR
	def get_vendor_id(self):
		return VENDOR_ID
	def get_product(self):
		return PRODUCT
	def get_product_id(self):
		return PRODUCT_ID
	def get_serial(self):
		return SERIAL
	def get_hash(self):
		return HASH
	def is_whitelisted(self):
		return WHITELISTED
	def is_authenticated(self):
		return AUTHENTICATED
	def is_connected(self):
		return CONNECTED
	def set_connected(self, state, path="Removed"):
		global CONNECTED, PATH
		CONNECTED = state
		PATH = path
