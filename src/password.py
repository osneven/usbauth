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
from paths import UNIX_PATHS

# Handle password updating and verification on the system part
class Password:

	# Verifies a password entered through the GUI with the one saved on disk
	# Give a description of the device to authenticate
	# Returns true if passwords match, false is they do not, or if the operation was canceled
	def verify_gui(self, desc):
		clear_verify = PasswordGUI().verify(desc)
		if clear_verify is not False:
			return self.verify(clear_verify.encode("UTF-8"))
		else: return False

	# Verifies the password saved on disk
	def verify(self, clear_verify_bytes):

		# Get SHA512 of the verification password
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(clear_verify_bytes)
		cipher_verify = digest.finalize()

		# Read the SHA512 of the password saved on the disk
		cipher_password = None
		try:
			with open(UNIX_PATHS.get_password_file_path(), "rb") as file:
				cipher_password = file.read()
				file.close()
		except FileNotFoundError:
			PasswordGUI().error("No password file found!")
			return False

		# Return result
		return cipher_verify == cipher_password

	# Updates the password saved on disk with a new one entered through the GUI
	# NOTE: This function calls update() which requires root!
	def update_gui(self):
		clear_password = PasswordGUI().update()
		if clear_password is not False:
			return self.update(clear_password.encode("UTF-8"))
		else: return False


	# Updates the password saved on disk
	# NOTE: Requires root permissions!
	def update(self, clear_password_bytes):

		# Get SHA512 of the password
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(clear_password_bytes)
		cipher_password = digest.finalize()

		# Write the SHA512 of the password to the disk
		# NOTE: This operation requires root permissions
		try:
			with open(UNIX_PATHS.get_password_file_path(), "wb") as file:
				file.write(cipher_password)
				file.close()
				return True
		except PermissionError:
			PasswordGUI().error("Root permissions required to change USB authentication password!")
			return False

# Handle GUI pass through of information to system password updating and verification
class PasswordGUI:

	# Creates an error window
	def error(self, message):
		a = QApplication(sys.argv)
		QMessageBox.warning(QWidget(), "ERROR", message, QMessageBox.Ok)

	# Creates a password verification window, return cleartext password or none if window was canceled
	def verify(self, message):
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
	def update(self):
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

	# Extract data from two line inputs if they are not none
	# Also if both line inputs are given, the text value is only returned if they are equal
	def extract_input(self, password=None, verify=None):
		if verify is not None:
			if password is not None:
				if password.text() == verify.text(): return password.text()
				else: return False
			else: return verify.text()