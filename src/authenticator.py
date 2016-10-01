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

import os.path
from password import Password
from paths import UNIX_PATHS

# Handles authentication of USB devices
class Authenticator:

	def __init__(self, path, logger):
		global DEV_PATH, PASSWORD, LOGGER
		DEV_PATH = UNIX_PATHS.get_usb_bus_path() + path
		PASSWORD = Password()
		LOGGER = logger
		result = self.deauthenticate_device()
		if not result:
			return

	# Starts the authentication process for the device
	def authenticate(self):
		if PASSWORD.verify_gui(DEV_PATH):
			LOGGER.log("Authentication success on " + DEV_PATH)
			self.authenticate_device()
		else:
			LOGGER.log("Authentication attempt failed on " + DEV_PATH)

	# Authenticates the device on the system
	def authenticate_device(self):
		try:
			with open(DEV_PATH + "authorized", "wb") as file:
				file.write(b"1")
				file.close()
				return True
		except PermissionError:
			LOGGER.log("No permissions, please run daemon as root!")
			exit()
		except:
			LOGGER.log(DEV_PATH, "was not found")
			return False

	# De authenticates the device on the system
	def deauthenticate_device(self):
		try:
			with open(DEV_PATH + "authorized", "wb") as file:
				file.write(b"0")
				file.close()
				return True
		except PermissionError:
			LOGGER.log("No permissions, please run daemon as root!")
			exit()
		except:
			LOGGER.log(DEV_PATH + " was not found")
			return False

	# Check if the directory provided actually exists
	def existence_of_directory(self):
		return os.path.isdir(DEV_PATH)