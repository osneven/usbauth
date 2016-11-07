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
	QUIET = None
	LOG_FILE = None

	# Initializes an empty log file
	def __init__(self, quiet):
		from os.path import isfile

		# Get a name for the log file
		log_file = self.load_log_filename()
		if log_file is None: # If no name is stored on the disk, generate a new one.
			log_file = Paths.LOG_DIR + self.generate_log_name()

		# Ensure that log file exists
		if not isfile(log_file):
			Paths.create_paths()
			open(log_file, "wb").close() # Initialize empty file

		self.LOG_FILE = log_file
		self.dump_log_filename()
		self.QUIET = quiet

	# Checks if there is a log filename stored on the disk
	def load_log_filename(self):
		Paths.create_paths()
		try:
			with open(Paths.LOG_PATHNAME_FILE, "rb") as f:
				log_file = f.read().decode("UTF-8")
				f.close()
				return log_file
		except FileNotFoundError:
			return None

	# Dumps the log filename to the disk
	def dump_log_filename(self):
		Paths.create_paths()
		with open(Paths.LOG_PATHNAME_FILE, "wb") as f:
			f.write(self.LOG_FILE.encode("UTF-8"))
			f.close()

	# Logs a message to stdout and the log file
	def log(self, message):
		message = self.get_time_stamp() + ": " + message + "\n"
		if not self.QUIET:
			print(message, end="")
		with open(self.LOG_FILE, "ab") as f:
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
