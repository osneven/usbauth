from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
from easygui import *

class Password:

	# Verifies a password entered through the GUI with the one saved on disk
	# Give a description of the device to authenticate
	# Returns true if passwords match, false is they do not, or if the operation was canceled
	def verify_gui(self, desc):
		clear_verify = PasswordGUI().verify("Please enter your USB authentication password.\nDevice pending for authentication:\n" + desc)
		if clear_verify is not None:
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
			with open("/etc/usbauth/passwd", "rb") as file:
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
		if clear_password is not None:
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
			with open("/etc/usbauth/passwd", "wb") as file:
				file.write(cipher_password)
				file.close()
				return True
		except PermissionError:
			PasswordGUI().error("Root permissions required to change USB authentication password!")
			return False

class PasswordGUI:

	# Creates an error window
	def error(self, message):
		msgbox("ERROR: " + message, "USB authentication error")

	# Creates a password verification window, return cleartext password or none if window was canceled
	def verify(self, message):
		try:
			return multpasswordbox(message, "Authenticate USB device", ["Password"])[0]
		except: return None

	# Creates a password update field, returns the cleartext password or none if window was canceled
	def update(self):
		title = "Update USB authentication password"
		clear_verify = clear_password = None
		try:
			while clear_password is None or clear_password != clear_verify:
				clear_password = multpasswordbox("Please enter a new USB authentication password.", title, ["New password"])[0]
				clear_verify = multpasswordbox("Please verify your new password.", title, ["Verify password"])[0]
			return clear_password
		except: return None