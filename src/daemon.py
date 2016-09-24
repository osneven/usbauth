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

import pyudev
from authenticator import Authenticator
from threading import Thread

# The actual daemon program
class Daemon:

	# Starts listening
	def start(self):
		ctx = pyudev.Context()
		mon = pyudev.Monitor.from_netlink(ctx)
		mon.start()

		print("Listening for USB devices ...")
		connected_paths = []
		for device in iter(mon.poll, None):
			thread = Thread(target=Daemon.connection, args=[self, device, connected_paths])
			thread.daemon = False
			thread.start()

	# Called as a new thread with the device connection
	def connection(self, device, connected_paths):
		insertion = device.get("ACTION") == "add"
		dev_path = device.get("DEVPATH").split("/")
		hub = dev_path[-2]  # The hub the USB is connected to
		port = dev_path[-1]  # The port the USB is connected to
		if not hub[:3] == "usb":  # Not the root connection of the USB
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