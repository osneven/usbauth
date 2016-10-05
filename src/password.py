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
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from sys import argv
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QInputDialog, QLineEdit
from paths import get_password_file_path, get_whitelist_file_path
import jsonpickle

# Verifies a password entered through the GUI with the one saved on disk
# Give a description of the device to authenticate
# Returns true if passwords match, false is they do not, or if the operation was canceled
def verify_gui(desc):
	clear_verify = gverify(desc)
	if clear_verify is not False:
		return verify(clear_verify.encode("UTF-8"))
	else: return False

# Verifies the password saved on disk
def verify(clear_verify_bytes):

	# Get SHA512 of the verification password
	digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
	digest.update(clear_verify_bytes)
	cipher_verify = digest.finalize()

	# Read the SHA512 of the password saved on the disk
	cipher_password = None
	try:
		with open(get_password_file_path(), "rb") as file:
			cipher_password = file.read()
			file.close()
	except FileNotFoundError:
		gerror("No password file found!")
		return False

	# Return result
	return cipher_verify == cipher_password

# Updates the password saved on disk with a new one entered through the GUI
# NOTE: This function calls update() which requires root!
def update_gui():
	clear_password = gupdate()
	if clear_password is not False:
		return update(clear_password.encode("UTF-8"))
	else: return False

# Updates the password saved on disk
# NOTE: Requires root permissions!
def update(clear_password_bytes):

	# Get SHA512 of the password
	digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
	digest.update(clear_password_bytes)
	cipher_password = digest.finalize()

	# Write the SHA512 of the password to the disk
	# NOTE: This operation requires root permissions
	try:
		with open(get_password_file_path(), "wb") as file:
			file.write(cipher_password)
			file.close()
			return True
	except PermissionError:
		gerror("Root permissions required to change USB authentication password!")
		return False

# Verifies that the specified USB device is whitelisted
def whitelist_verify(dev_path):

	# Get the identifying hash of the USB device
	identifying_hash = whitelist_identify(dev_path)

	# Check that the hash is inside the whitelist file
	try:
		with open(get_whitelist_file_path(), "rb") as f:
			wl = jsonpickle.decode(f.read().decode("UTF-8"))
			f.close()
		return identifying_hash in wl
	except FileNotFoundError or TypeError:
		with open(get_whitelist_file_path(), "wb") as f:
			f.write(jsonpickle.encode([]).encode("UTF-8"))
			f.close()

# Whitelists a USB device if user clicks yes on the GUI
# NOTE: This function calls whitelist() which requires root!
def whitelist_update_gui(dev_path):
	if gwhitelist_update(dev_path):
		whitelist_update(dev_path)
		return True
	return False

# Whitelists a USB device
# NOTE: Requires root permissions!
def whitelist_update(dev_path):

		# Get the identifying hash of the USB device
		identifying_hash = whitelist_identify(dev_path)

		# Add the hash to to the json whitelist file
		try:
			# Read all the other whitelist entries
			with open(get_whitelist_file_path(), "rb") as f:
				wl = jsonpickle.decode(f.read().decode("UTF-8"))
				f.close()

			# Write them back to the file in addition to the new entry
			with open(get_whitelist_file_path(), "wb") as f:
				wl.append(identifying_hash)
				f.write(jsonpickle.encode(wl).encode("UTF-8"))
				f.close()
		except PermissionError:
			gerror("Root permissions required to whitelist USB device!")

		# Whitelist file doesn't exist, create it and redo this function
		except FileNotFoundError:
			with open(get_whitelist_file_path(), "wb") as f:
				f.write(jsonpickle.encode([]).encode("UTF-8"))
				f.close()
			whitelist(dev_path)

# Returns the identifying hash for a specific USB device
def whitelist_identify(dev_path):
	# Initialize SHA512 digest for the identifying data
	digest = hashes.Hash(hashes.SHA512(), backend=default_backend())

	# Identify the USB device using the following files
	identifying_files = ["idProduct", "idVendor", "manufacturer", "product", "serial"]

	# Read the data from each file
	for id_file in identifying_files:
		try:
			with open(dev_path + id_file, "rb") as f:
				digest.update(f.read())
				f.close()
		except:
			continue

	# Finalize the identifying hash and return it
	return digest.finalize()

# QT gui pup functions
# Creates an error window
def gerror(message):
	a = QApplication(argv)
	QMessageBox.warning(QWidget(), "ERROR", message, QMessageBox.Ok)

# Creates a password verification window, return cleartext password or none if window was canceled
def gverify(message):
	a = QApplication(argv)
	q = QInputDialog()
	q.setWindowTitle("USB Authentication")
	q.setLabelText("Provide your USB authentication password.\nDevice pending for authentication:\n" + message)
	q.setTextEchoMode(QLineEdit.Password)
	q.show()
	a.exec()
	t = q.textValue()
	if t == "": t = False
	return t

# Creates a password update field, returns the cleartext password or none if window was canceled
def gupdate():
	clear_verify = clear_password = None
	a = QApplication(argv)
	while clear_password is None or clear_password != clear_verify:
		q0 = QInputDialog()
		q0.setWindowTitle("USB Authentication Update")
		q0.setLabelText("Provide a new USB authentication password.")
		q0.setTextEchoMode(QLineEdit.Password)
		q0.show()
		a.exec()
		clear_password = q0.textValue()
		q1 = QInputDialog()
		q1.setWindowTitle("USB Authentication Update")
		q1.setLabelText("Verify your new USB authentication password.")
		q1.setTextEchoMode(QLineEdit.Password)
		q1.show()
		a.exec()
		clear_verify = q1.textValue()
	if clear_password is "": clear_password = False
	return clear_password

# Creates a whitelist request field, returns true if the users clicks yes, and false if otherwise
def gwhitelist_update(desc):
	a = QApplication(argv)
	result = QMessageBox.question(QWidget(), "Whitelist Device", "Do you wish to whitelist the following USB device?\n" + desc, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
	return result == QMessageBox.Yes
