import sys
import socket
import threading
from pyfiglet import Figlet
import Requests

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
            server_name = args[1]
            server_port = int(args[2])

            self.s.connect((server_name, server_port))
        except:
            print("Couldn't connect to server, please type in valid host name and port.")
            sys.exit(0)

        self.username = input("Enter username: ")
        self.s.send(Requests.login(self.username))

        self.recipient = None
        
        # Handles threading of sending and receiving messages for a client
        send_handler = threading.Thread(target=self.handle_send, args=())
        send_handler.start()

        receive_handler = threading.Thread(target=self.handle_receive,args=())
        receive_handler.start()

    def handle_send(self):
        while True:
            if not self.recipient: 
                # If user inputs a correct username, will start chat with them
                # TODO: Better user logic here
                msg = input("Who would you like to start chatting with? ")
                self.s.send(Requests.initiate_chat(self.username, msg))
                self.recipient = msg
            else:
                msg = input("Message: ")
                self.s.send(Requests.message(self.username, self.recipient, msg))   

    def handle_receive(self):
        while True:
            data = self.s.recv(1204)
            request = Requests.parse_request(data)
            if request.is_message():
                print(request.data["sender"] + ": " + request.data["message"]) 
            elif request.is_broadcast():
                print(request.data["message"]) 

client = Client()