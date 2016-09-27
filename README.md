# USBAuth
A USB device authentcation tool. When a USB device is plugged into the computer, a password verification prompts. If the password verification succeded, the port the USB device is plugged into will be verified, and communication will be permitted. If the password verification failed, the port will not be authenticated, and communication will continue to be blocked. To attempt a re-autentication, simply remove the USB device and connect it again.

## Dependencies
-   [Python (3.5.1+)](https://www.python.org/)
-   [Cryptography (1.2.3+)](https://pypi.python.org/pypi/cryptography)
-   [PyQt5 (5.5.1+)](https://pypi.python.org/pypi/PyQt5/5.6)
-   [Pyudev (0.16.1+)](https://pypi.python.org/pypi/pyudev)

## Installation
1.  Clone the project: `git clone https://github.com/osneven/usbauth.git`
2.  Change into the directory: `cd ./usbauth`
3.  Execute the installation script and follow the instrctions: `./install.sh`
4.  Clean up installtion folder: `cd ..`, `rm -r ./usbauth`
5.  Installation complete, start the daemon: `sudo /etc/usbauth/usbauth --start`

## Usage
For complete help and usage, run: `/etc/usbauth/usbauth --help`

## License
The complete project is licensed under the GNU GENERAL PUBLIC LICENSE version 3(GPL-3.0).
