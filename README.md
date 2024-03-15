# DynamicDroneID

## Description
This application retrieves the hostID (typically the last 8 bits) of the local IP address of a Linux machine. It then establishes a connection over USB to an Ardupilot flight controller and sets the SYSID_THISMAV parameter to the same value as the retrieved hostID. In doing so, the flight controller:
* avoids conflicts with other Mavlink devices on the network which may initially share the same system ID
* no longer requires that a user manually assign a sysID before adding a drone to a network
* inherits many of the features offered by TCP/IP
* has reduced constraints regarding the number of Mavlink components that can exist simultaneously on a single network (thanks to IP subnetting)

## Hardware
Designed to be run on a Raspberry Pi CM4 module + COMRAD v2b carrier board.
Docker container available to allow deployment on other CPU architectures and operating systems.
Tested using Cube Orange, ArduPlane 4.4.1 and later.

## Future revisions
- Retry the entire process if an error occurs.
- Limit number of retries to a predefined value

## Version 1.0
- Handles all common exceptions
- After assigning the SysID, the program reboots the flight controller, re-establishes  connection, and verifies whether  parameter has been set. Results of  verification are shown as console messages.
- Refactored much of the code into reusable functions for future expansion.
