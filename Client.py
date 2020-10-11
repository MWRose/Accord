import sys
import socket
import threading
from pyfiglet import Figlet

# Argument: IP address, port number
# Can run this multiple times for multiple different users
class Client:
    def __init__(self):
        # Print Accord client side messages
        f = Figlet(font="smslant")
        print (f.renderText("Welcome to ACCORD"))
        print ("Chat away!")

        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Get command line arguments and check correctness
            args = sys.argv
            if len(args) != 3:
                print("correct usage: python3 Server.py <server name> <port>")
                # TODO: Maybe make this quit?

            server_name = args[1]
            server_port = int(args[2])

            self.s.connect((server_name, server_port))
        except:
            print("Couldn't connect to server, please type in valid host name and port.")
            # TODO: Maybe make this quit?

        self.username = input("Enter username: ")
        self.s.send(self.username.encode())

        self.recipient_established = False
        
        # Handles threading of sending and receiving messages for a client
        send_handler = threading.Thread(target=self.handle_send, args=())
        send_handler.start()

        receive_handler = threading.Thread(target=self.handle_receive,args=())
        receive_handler.start()

    def handle_send(self):
        while True:
            if (self.recipient_established == False): 
                # If user inputs a correct username, will start chat with them
                # TODO: Better user logic here
                msg = input("Who would you like to start chatting with? ")
                self.s.send(msg.encode())
                self.recipient_established = True
            else:
                self.s.send((self.username + " - "+ input("Message: ")).encode())   

    def handle_receive(self):
        while True:
            print(self.s.recv(1204).decode())      

client = Client()