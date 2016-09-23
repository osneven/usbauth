#!/usr/bin/python3
'''

This is the daemon launch manager for USBAuth

Author: Oliver Stochholm Neven
Email: oliver@neven.dk
Created on: 22. September 2016

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
	easygui (>= 0.96)
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






launcher = Launcher()
launcher.launch()