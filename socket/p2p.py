import threading
import socket

server = socket.socket()
client = socket.socket()
port = 40674
print("Enter IP for connection")
PEER_IP = input()
PEER_ADD = 0

def listenConnect():
    server.bind(('',port))
    print(f"Server binding to {port}")
    server.listen(5)
    print("Server listening")

    while True:
        PEER_ADD = server.accept()
        print(f"Connection from {PEER_ADD}")
        if PEER_ADD != 0:
            client.connect(PEER_ADD)
        print("Connected client and server")
        

def receiveServer():
    while True:
        msg = client.recv(1024)
        print(msg)
        if msg == "end":
            break




server.close()