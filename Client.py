import sys
import socket
import threading

# Argument: IP address, port number
# Can run this multiple times for multiple different users
class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        
        try:
            # Get command line arguments and check correctness
            args = sys.argv
            if len(args != 2):
                print("correct usage: python3 Server.py <server name> <port>")
            server_name = args[1]
            server_port = int(args[2])

            # server_name = input("Enter host server's IP address: ")
            # server_port = int(input("Enter host server port number: "))

            self.s.connect((server_name, server_port))
            
        except:
            print("Couldn't connect to server, please type in valid host name and port.")

        self.username = input("Enter username: ")
        self.s.send(self.username.encode())
        
        # Handles threading of sending and receiving messages for a client
        send_handler = threading.Thread(target=self.handle_send, args=())
        send_handler.start()

        receive_handler = threading.Thread(target=self.handle_receive,args=())
        receive_handler.start()

    def handle_send(self):
        while True:
            print(self.s.recv(1204).decode())

    def handle_receive(self):
        while True:
            self.s.send((self.username+' - '+input()).encode())

client = Client()