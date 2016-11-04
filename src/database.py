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
from enum import Enum

#
# TODO: Make a sqlite, encrypted, database for storing information about previous USB devices.
#		This is how the structure should look:
#

class USBDatabase:

	def __init__(self):
		self.OPEN = False
		self.TABLE_NAME = "Devices"

################################################################################

	# Connects to the database file and decrypts it
	def open(self, cleartext_password):
		if self.OPEN: return
		self.CONN = lite.connect(Paths.DATABASE_FILE, detect_types=lite.PARSE_DECLTYPES)
		self.CUR = self.CONN.cursor()
		self.CUR.execute('PRAGMA key="{}"'.format(cleartext_password))
		self.CUR.execute('PRAGMA kdf_iter=100000')
		self.OPEN = True

	# Closes the database connection
	def close(self):
		if not self.OPEN: return
		self.CUR.close()
		self.CONN.commit()
		self.CONN.close()
		self.OPEN = False

	# Commits the database connection
	def commit(self):
		self.CONN.commit()

################################################################################

	# Handles the insertion of a USB device
	def insertion_of_device(self, device):
		if not self.OPEN: return
		self.ensure_table_exists()

		# Chek if the device is already stored in the database, there should not be any more than one
		match = self.select_devices(ColumnNames.HASH, device.get_hash())
		if match is not None and len(match) > 0: # There is a match

			# Merge the matched devices information into the new device and delete the match
			match = match[0]
			match_device = self.list_to_de	vice(match)
			device = self.merge_old_and_new_device(device, match_device)
			self.delete_devices(ColumnNames.ID, "'" + match[0] + "'")

		# Deauthenticate the device if it is not whitelisted
		if device.is_whitelisted(): device.authenticate()
		else: device.deauthenticate()

		# Insert the new device into the table
		device_values = self.device_to_list(device)
		self.insert_devicedevice(self, column_name, column_values)(device_values)
		self.commit()

	# Handles the removal of a USB device
	def removal_of_device(self, device):
		if not self.OPEN: return
		self.ensure_table_exists()

		# Check if the device is stored in the database, there should not be any more than one
		match = self.select_devices(ColumnNames.HASH, device.get_hash())
		if match is not None and len(match) > 0: # There is a match
			match[0].set_connected(False) 		 # Simply set its connected state to "False"
			self.commit()

################################################################################

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

################################################################################

	# An enum of all the columns names in the table "Devices"
	class ColumnNames(Enum):
		ID 				= "ID"
		VENDOR			= "VENDOR"
		VENDOR_ID		= "VENDOR_ID"
		PRODUCT			= "PRODUCT"
		PRODUCT_ID		= "PRODUCT_ID"
		SERIAL			= "SERIAL"
		HASH			= "HASH"
		PATH			= "PATH"
		CONNECTED		= "CONNECTED"
		WHITELISTED		= "WHITELISTED"
		TIMEOUT_DATE	= "TIMEOUT_DATE"

	# Creates the "Devices" table if it doesn't already exist
	def ensure_table_exists(self):
		if not self.OPEN: return
		columns = "\
		{} 	INT 	AUTOINCREMENT,\
		{}	TEXT	NOT NULL,\
		{}	TEXT	NOT NULL,\
		{}	TEXT	NOT NULL,\
		{} 	TEXT	NOT NULL,\
		{} 	TEXT	NOT NULL,\
		{}	BLOB	NOT NULL,\
		{}	TEXT	NOT NULL,\
		{}	BOLLEAN	NOT NULL,\
		{}	BOOLEAN	NOT NULL,\
		{}	TIMESTAMP,\
		".format(ColumnNames.ID,
			ColumnNames.VENDOR,
			ColumnNames.VENDOR_ID,
			ColumnNames.PRODUCT,
			ColumnNames.PRODUCT_ID,
			ColumnNames.SERIAL,
			ColumnNames.HASH,
			ColumnNames.PATH,
			ColumnNames.CONNECTED,
			ColumnNames.WHITELISTED,
			ColumnNames.TIMEOUT_DATE)
		self.CUR.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(self.TABLE_NAME, columns))

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
	def insert_device(self, column_values):
		if not self.OPEN: return
		self.CUR.execute("INSERT INTO ? VALUES (?)", (self.TABLE_NAME, column_values))

	# Updates a device which has the provided match value in the provided match column, with the new provided insert values in the provided insert columns
	# This does not commit!
	def update_device(self, match_column_name, match_column_values, insert_column_names, insert_column_values):
		if not self.OPEN or len(insert_column_names) == len(insert_column_values): return
		s = []
		[s.append("{} = '{}', ".format(c, insert_column_values[i])) for i,c in enumerate(insert_column_names)]
		s = "".join(s)[:-2]
		self.CUR.execute("UPDATE ? SET ? WHERE ? = '?'")
