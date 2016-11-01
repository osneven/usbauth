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
		self.VENDOR = None
		self.VENDOR_ID = None
		self.PRODUCT	= None
		self.PRODUCT_ID = None
		self.SERIAL = None
		self.HASH = None
		self.WHITELISTED = False
		self.TIMEOUT_DATE = None
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
		self.PRODUCT	= information[2]
		self.PRODUCT_ID	= information[3]
		self.SERIAL		= information[4]

	# Generates a SHA512 hash using the information gathered about the device and stores it in the hash variable
	def generate_device_hash(self):
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(self.VENDOR + self.VENDOR_ID + self.PRODUCT + self.PRODUCT_ID + self.SERIAL)
		self.HASH = digest.finalize()

	# Authenticates the device on system level, reguires root permissions!
	def authenticate(self):
		if self.CONNECTED:
			with open(self.PATH + Paths.AUTHORIZED_FILENAME, "wb") as f:
				f.write("1".encode("UTF-8"))
				f.close()

	# Deauthenticates the device on system level, reguires root permissions!
	def deauthenticate(self):
		if self.CONNECTED:
			with open(self.PATH + Paths.AUTHORIZED_FILENAME, "wb") as f:
				f.write("0".encode("UTF-8"))
				f.close()

	# Whitelists the device if the state is true, removes it from the whitelist if not
	# Optionally set a timespan value for the whitelist to timeout after that amout of time.
	# Also, set the unit when choosing a timespan, 0 for seconds, 1 for minutes and 2 for hours.
	def update_whitelist(self, state, timespan=None, unit=None):
		self.WHITELISTED = state

		# Set timeout date
		if timespan is not None and unit in list(range(3)):
			from datetime import datetime, timedelta

			# Get current date
			now_date = datetime.now()

			# Add the timespan in units to the current date
			if unit == 0: self.TIMEOUT_DATE = now_date + timedelta(seconds=timespan)
			elif unit == 1: self.TIMEOUT_DATE = now_date + timedelta(minutes=timespan)
			elif unit == 2: self.TIMEOUT_DATE = now_date + timedelta(hours=timespan)

		# Set timout date to none if whitelisted is False
		if not self.WHITELISTED and self.TIMEOUT_DATE is not None:
			self.TIMEOUT_DATE = None

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

	def get_hash_as_hex(self):
		from binascii import hexlify
		return hexlify(self.HASH).decode("ASCII")

	def is_whitelisted(self):

		# Check if a timeout date is set
		if self.TIMEOUT_DATE is not None:
			# Return whether the timeout date is in the future or not
			from datetime import datetime
			return self.TIMEOUT_DATE > datetime.now()
		# No timeout date, just return the value
		return self.WHITELISTED

	def get_timeout_date_str(self):
		if self.WHITELISTED:
			if self.TIMEOUT_DATE is None:
				return "removed from the whitelist"
			else:
				return self.TIMEOUT_DATE.strftime("%d/%m/%Y %I:%M:%S %p")
		return None
	def is_authenticated(self):
		# Read the "authorized" file and check if the USB device is authenticated
		with open(self.PATH + Paths.AUTHORIZED_FILENAME, "rb") as f:
			authenticated = (f.read().decode("UTF-8").strip() == "1")
			f.close()
		return authenticated
	def is_connected(self):
		return self.CONNECTED
	def set_connected(self, state, path="Removed"):
		self.CONNECTED = state
		if not state:
			self.PATH = path

	# Returns a string containing the vendor and then product name
	def to_name_string(self):
		return self.VENDOR.decode("UTF-8").strip() + " " + self.PRODUCT.decode("UTF-8").strip()
	# Returns a string containing the vendor and then product hex
	def to_id_string(self):
		return "(" + self.VENDOR_ID.decode("UTF-8").strip() + ":" + self.PRODUCT_ID.decode("UTF-8").strip() + ")"
	# Return full description for this device
	def get_description(self):
		desc = self.to_name_string() + " " + self.to_id_string() + "\n"
		desc += "Serial:\t" + self.get_serial().decode("UTF-8").strip() + "\n"
		desc += "Path:\t" + self.get_path() + "\n"
		H = self.get_hash_as_hex()
		desc += "Hash:\t" + H[:4] + "..." + H[-4:] + "\n"
		timeout_str = self.get_timeout_date_str()
		if timeout_str is not None:
			desc += "Whitelisted untill: " + timeout_str + "\n"

		return desc
