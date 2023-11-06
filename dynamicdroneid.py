from __future__ import print_function
from pymavlink import mavutil
import socket

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
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_component))

# Initialize serial connection on UART2 to flight controller
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600, source_system=255)

# Wait for heartbeat
wait_heartbeat(master)
