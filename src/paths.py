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
# Some global paths needed in various circumstances
class Paths:
	INSTALL_DIR 	= "/usr/bin/usbauth/"			# Directory where the program is installed
	PASSWORD_FILE	= INSTALL_DIR + "passwd"		# SHA512 encrypted password byte file
	WHITELIST_FILE	= INSTALL_DIR + "whitelist"		# AES256 encrypted whitelist python pickle file
	PID_FILE		= INSTALL_DIR + "pid"			# File containing pid of running process, if any.
	LOG_DIR 		= INSTALL_DIR + "logs/"			# Directory where logs are stored
	BUS_DIR			= "/sys/bus/usb/devices/"		# Directory where USB devices "connect"
