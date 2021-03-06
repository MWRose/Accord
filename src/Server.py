import sys
import socket
import threading
from pyfiglet import Figlet
import Requests
import Database


class Server:
    """
    Arguments: port number
    Must run this before starting Client
    """

    def __init__(self):
        # Print Accord server side messages
        f = Figlet(font="smslant")
        print(f.renderText("Welcome to ACCORD"))
        print("Server side")

        # Initalize clients dictionary
        self.clients = dict()

        # Initalize the socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Initialize the databases
        self.is_database_logs_init = False
        self.is_database_user_init = False
        self.start_server()

    def start_server(self):
        server_name = socket.gethostbyname(socket.gethostname())

        # Get command line arguments and check correctness
        args = sys.argv
        if len(args) != 2:
            print("correct usage: python3 Server.py <port>")
        server_port = int(args[1])

        self.s.bind((server_name, server_port))
        self.s.listen(100)

        print("Running on host: " + str(server_name))
        print("Running on port: " + str(server_port))

        while True:
            print("In while loop on the server")
            c, addr = self.s.accept()
            data = c.recv(4096)
            request = Requests.parse_request(data)
            print(request.data)
            if len(request.data) == 0:
                print("There was in issue with the received data. Received the following raw data: ", data)
            elif request.is_establish_connection():
                threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg):
        for connection in self.clients.values():
            connection.send(Requests.broadcast(msg))

    def create_new_account(self, c, data):
        username = data["username"]
        public_key = data["public_key"]
        ca_signature = data["signature"]

        if not Database.check_user(username):
            Database.add_user_info(username, public_key, ca_signature)
            request = Requests.account_created()
            c.send(request)
        else:
            request = Requests.account_not_created()
            c.send(request)
            print("Could not create an account. The provided username is taken.")

    def handle_client(self, c, addr):
        while True:
            try:
                data = c.recv(4096)
            except:
                c.shutdown(socket.SHUT_RDWR)
                break

            self.handle_recipient(data, c)

    def handle_recipient(self, data, c):
        request = Requests.parse_request(data)
        print(request.data)
        if len(request.data) == 0:
            print("There was in issue with the received data. Received the following raw data: ", data)
        if request.is_create_new_account():
            self.create_new_account(c, request.data)
        if request.is_login():
            username = request.data["username"]
            print("New connection. Username: " + str(username))
            self.broadcast(username + " has entered the chat.")
            self.clients[username] = c
        if request.is_logout():
            username = request.data["username"]
            print("Ended connection with " + str(username))
            del self.clients[username]
        if request.is_initiate_direct_message():
            # Initiate new chat between 2 connections
            recipient = request.data["recipient"]
            sender = request.data["requester"]
            if recipient in self.clients:
                self.clients[recipient].send(data)
        elif request.is_initiate_group_chat():
            recipient = request.data["recipient"]
            sender = request.data["requester"]
            # Skip sending back the handshake to the original sender in the group
            # message handshake 
            if recipient in self.clients and not (sender == recipient):
                self.clients[recipient].send(data)
        # Existing direct message
        elif request.is_direct_message():
            recipient = request.data["recipient"]
            if recipient in self.clients:
                self.clients[recipient].send(data)
        # Existing group message
        elif request.is_group_message():
            members = request.data["members"].split(",")
            sender = request.data["sender"]
            for member in members:
                if member in self.clients:
                    if member != sender:
                        self.clients[member].send(data)


server = Server()
