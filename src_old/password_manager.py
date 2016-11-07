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
from crypto import PasswordHandler, SaltHandler
from paths import Paths

# This class is for reading and writing the password to the disk
# This is class is not used for encrypting the password.
class PasswordManager:
	def __init__(self, logger):
		self.LOGGER = logger

	# Reads the password hash from the disk
	def read_password_hash(self):
		Paths.create_paths()
		try:
			with open(Paths.PASSWORD_FILE, "rb") as f:
				password_hash = f.read()
				f.close()
				return password_hash
		except FileNotFoundError:
			if self.LOGGER is not None:
				self.LOGGER.log("Password file doesn't exist")
			return None

	# Updates the password hash on the disk with a given cleartext password
	def update_password_hash(self, cleartext_password):

		# Generate the hash
		salt_handler = SaltHandler()
		password_handler = PasswordHandler(salt_handler, cleartext_password)
		key = password_handler.generate()

		# Write the hash to the file
		Paths.create_paths()
		with open(Paths.PASSWORD_FILE, "wb") as f:
			f.write(key)
			f.close()

		# Log feedback
		if self.LOGGER is not None:
			self.LOGGER.log("Password was updated")

	# Returns true if the given cleartext password equals the ciphertext password stored on the disk
	def verify_password_hash(self, cleartext_password):

		# Read the hash from the file
		with open(Paths.PASSWORD_FILE, "rb") as f:
			key = f.read()
			f.close()

		# Match the password's hash and hash in the file
		salt_handler = SaltHandler()
		password_handler = PasswordHandler(salt_handler, cleartext_password)
		match = password_handler.verify(key)

		# Return resutl
		return match
