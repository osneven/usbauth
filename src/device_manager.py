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

class DeviceManager:
	def __init__(self):
		global CONNECTED_DEVICES
		DEVICES = self.load_database_file()

	# Add a device to the database and deauthenticates it
	def add_device(self, device):
		# Removes any matching device
		for dev in DEVICES:
			if dev.get_hash() == device.get_hash():
				DEVICES.remove(dev)
				break

		# Adds the device
		device.deauthenticate()
		DEVICES.append(device)

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
		pickle.dump(DEVICES, open(Paths.DATABASE_FILE, "wb"))
