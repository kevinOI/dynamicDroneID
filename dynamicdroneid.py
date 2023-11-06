from __future__ import print_function
from pymavlink import mavutil
import socket
import os

droneid = 0 # Initialize variable to store droneID that will be retrieved later
dronecomponent = 0 # Intiialize variable to store droneComponent to 0

# Function to retrieve local IP address as string
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
str = get_ip_address() # Retrieve local IP address
str = str.split('.') # Subdivide into groups delimited by '.'
newid = str[3] # Save last three digits as 'newid'

# Function to wait for heartbeat packets and report back sysid
def wait_heartbeat(m):
    '''wait for heartbeat so we know target system IDs'''
    print("Waiting for APM heartbeat")
    msg = m.recv_match(type='HEARTBEAT', blocking=True)
    droneid = m.target_system # Store droneid
    dronecomponent = m.target_component # Store component

# Grant read/write access to USB device.
print("Making USB devices accesible...")
os.system('sudo chmod a+rw /dev/ttyACM0')

# Initialize USB connection to flight controller
print("Connecting to the flight controller...")
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600, source_system=255)

# Wait for heartbeat
wait_heartbeat(master)
print("Heartbeat received! The drone is connected.")

# Compare the drone's ID to the IP-based value
if master.target_system != newid: 
    # Set droneID to newid
    print("Setting droneID of drone ", master.target_system)
    master.mav.param_set_send(
            master.target_system,
            master.target_component,
            b'SYSID_THISMAV',
            157,
            mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )
    print("Writing parameters to EEPROM...")
    master.mav.command_long_send(
            droneid,
            master.target_component,
            mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE,
            1,0,0,0,0,0,0,0
    )
    print("Rebooting drone...")
    master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,
            0,1,0,0,0,0,0,0
    )
    master.close()
else:
    print("DroneID is already set. Shutting down.")
