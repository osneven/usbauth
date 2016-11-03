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
from pysqlcipher import dbapi2 as lite
from paths import Paths

#
# TODO: Make a sqlite, encrypted, database for storing information about previous USB devices.
#		This is how the structure should look:
#

class USBDatabse:

	def __init__(self):
		self.OPEN = False

	###
	### Globally used methods
	###

	#
	# Handle opening and closing of the database
	#

	# Connects to the database file and decrypts it
	def open(self, cleartext_password):
		self.CONN = lite.connect(Paths.DATABASE_FILE, detect_types=lite.PARSE_DECLTYPES)
		self.CUR = self.CONN.cursor()
		self.CUR.execute('PRAGMA key="{}"'.format(cleartext_password))
		self.CUR.execute('PRAGMA kdf_iter=100000')
		self.OPEN = True

	# Closes the database connection
	def close(self):
		self.CUR.close()
		self.CONN.commit()
		self.CONN.close()
		self.OPEN = False

	#
	# Handle USB device connections
	#

	# Inserts the data of a device into a row in the table
	def insertion_of_device(self, device):
		if not self.OPEN(): return
		self.ensure_table_exists()

	def removal_of_device(self, device):
		pass

	#
	# Additional methods
	#

	def list_connected_devices(self):
		pass

	def get_device_by_path(self, device_path):
		pass

	###
	### Methods that only need to be executed inside this class
	###

	# Creates the "Devices" table if it doesn't already exist
	def ensure_table_exists(self):
		if not self.OPEN: return
		table_name = "Devices"
		collums = "\
		ID 				INT 	AUTOINCREMENT,\
		VENDOR			TEXT	NOT NULL,\
		VENDOR_ID		TEXT	NOT NULL,\
		PRODUCT			TEXT	NOT NULL,\
		PRODUCT_ID 		TEXT	NOT NULL,\
		SERIAL 			TEXT	NOT NULL,\
		HASH			BLOB	NOT NULL,\
		PATH			TEXT	NOT NULL,\
		CONNECTED		INT		NOT NULL,\
		WHITELISTED		INT		NOT NULL,\
		TIMEOUT_DATE	TEXT	NOT NULL,\
		"
		self.CUR.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, collums))

	# Converts, and returns, a device into a list, parsable by SQL
	def device_to_list(self, device):
		pass
