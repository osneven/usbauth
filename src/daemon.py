'''

This is the daemon for USBAuth

Author: Oliver Stochholm Neven
Email: oliver@neven.dk
Created on: 22. September 2016

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