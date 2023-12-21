from __future__ import print_function
from pymavlink import mavutil
import socket
import os
import time

droneid = 0 # Initialize variable to store droneID that will be retrieved later
dronecomponent = 0 # Intiialize variable to store droneComponent to 0

# Function to retrieve local IP address as string
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# Function to wait for heartbeat packets and report back sysid
def wait_heartbeat(m):
    '''Wait for heartbeat from connected drone and store droneID and componentID.'''
    print("Waiting for heartbeat")
    msg = m.recv_match(type='HEARTBEAT', blocking=True)
    droneid = m.target_system # Store droneid
    dronecomponent = m.target_component # Store component

# Instruct the flight controllers to save parameters to persistent memory
def write_params():
    print("Writing parameters to EEPROM...")
    master.mav.command_long_send(
         droneid,
         master.target_component,
         mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE,
         1,0,0,0,0,0,0,0
    )

# Instruct the flight controller to reboot, applying changes
def reboot_drone():
    print("Rebooting drone...")
    master.mav.command_long_send(
         master.target_system,
         master.target_component,
         mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,
         0,1,0,0,0,0,0,0
    )

# Set the flight controller's system ID to the provided argument
def set_sysid(id):
    master.mav.param_set_send(
        master.target_system,
        master.target_component,
        b'SYSID_THISMAV',
        id,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )

#################################### Start of program ########################################
### Retrieve local IP address and process
print("\n\n############################ IP RETRIEVAL ################################")
try:
	time.sleep(1)
	print("Obtaining local IP address...")
	str = get_ip_address()
	time.sleep(0.5)
	print("Splitting into groups delimited by '.'")
	str = str.split('.')
	time.sleep(0.5)
	newid = int(str[3])
	print(f'The last three digits of the local IP address are: {newid}\n\n')
	time.sleep(0.5)
except RuntimeError:
	print("ERROR: The local network is unreachable or improperly configured.")

print("#################### CONNECT TO FLIGHT CONTROLLER #########################")
time.sleep(1)
### Grant read/write access to USB device.
print("Making USB devices accessible...")
usbAccess = os.system('sudo chmod a+rw /dev/ttyACM0')
if usbAccess != 0:
	print("ERROR: The USB device was not found.")
	exit(-1)
print("Success.")
time.sleep(0.5)

### Initialize USB connection to flight controller
print("Connecting to the flight controller...")
try:
	master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600, source_system=255)
except RuntimeError:
	print("ERROR: USB port could not be opened.")
	exit(-1)

### Wait for heartbeat
try:
	wait_heartbeat(master)
except RuntimeError:
	print("ERROR: No heartbeat was detected.")

print("Heartbeat message received; flight controller  is CONNECTED.\n\n")
time.sleep(1)

print("########################## CONFIGURE SYSID ################################")
if master.target_system != newid: 
    # Set droneID to newid
    print(f"Current sysID: {master.target_system}")
    time.sleep(0.5)
    print(f"Setting sysID to: {newid}")
    set_sysid(newid)
    time.sleep(0.5)
    write_params()
    time.sleep(0.5)
    reboot_drone()
    time.sleep(0.5)
    print("Closing connection to flight controller...")
    master.close()
    time.sleep(1)
    print(f"SUCCESS: Drone ID has been set to {newid} and parameters have been saved.\n\n")
else:
    print("DroneID is already set. Shutting down...\n\n")
    exit()

print("######################## VERIFICATION OF ID ###############################")

### Initialize USB connection to flight controller
print("Connecting to the flight controller...")
try:
	master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600, source_system=255)
except RuntimeError:
	print("ERROR: USB port could not be opened.")
	exit(-1)

### Wait for heartbeat
try:
	wait_heartbeat(master)
except RuntimeError:
	print("ERROR: No heartbeat was detected.")

print("Heartbeat message received; flight controller  is CONNECTED.\n\n")
time.sleep(1)

if master.target_system == newid:
	print(f'CONFIRMED: ID has been set to {master.target_system}')
else:
	print(f'FAILED: The ID has not been set to {newid} and is instead {master.target_system}')

master.close()
print("Closing...")
exit()
