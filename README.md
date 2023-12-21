# DynamicID

## Description
This application retrieves the last three digits of the local IP address of whatever single board computer it runs on. It then establishes a connection over USB to an Ardupilot flight controller and sets the SYSID_THISMAV parameter to those three digits. This allows the flight controller to avoid conflicts with others on the network which may originally share the same system ID.

## Hardware
DynamicID was developed to be run on a Raspberry Pi CM4 module, but using Docker, should be easily portable to any other Linux-based system on a Debian base image.
The flight controller assumed is the Cube Orange, running ArduCopter or ArduPlane V4.4.1 or later. This will likely work on earlier firmware versions, but has not been tested to do so.

## Future revisions
- Retry the entire process if an exception occurs anywhere.
- Limit number of retries to a set value

## Version 1.0
- Added exception handling for all common exceptions
- After assigning the SysID, the program reboots the flight controller, re-establishes the connection, and verifies whether the parameter has been set. The results of this verification are shown as console messages.
- Refactored much of the code into reusable functions for future expansion.