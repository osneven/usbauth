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

# All files and directories used by the program
class Paths:
	def __init__(self):
		# Directory where the program source files is located
		self.__source_dir = "/opt/usbauth/"

		# Where to store temporary files, should be cleared everytime the process is terminated
		self.__temporary_dir = "/tmp/usbauth/"
		self.__pid_file		 = self.get_temporary_dir() + "process-pid"
		self.__log_name_file = self.get_temporary_dir() + "process-logname"

		# Where to store files for longer periods, such as logs
		self.__various_dir	 = "/var/usbauth/"
		self.__database_file = self.get_various_dir() + "storage.db"
		self.__log_dir		 = self.get_various_dir() + "logs/"

		# Where to store configuration files
		self.__configuration_dir = self.get_various_dir() + "config/"

		# Where to store sensetive information, such as password hashes and salts
		self.__secret_dir		  = self.get_various_dir() + "secret/"
		self.__passowrd_hash_file = self.get_secret_dir() + "password-hash"
		self.__password_salt_file = self.get_secret_dir() + "password-salt"

		# Where USB connections shows up as 'folders'
		self.__usb_bus_dir			   = "/sys/bus/usb/devices/"
		self.__usb_authorized_filename = "authorized"
		self.__usb_vendor_filename	   = "manufacturer"
		self.__usb_vendor_id_filename  = "idVendor"
		self.__usb_product_filename	   = "product"
		self.__usb_product_id_filename = "idProduct"
		self.__usb_serial_filename	   = "serial"

	# Creates all the directories if they don't exists
	def create_directories(self):
		directories = []
		for item in self.__dict__:
			x = 3
			if len(item) > x and item[-x:].lower() == "dir":
				directories.append(item)
		[print(x) for x in directories]

	# Getters for all the directories and files
	def get_source_dir(self): 			return self.__source_dir
	def get_temporary_dir(self): 		return self.__temporary_dir
	def get_pid_file(self):				return self.__pid_file
	def get_log_name_file(self):		return self.__log_name_file
	def get_various_dir(self): 			return self.__various_dir
	def get_database_file(self):		return self.__database_file
	def get_log_dir(self):				return self.__log_dir
	def get_configuration_dir(self): 	return self.__configuration_dir
	def get_secret_dir(self): 			return self.__secret_dir
	def get_password_hash_file(self):	return self.__passowrd_hash_file
	def get_password_salt_file(self):	return self.__password_salt_file
	def get_usb_bus_dir(self):			return self.__usb_bus_dir
	def get_usb_authorized_filename(self): 	return self.__usb_authorized_filename
	def get_usb_vendor_filename(self):		return self.__usb_vendor_filename
	def get_usb_vendor_id_filename(self):	return self.__usb_vendor_id_filename
	def get_usb_product_filename(self):		return self.__usb_product_filename
	def get_usb_product_id_filename(self):	return self.__usb_product_id_filename
	def get_usb_serial_filename(self):		return self.__usb_serial_filename

"""
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
"""
