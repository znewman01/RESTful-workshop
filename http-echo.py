#!/usr/bin/python

# Much of this code thanks to docs.python.org/howto/sockets.html

# We need to make a sockets to make a basic HTTP server
import socket
# Used to get the IP address
import fcntl
import struct

def get_ip_address(ifname):
    """
    Given an interface name (i.e. 'lo' or 'eth0') gives that interface's IP
    address. Credit to http://code.activestate.com/recipes/439094/
   
    Probably very specific to Linux, not portable code
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

################
# Set up server
################

# INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# Bind to the local hostname on a port that probably isn't being used
#serversocket.bind((socket.gethostname(), 3000))
serversocket.bind((get_ip_address('eth1'), 3000))

# Start listening
serversocket.listen(5)

###################
# Main server loop
###################

response = """HTTP/1.1 200 OK
Date: Sun, 13 Nov 2011 22:08:44 GMT
Content-Type: text/html; charset=UTF-8

<html>some content</html>
"""

while 1:
    (clientsocket, address) = serversocket.accept()
    msg = clientsocket.recv(4096)
    clientsocket.send(response)
    clientsocket.close()
    print msg
