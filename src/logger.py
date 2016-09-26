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

# Handles log creation and prints to the screen
class Logger:
	# If quiet is true, no information is printed to stdout, only to log files
	def __init__(self):
		global LOG_DIRECTORY
		LOG_DIRECTORY = "/etc/usbauth/logs/"

	# Open a logfile for entries
	def open_logfile(self):
		from os import makedirs
		from os.path import isdir
		global LOG_FILE
		if not isdir(LOG_DIRECTORY): makedirs(LOG_DIRECTORY)
		pathname = LOG_DIRECTORY + "USBAUTH-" + self.get_time_string() + ".log"
		LOG_FILE = open(pathname, "wb")
		self.log("### START OF LOG ###")

	# Close the logfile
	def close_logfile(self):
		self.log("### END OF LOG ###")
		LOG_FILE.close()

	# Return a human readable time string
	def get_time_string(self):
		from datetime import datetime
		t = datetime.now()
		return str(t.year) + "-" + str(t.month) + "-" + str(t.day) + "-" + str(t.hour) + "-" + str(t.minute) + "-" + str(t.second)

	# Log an entry
	def log(self, entry):
		entry = self.get_time_string() + ":\t" + entry + "\n"
		LOG_FILE.write(entry.encode("UTF-8"))
		print(entry)