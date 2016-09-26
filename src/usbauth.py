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

Usage:
	--start 			- starts the daemon
	--start-login 	- writes a rule to ~/.profile so that it starts on login

	--stop			- stops the daemon
	--stop-login		- removes the rule from ~/.profile

	--update-pass		- changes the USB authentication password. Requires root!

	--uninstall		- uninstalls the program from the computer

Dependencies:
	python (>= 3.5.1)
	cryptography (>= v1.2.3)
	pyqt5 (>= 5.5.1)
	pyudev (>= 0.16.1)

'''

import argparse
from daemon import Daemon

NAME = "USBAuth"
VERSION = 1.0
DESCRIPTION = "A USB device authentication tool."

# Handles launch of the program
class Launcher:

	# Parses arguments from the command line
	def argument_parser(self):
		parser = argparse.ArgumentParser(description=NAME + " (" + str(VERSION) + ") : " + DESCRIPTION)
		parser.add_argument("--start", help="starts the daemon", action="store_true")
		parser.add_argument("--start-login", help="writes a rule to ~/.profile so that it starts on login", action="store_true")
		parser.add_argument("--stop", help="stops the daemon", action="store_true")
		parser.add_argument("--stop-login", help="removes the rule from ~/.profile", action="store_true")
		parser.add_argument("--update-pass", help="changes the USB authentication password. Requires root privileges!", action="store_true")
		parser.add_argument("--uninstall", help="uninstalls the program from the computer", action="store_true")
		return parser.parse_args()

	# Launches the program
	def launch(self):
		args = self.argument_parser()
		if args.start: self.start()
		elif args.start_login: self.start_login()
		elif args.stop: self.stop()
		elif args.start_login: self.stop_login()
		elif args.update_pass: self.update_pass()
		elif args.uninstall: self.uninstall()

	def start(self):
		d = Daemon()
		d.start()
	def start_login(self):
		pass
	def stop(self):
		pass
	def stop_login(self):
		pass
	def update_pass(self):
		pass
	def uninstall(self):
		pass

try:
	launcher = Launcher()
	launcher.launch()
except KeyboardInterrupt:
	print("Exiting ...")