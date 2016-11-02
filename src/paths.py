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
from os.path import expanduser, exists
from os import makedirs

# Some global paths needed in various circumstances
class Paths:
	INSTALL_DIR 		= "/opt/usbauth/"				# Directory where the program source files is located.
	TMP_DIR				= "/tmp/usbauth/"				# Where to store temporary files, should be cleared everytime the process is terminated.
	CONFIG_DIR			= INSTALL_DIR + "config/"		# Directory where the program files that are not source files are located.
	PASSWORD_FILE		= CONFIG_DIR + "passwd"			# SHA512 hash of the password.
	DATABASE_FILE		= CONFIG_DIR + "database.db"	# AES256 encrypted pickle file.
	PID_FILE			= TMP_DIR + "pid"				# File containing the PID of the running process, if any.
	LOG_PATHNAME_FILE	= TMP_DIR + "logfile_name"		# File containing the log's file name of the running process, if any.
	LOG_DIR 			= INSTALL_DIR + "logs/"			# Directory where logs are stored.
	BUS_DIR				= "/sys/bus/usb/devices/"		# Directory where USB devices "connect".
	AUTHORIZED_FILENAME	= "authorized"					# The file name, needs to be prefixed by the root of a device path, of the system file that authenticates a device.
	VENDOR_FILENAME		= "manufacturer"				# Same as above, but with the vendor name.
	VENDOR_ID_FILENAME	= "idVendor"					# Same as above, but with the vendor ID.
	PRODUCT_FILENAME	= "product"						# Same as above, but with the product name.
	PRODUCT_ID_FILENAME	= "idProduct"					# Same as above, but with the product ID.
	SERIAL_FILENAME		= "serial"						# Same as above, but with the serial number.

	# Check if all directories above exists, if not, create them
	@staticmethod
	def create_paths():
		directories = [Paths.TMP_DIR, Paths.INSTALL_DIR, Paths.CONFIG_DIR, Paths.LOG_DIR]
		for directory in directories:
			if not exists(directory):
				makedirs(directory)

	# Deletes the temporary directory and all its content, should be called every time the process stops
	@staticmethod
	def delete_tmp_dir():
		from shutil import rmtree
		try:
			rmtree(Paths.TMP_DIR)
		except FileNotFoundError:
			pass
