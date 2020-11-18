import os
from socket import *
host = "192.168.86.249"
port = 8989
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print("Waiting to receive messages...")
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print(data)
UDPSock.close()
os._exit(0)