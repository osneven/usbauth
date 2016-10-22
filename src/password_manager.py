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
from paths import Paths

# A class used for updating and reading the password used for all USB device authentications
class PasswordManager:
	def __init__(self, logger):
		global LOGGER
		LOGGER = logger

	# Reads the password hash from the disk
	def read_password_hash(self):
		Paths.create_paths()
		try:
			with open(Paths.PASSWORD_FILE, "rb") as f:
				password_hash = f.read()
				f.close()
				return password_hash
		except FileNotFoundError:
			if LOGGER is not None:
				LOGGER.log("Password file doesn't exist")
			return None

	# Updates the password hash on the disk with a given cleartext password
	def update_password_hash(self, cleartext_password):
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(cleartext_password.encode("UTF-8"))
		Paths.create_paths()
		with open(Paths.PASSWORD_FILE, "wb") as f:
			f.write(digest.finalize())
			f.close()
		if LOGGER is not None:
			LOGGER.log("Password was updated")

	# Returns true if the given cleartext password equals the ciphertext password stored on the disk
	def verify_password_hash(self, cleartext_password):
		digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
		digest.update(cleartext_password.encode("UTF-8"))
		with open(Paths.PASSWORD_FILE, "rb") as f:
			match = f.read() == digest.finalize()
			f.close()
			return match
