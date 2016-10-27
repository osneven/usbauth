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
	PATH = None
	CONNECTED = None
	VENDOR = None
	VENDOR_ID = None
	PRODUCT	= None
	PRODUCT_ID = None
	SERIAL = None
	HASH = None
	AUTHENTICATED = None
	WHITELISTED = False

	# Initializes the USB device using the root of its path and gathers information about it, and saves it all as bytes like objects
	def __init__(self, device_path):
		self.PATH = device_path
		self.CONNECTED = True
		self.read_device_information()
		self.generate_device_hash()

	# Reads the following information about the device and stores it in variables:
	#	vendor name, vendor id, product name, product id and serial
	def read_device_information(self):

		# Pre-define the need files, all of them needs to be prefixed by the root of the device's path
		information_files = ["manufacturer", "idVendor", "product", "idProduct", "serial"]
		information = []

		# Read the files
		for file_name in information_files:
			with open(self.PATH + file_name, "rb") as f:
				information.append(f.read())
				f.close()

		# Set the information variables
		self.VENDOR		= information[0]
		self.VENDOR_ID	= information[1]
		self.PRODUCT		= information[2]
		self.PRODUCT_ID	= information[3]
		self.SERIAL		= information[4]

	# Generates a SHA512 hash using the information gathered about the device and stores it in the hash variable
	def generate_device_hash(self):
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(self.VENDOR + self.VENDOR_ID + self.PRODUCT + self.PRODUCT_ID + self.SERIAL)
		self.HASH = digest.finalize()

	# Authenticates the device on system level, reguires root permissions!
	def authenticate(self):
		try:
			if self.CONNECTED:
				with open(self.PATH + Paths.AUTHORIZED_FILENAME, "wb") as f:
					f.write("1".encode("UTF-8"))
					f.close()
					self.AUTHENTICATED = True
					return True
		except PermissionError:
			return False

	# Deauthenticates the device on system level, reguires root permissions!
	def deauthenticate(self):
		try:
			if self.CONNECTED:
				with open(self.PATH + Paths.AUTHORIZED_FILENAME, "wb") as f:
					f.write("0".encode("UTF-8"))
					f.close()
					self.AUTHENTICATED = False
					return True
		except PermissionError:
			return False

	# Whitelists the device if the state is true, removes it from the whitelist if not
	def update_whitelist(self, state):
		self.WHITELISTED = state

	# Some getters for the device's information
	def get_path(self):
		return self.PATH
	def get_vendor(self):
		return self.VENDOR
	def get_vendor_id(self):
		return self.VENDOR_ID
	def get_product(self):
		return self.PRODUCT
	def get_product_id(self):
		return self.PRODUCT_ID
	def get_serial(self):
		return self.SERIAL
	def get_hash(self):
		return self.HASH
	def is_whitelisted(self):
		return self.WHITELISTED
	def is_authenticated(self):
		return self.AUTHENTICATED
	def is_connected(self):
		return self.CONNECTED
	def set_connected(self, state, path="Removed"):
		self.CONNECTED = state
		self.PATH = path
	def to_name_string(self):
		return self.VENDOR.decode("UTF-8").strip() + " " + self.PRODUCT.decode("UTF-8").strip()
