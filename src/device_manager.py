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
import pickle
from paths import Paths

# A class used for handling:
#	password verification for USB device authentication, and
#	storing data about all USB devices it handles.
class DeviceManager:
	DEVICES = []

	def __init__(self):
		self.DEVICES = self.load_database_file()

	# Add a device to the database and deauthenticates it
	def add_device(self, device):
		# Removes any matching device
		for i in range(len(self.DEVICES)):
			if self.DEVICES[i].get_hash() == device.get_hash():
				del self.DEVICES[i]
				break

		# Adds the device
		device.deauthenticate()
		self.DEVICES.append(device)

	# States a device as not connected, leaves it in the DEVICES list
	# NOTE: This also sets the device's PATH to "Removed"
	def remove_device(self, device):
		# Looks for the matching device in the list
		for i in range(len(self.DEVICES)):
			if self.DEVICES[i].get_hash() == device.get_hash(): # Match found
				self.DEVICES[i].set_connected(False) 			# State is as "not connected"
				break

	# States all connected devices as non connected, leaves it in the DEVICES list
	# NOTE: This also sets the device's PATH to "Removed"
	def remove_all_devices(self):
		for device in self.DEVICES:
			if device.is_connected():
				device.set_connected(False)

	# Load and return data stored in the database file
	def load_database_file(self):
		Paths.create_paths()
		try:
			return pickle.load(open(Paths.DATABASE_FILE, "rb"))
		except FileNotFoundError: # Create an empty database file if non exists
			pickle.dump([], open(Paths.DATABASE_FILE, "wb"))
			return self.load_database_file()

	# Dump the devices into the database file
	def dump_database_file(self):
		pickle.dump(self.DEVICES, open(Paths.DATABASE_FILE, "wb"))

	# Returns the device that has a specific path
	def get_device_by_path(self, path):
		for device in self.DEVICES:
			if device.get_path() == path:
				return device
		return None

	# Returns a list of all the connected devices
	def list_connected_devices(self):
		connected_devices = []
		for device in self.DEVICES:
			if device.is_connected(): connected_devices.append(device)
		return connected_devices
