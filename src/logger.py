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
from paths import Paths

# This class is used to log feedback to stdout and a generated log file
# Log files are contained within the logs directory, see paths.py
class Logger:

	# Initializes an empty log file
	def __init__(self):
		global LOG_FILE
		Paths.create_paths()
		LOG_FILE = Paths.LOG_DIR + self.generate_log_name()
		open(LOG_FILE, "wb").close() # Initialize empty file

	# Logs a message to stdout and the log file
	def log(self, message):
		message = self.get_time_stamp() + ": " + message + "\n"
		print(message, end="")
		with open(LOG_FILE, "ab") as f:
			f.write(message.encode("UTF-8"))
			f.close()

	# Generates and returns a new log name using this format:
	#	USBAUTH-LOG_<cureent time stamp>
	def generate_log_name(self):
		return "USBAUTH-LOG_" + self.get_time_stamp()

	# Returns the current time stamp using this format:
	#	LOG_YYYY-MM-DD_hh-mm-ss
	def get_time_stamp(self):
		from datetime import datetime
		t = datetime.now()
		return str(t.year) + "-" + str(t.month) + "-" + str(t.day) + "_" + str(t.hour) + "-" + str(t.minute) + "-" + str(t.second)
