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
from pyudev import Context
from pyudev.Monitor import from_netlink
from sys import exit

# This class listens for new USB device connections, and sends them through the authentication process
class Listener:

	# Initializes a logger
	def __init__(self):
		global LOGGER
		LOGGER = Logger()

	# Starts listening for USB connections
	def listen(self):

		# Initialize pyudev monitor
		ctx = Context()
		mon = from_netlink(ctx)
		mon.start()

		# Start listening and send all new connections to another thread
		LOGGER.log("Listening for USB devices")
		connected_device_paths = []
		try:
			for dev in iter(mon.poll(), None):
				connection_thread = Thread(target=Listener.connection, args=[self, dev, connected_device_paths])
				connection_thread.daemon = True
				connection_thread.start()
		except KeyboardInterrupt:
			LOGGER.log("Exited by user!")
			exit(1)

		# Sends a USB device to authentication if necessary

# TODO: REMOVE DEBUG CODE
l = Listener()
l.listen()
