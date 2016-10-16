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
from threading import Thread
from logger import Logger
from pyudev import Context, Monitor
from sys import exit
from paths import Paths
from device import Device

# This class listens for new USB device connections, and sends them through the authentication process
class Listener:

	# Initializes a logger
	def __init__(self):
		global LOGGER, CONNECTED_DEVICES
		LOGGER = Logger()
		CONNECTED_DEVICES = []

	# Starts listening for USB connections
	def listen(self):

		# Initialize pyudev monitor
		ctx = Context()
		mon = Monitor.from_netlink(ctx)
		mon.start()

		# Start listening and send all new connections to another thread
		LOGGER.log("Listening for USB devices")
		try:
			for dev in iter(mon.poll, None):
				connection_thread = Thread(target=Listener.connection, args=[self, dev])
				connection_thread.daemon = True
				connection_thread.start()
		except KeyboardInterrupt:
			LOGGER.log("Exited by user!")
			exit(1)

	# Sends a USB device to authentication if necessary
	def connection(self, dev):

		# Get some connection information beforing continuing to authentication process
		path = self.connection_device_path(dev)
		if not path: return
		insertion = self.connection_type(dev)

		# Check if the connection was an insertion or removal
		if insertion: self.insertion(path)
		else: self.removal(path)

	# Handles post insertion of a device path
	def insertion(self, path):
		LOGGER.log("Insertion at " + path)
		device = Device(path)
		CONNECTED_DEVICES.append(device)
		device.deauthenticate()
		# TODO: Prompt for authentification, allow for methods for either using X or using terminal

	# Handles post removal of a device path
	def removal(self, path):
		LOGGER.log("Removal at " + path)
		self.remove_device_by_path(path)

	# Removes a device from the list by it's path
	def remove_device_by_path(self, path):
		for device in CONNECTED_DEVICES:
			if device.get_path() == path:
				CONNECTED_DEVICES.remove(device)
				break

	# Returns true if device was inserted into the hub, and false if it was removed from it
	def connection_type(self, dev):
		return dev.get("ACTION") == "add"

	# Returns the full path to the device's system files, e.g. authorized, vendor, product, etc.
	# Returns false if it's not the root of the device's path
	def connection_device_path(self, dev):
		dev_path = dev.get("DEVPATH").split("/")
		hub = dev_path[-2]  # The hub the USB is connected to
		port = dev_path[-1]  # The port the USB is connected to
		if not (hub[:3] == "usb" and hub[3:].isdigit()):  # Not the root connection of the USB
			return False
		return Paths.BUS_DIR + hub + "/" + port + "/"

# TODO: REMOVE DEBUG CODE
l = Listener()
l.listen()
