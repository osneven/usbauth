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
from device import Device
from pysqlcipher import dbapi2 as lite
from paths import Paths

#
# TODO: Make a sqlite, encrypted, database for storing information about previous USB devices.
#		This is how the structure should look:
#

class USBDatabse:

	def __init__(self):
		self.OPEN = False
		self.TABLE_NAME = "Devices"




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





	# Inserts the data of a device into a row in the table
	def insertion_of_device(self, device):
		if not self.OPEN: return
		self.ensure_table_exists()

		# Chek if the device is already stored in the database, there should not be any more than one
		match = self.select_devices("HASH", device.get_hash())]
		if match is not None and len(match) > 0: # There is a match

			# Merge the matched devices information into the new device and delete the match
			match = match[0]
			match_device = self.list_to_device(match)
			device = self.merge_old_and_new_device(device, match_device)
			self.delete_devices("ID", match[0])

		# Insert the new device into the table
		device_values = self.device_to_list(device)
		self.insert_values(device_values)

	def removal_of_device(self, device):
		pass






	def list_connected_devices(self):
		pass

	def get_device_by_path(self, device_path):
		pass



	# Creates the "Devices" table if it doesn't already exist
	def ensure_table_exists(self):
		if not self.OPEN: return
		columns = "\
		ID 				INT 	AUTOINCREMENT,\
		VENDOR			TEXT	NOT NULL,\
		VENDOR_ID		TEXT	NOT NULL,\
		PRODUCT			TEXT	NOT NULL,\
		PRODUCT_ID 		TEXT	NOT NULL,\
		SERIAL 			TEXT	NOT NULL,\
		HASH			BLOB	NOT NULL,\
		PATH			TEXT	NOT NULL,\
		CONNECTED		INT		NOT NULL,\
		WHITELISTED		BOOLEAN	NOT NULL,\
		TIMEOUT_DATE	TIMESTAMP,\
		"
		self.CUR.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(self.TABLE_NAME, columns))



	# Converts, and returns, a device object into a list, parsable by SQL
	# Returns in the same sequence as the "Devices" table columns
	def device_to_list(self, device):
		return [
			device.get_vendor().decode("UTF-8"),
			device.get_vendor_id().decode("UTF-8"),
			device.get_product().decode("UTF-8"),
			device.get_product_id().decode("UTF-8"),
			device.get_serial().decode("UTF-8"),
			device.get_hash(),
			device.get_path(),
			device.is_connected(),
			device.is_whitelisted(),
			device.get_timeout_date()
		]

	# Converts, and returns, a list parsable by SQL into a device object
	# Parses the list in the same sequence as the "Devices" table columns
	def list_to_device(self, device_list):
		device = Device(None, read_information=False)
		device.VENDOR 		= device_list[1].encode("UTF-8") # Shift all values by one since the first value is the ID
		device.VENDOR_ID 	= device_list[2].encode("UTF-8")
		device.PRODUCT		= device_list[3].encode("UTF-8")
		device.PRODUCT_ID	= device_list[4].encode("UTF-8")
		device.SERIAL		= device_list[5].encode("UTF-8")
		device.HASH			= device_list[6]
		device.PATH			= device_list[7]
		device.CONNECTED	= device_list[8]
		device.WHITELISTED	= device_list[9]
		device.TIMEOUT_DATE = device_list[10]
		return device

	# Merge a new connection of a device with it's prior stored one
	def merge_old_and_new_device(self, new, old, connected=True):

		# Copy everything from the old device into the new except the path
		new_path = new.get_path()
		new.__dict__ = {**new.__dict__, **old.__dict__}
		new.PATH = new_path()
		new.set_connected(connected) # Also set its connected state
		return new

	# Returns a list of rows from the table "Devices" which all contains the provided value in the provided column
	def select_devices(self, column_name, column_value):
		if not self.OPEN: return None
		self.CUR.execute("SELECT * FROM ? WHERE ? MATCH '?'", (self.TABLE_NAME, column_name, column_value))
		return self.CUR.fetchall()

	# Deletes a row from the table "Devices" which contains the provided value in the provided column
	# This does not commit!
	def delete_devices(self, column_name, column_value):
		if not self.OPEN: return
		self.CUR.execute("DELETE FROM ? WHERE ? = ?", (self.TABLE_NAME, column_name, column_value))

	# Inserts a list of provided values into the table "Devices"
	# This does not commit!
	def insert_values(self, column_values):
		if not self.OPEN: return
		self.CUR.execute("INSERT INTO ? VALUES (?)", (self.TABLE_NAME, column_values))
