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

def write_params():
    print("Writing parameters to EEPROM...")
    master.mav.command_long_send(
         droneid,
         master.target_component,
         mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE,
         1,0,0,0,0,0,0,0
    )

def reboot_drone():
    print("Rebooting drone...")
    master.mav.command_long_send(
         master.target_system,
         master.target_component,
         mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,
         0,1,0,0,0,0,0,0
    )

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
print("\n\n########################## IP RETRIEVAL ##############################")
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

print("##################### CONNECT TO FLIGHT CONTROLLER #########################")
time.sleep(1)
### Grant read/write access to USB device.
print("Making USB devices accessible...")
os.system('sudo chmod a+rw /dev/ttyACM0')
print("Success.")
time.sleep(0.5)

### Initialize USB connection to flight controller
print("Connecting to the flight controller...")
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600, source_system=255)

### Wait for heartbeat
wait_heartbeat(master)
print("Heartbeat message received; flight controller  is CONNECTED.\n\n")
time.sleep(1)

# TESTING better way to retrieve existing droneid
#master.mav.param_request_read_send(
#        master.target_system,
#        master.target_component,
#        b'SYSID_THISMAV',
#        -1
#)

#while True:
#    try:
#        message = master.recv_match(type='SYSID_THISMAV', blocking=True)
#        if message is not None and message.param_id.decode('utf-8') == 'SYSID_THISMAV':
#            print(f"Parameter: {message.param_id}, value: {message.param_value}")
#            break
#    except Exception as e:
#        print(f"Error: {e}")
#        break

# Compare the drone's ID to the IP-based value
print("######################## CONFIGURE SYSID ###############################")
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
    print(f"SUCCESS: Drone ID has been set to {newid} and parameters have been saved.")
else:
    print("DroneID is already set. Shutting down...")
