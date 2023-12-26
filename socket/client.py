# Import socket module
import socket

# Final Variables
SERVER_ADD = '192.168.0.67'

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 40674

# connect to the server on local computer
s.connect((SERVER_ADD, port))

# receive data from the server
print(s.recv(1024))

# close the connection
s.close()
