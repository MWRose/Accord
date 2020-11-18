import os
import base64  
from socket import *
host = "192.168.86.249"
port = 8989
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.sendto(b"Hello, World!", addr)
UDPSock.close()
os._exit(0)