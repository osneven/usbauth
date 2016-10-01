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

# The paths used for UNIX like operating systems
class UNIX_PATHS:
	def get_install_dir_path(self):
		return "/etc/usbauth/"
	def get_password_file_path(self):
		return self.get_install_dir_path() + "passwd"
	def get_pid_file_path(self):
		return self.get_install_dir_path() + "pid"
	def get_log_dir_path(self):
		return self.get_install_dir_path() + "log/"
	def get_usb_bus_path(self):
		return "/sys/bus/usb/devices/"


