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
from database import USBDatabse

# A class used for handling:
#	password verification for USB device authentication, and
#	storing data about all USB devices it handles.
class DeviceManager:
	def __init__(self, logger=None):
		self.DATABASE = USBDatabase()
		self.LOGGER = logger

	# Add a device to the database and deauthenticates it
	def add_device(self, device):
		pass

	# States a device as not connected, leaves it in the DEVICES list
	# NOTE: This also sets the device's PATH to "Removed"
	def remove_device(self, device):
		pass

	# Returns the device that has a specific path
	def get_device_by_path(self, path):
		match = self.DATABASE.select_devices(self.DATABASE.ColumnNames.PATH, path)
		if len(match) > 0: return self.DATABASE.list_to_device(match[0])

	# Returns a list of all the connected devices
	def list_connected_devices(self):
		connected_devices = []
		for device in self.DEVICES:
			if device.is_connected(): connected_devices.append(device)
		return connected_devices
