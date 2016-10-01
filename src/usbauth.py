#!/usr/bin/python3
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

Usage (after install):
	/etc/usbauth/usbauth --help

Dependencies:
	python (>= 3.5.1)
	cryptography (>= v1.2.3)
	pyqt5 (>= 5.5.1)
	pyudev (>= 0.16.1)

'''

import argparse
from daemon import Daemon
from paths import get_pid_file_path, get_install_dir_path

NAME = "USBAuth"
VERSION = 1.0
DESCRIPTION = "A USB device authentication tool."

# Handles launch of the program
class Launcher:

	# Parses arguments from the command line
	def argument_parser(self):
		parser = argparse.ArgumentParser(description=NAME + " (" + str(VERSION) + ") : " + DESCRIPTION)
		parser.add_argument("--start", help="starts the daemon", action="store_true")
		parser.add_argument("--stop", help="stops the daemon", action="store_true")
		parser.add_argument("--update-pass", help="changes the USB authentication password. Requires root privileges!", action="store_true")
		return parser.parse_args()

	# Launches the program
	def launch(self):
		args = self.argument_parser()
		if args.start: self.start()
		elif args.stop: self.stop()
		elif args.update_pass: self.update_pass()
		elif args.uninstall: self.uninstall()

	# Starts the daemon
	def start(self):
		self.write_pid_file()
		d = Daemon()
		d.start()

	# Stops the daemon
	def stop(self):
		from os import kill
		from signal import SIGTERM
		PID = self.read_pid_file()
		kill(int(PID), SIGTERM)

	# Updates the password
	def update_pass(self):
		from password import update_gui
		update_gui()

	# Writes the this process PID to a PID file
	def write_pid_file(self):
		from os import getpid
		PID = getpid()
		with open(get_pid_file_path(), "wb") as f:
			f.write(str(PID).encode("UTF-8"))
			f.close()

	# Reads and returns the PID stored in the PID file
	def read_pid_file(self):
		with open(get_pid_file_path(), "rb") as f:
			PID = f.read().decode("UTF-8")
			f.close()
		return PID

launcher = Launcher()
launcher.launch()