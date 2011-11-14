#!/usr/bin/python

# RESTful API server example

# Much of this code thanks to docs.python.org/howto/sockets.html

# We need to make a sockets to make a basic HTTP server
import socket
# Used to get the IP address
import fcntl
import struct
# Used for processing HTTP requests. Needs to be installed (i.e. through pip).
# try to import C parser then fallback in pure python parser.
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser

def get_ip_address(ifname):
    '''
    Given an interface name (i.e. 'lo' or 'eth0') gives that interface's IP
    address. Credit to http://code.activestate.com/recipes/439094/
   
    Probably very specific to Linux, not portable code
    '''
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

################################
# Process received HTTP requests
################################

# User database, stored as [name, password, number logins] lists
users = []

def process_request(method, path, body):
    if method == 'GET':
        if path == '/users': 
            return str(users)
        elif path.startswith('/users'):
            return str([x for x in users if x[0] == path[len('/users/'):]])
        else:
            return 'Bad URL'
    elif method == 'POST':
        if path == '/users/new':
            name = body['name']
            password = body['password']
            if len([x for x in users if x[0] == name]) > 0:
                return "ERROR: User already exists"
            users.append([name, password, 0])
            return "User {0} successfully created.".format(name)
        elif path == '/users/changepassword':
            name = body['name']
            password = body['password']
            passwordnew = body['passwordnew']
            match_users = [x for x in users if x[0] == name]
            print match_users
            if len(match_users == 0):
                return "ERROR: No such user"
            user = match_users[0]
            if password != user[1]:
                return "ERROR: Bad password"
            user[1] = passwordnew
            return "User {0}'s password successfully changed.".format(name)
        elif path == '/users/login':
            name = body['name']
            password = body['password']
            match_users = [x for x in users if x[0] == name]
            if len(match_users == 0):
                return "ERROR: No such user"
            user = match_users[0]
            if password != user[1]:
                return "ERROR: Bad password"
            user[2] += 1
            return "User {0} successfully logged in. " + \
                "Login count: {1}".format(name, user[2])
        else:
            return 'Bad URL'
    elif method == 'DELETE':
        if path.startswith('/users'):
            name = body['name']
            password = body['password']
            match_users = [x for x in users if x[0] == name]
            if len(match_users == 0):
                return "ERROR: No such user"
            user = match_users[0]
            if password != user[1]:
                return "ERROR: Bad password"
            users.remove(user)
            return "User {0}'s successfully deleted.".format(name)
        else:
            return 'Bad URL'
    else:
        return 'Bad Method'

###################
# Main server loop
###################

response = '''HTTP/1.1 200 OK
Date: Sun, 13 Nov 2011 22:08:44 GMT
Content-Type: text/html; charset=UTF-8

'''

while True:
    (clientsocket, address) = serversocket.accept()
    parser = HttpParser()
    body = []
    while True:
        data = clientsocket.recv(1024)
        if not data:
            break
        
        recved = len(data)
        nparsed = parser.execute(data, recved)
        assert nparsed == recved

        if parser.is_headers_complete():
            print parser.get_method()
            print parser.get_path()
            print parser.get_headers()

        if parser.is_partial_body():
            body.append(parser.recv_body())

        if parser.is_message_complete():
            break
    
    print ''.join(body)
    print [x.split('=') for x in ''.join(body).split('&')]
    print dict([x.split('=') for x in ''.join(body).split('&') if len(x) == 2])

    result = process_request(parser.get_method(),
                             parser.get_path(),
                             dict([x.split('=') for x in ''.join(body).split('&') if len(x.split('=')) == 2]))
    result += '\n'
    clientsocket.send(response + str(result))
    print result

    clientsocket.close()
