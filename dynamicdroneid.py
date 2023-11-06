from __future__ import print_function
from pymavlink import mavutil

import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
str = get_ip_address()
str = str.split('.')
newid = str[3]
print(newid)
