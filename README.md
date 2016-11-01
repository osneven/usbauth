# USBAuth
A USB device authentication tool. When a USB device is plugged into the computer, it automatically gets blocked by the listener running in the background. A command can then be issued from a terminal to authenticate that device by entering a password. You have the ability to then again deauthenticate the device when it's no longer needed. If you're using a single USB device often, you can add it to a white list, so you don't have to enter you password every time it inserted.
**NOTE: Much of this is still in development.**

## Dependencies
-	[Python (3.5.1+)](https://www.python.org/)
-	[Cryptography (1.2.3+)](https://pypi.python.org/pypi/cryptography)
-	[PyQt5 (5.5.1+)](https://pypi.python.org/pypi/PyQt5/5.6)
-	[Pyudev (0.16.1+)](https://pypi.python.org/pypi/pyudev)

## Installation
1.	Clone the project: `git clone https://github.com/osneven/usbauth.git`
2.	Change into the directory: `cd ./usbauth`
3.	Execute the setup script and follow the instructions: `./setup.sh`
4.	Cleanup the setup folder folder: `cd ..`, `rm -r ./usbauth`
5.	Setup complete, start the listener: `sudo usbauth --start`

## Usage
### General usage
This is a general overview of USBAuth's command line interface.
-	`--help` or `-h` shows the help menu.
-	`--start` starts the listener.
-	`--stop` stops the listener.
-	`--list` or `-l` will list all USB devices the listener have stored in the database.
-	`--auth ID` or `-a ID` will prompt for authentication of the USB device with that ID.
-	`--deauth ID` or `-d ID` will prompt for deauthentication of the USB device with that ID.
-	`--whitelist ID` or `-w ID` will prompt for adding/removing the USB device with that ID to the white list.
-	`--password` or `-p` will prompt for an updation of the USB authentication password.
-	`--quiet` or `-q` when called with `--start` will tell it not to print any feedback messages to the screen.

### Starting and stopping
USBAuth is split into two main parts, the listener and the command issuer. The listener is supposed to be run in the background, while the command issuer can be accessed any time through the command line. The listener can be started like this:
```
# usbauth --start
```
The listener needs to be run with root privileges, since deauthentication of USB devices on Linux systems is done by accessing the `/sys/bus/usb/devices/` folder. Staring the listener like this will not run it in the background, and it will begin to log feedback messages to the screen. If you want to background the listener, you can do so by the writing this line instead:
```
# usbauth --start --quiet &
```
This will simply start the listener in 	quiet mode by adding `--quiet`, and by trailing the command with a `&`, the command gets backgrounded. Every time the listener is started, it's PID is written to a file that is read when it's ordered to stop. To stop the listener, simple use the next command:
```
# usbauth --stop
```
All the feedback the listener will have provided while it was running, will have continuously been written to a log file located in inside the `/opt/usbauth/logs/` directory.

### Authentication and deauthentication
The most important part of USBAuth is the (de)authentication of USB devices. This can be done through the CLI, which (de)authenticates a device from a selected ID. The IDs of all the currently connected USB devices can be done so:
```
# usbauth --list
```
This prints some identifying information about the USB devices, the ID is presented as the fist number in each row, surrounded by square brackets. When the correct ID is selected, you can authenticate it by typing:
```
# usbauth --auth ID
```
*Replace `ID` with your selected ID. Note, the ID of a particularly USB device may change when inserting or removing other devices.*

When you are done with using the USB device, you deauthenticate it by either removing it from the computer or running the following command.
```
# usbauth --deauth ID
```
*Replace `ID` with your selected ID.*

When (de)authenticating a USB device, you will be prompted for some confirmation. Authentication will require the authentication password to be entered, and deauthentication will require a simple yes or no confirmation.

If your continuously inserting and removing the same USB device, and don't want to enter the authentication password every time, you can add it to the white list. To white list the device, use the following command:
```
# usbauth --whitelist ID
```
*Replace `ID` with your selected ID.*

This will white list the USB device with the selected ID, but before it will do anything, it will prompt for a yes or no confirmation. There is no need the for the authentication password, since the device would already have been authenticated first. When choosing to authenticate the USB device, you will also be prompted for a timeout value. If you wish for the white listing to last on till its removed from the white list, simple type in a value of `0`. Otherwise type in any timespan presided by the unit's symbol. The unit can either be seconds (s), minutes (m) or hours (h). As an example, this value should be `10m` for a white list of ten minutes.

### Password updation
The authentication password is selected on install, but if you wish to change the password later use this command:
```
# usbauth --password
```
This will prompt for a new password, it will not ask for the old password. Reason for this is that the password's hash is stored in a file only one with root permissions can change. Since you need to run the above command with root permissions, you could easily just manually configure the password file with out knowing the content of said file.

## License
The complete project is licensed under the GNU GENERAL PUBLIC LICENSE version 3(GPL-3.0).
