import sys
import socket
import threading
from pyfiglet import Figlet
import Requests
import CA

#importing database commands
import Database

# Argument: port number
class Server:
    def __init__(self):
        # Print Accord server side messages
        f = Figlet(font="smslant")
        print (f.renderText("Welcome to ACCORD"))
        print("Server side")
        self.client_index = -1

        self.start_server()

    def start_server(self):

        #Initialize the databases
        self.is_database_user_init = False
        self.is_database_logs_init = False
        # if is_database_user_init:
        #     Database.initialize_database()
        # if is_database_logs_init:
        #     Database.initialize_log_database()



        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_name = socket.gethostbyname(socket.gethostname())

        # Get command line arguments and check correctness
        args = sys.argv
        if len(args) != 2:
            print("correct usage: python3 Server.py <port>")
        server_port = int(args[1])

        self.clients = dict()

        self.s.bind((server_name, server_port))
        self.s.listen(100)

        print("Running on host: " + str(server_name))
        print("Running on port: " + str(server_port))

        while True:
            c, addr = self.s.accept()

            data = c.recv(2048)

            request = Requests.parse_request(data)

            print(request)

            if request.is_login():
                username = request.data["username"]
                if username == "CA":
                    self.clients["CA"] = c
                else: 
                    print("New connection. Username: " + str(username))
                    self.broadcast(username + " has entered the chat.")
                    self.clients[username] = c
                    threading.Thread(target=self.handle_client,args=(c,username,addr,)).start()

            if request.is_ca_request():
                username = request.data["username"]
                print("New connection. Username: " + str(username))
                self.broadcast(username + " has entered the chat.")
                self.clients[username] = c

                # Communicate with CA
                threading.Thread(target=self.handle_ca, args=(self, request)).start()

                threading.Thread(target=self.handle_client,args=(c,username,addr,)).start()


    def handle_ca(self, data):
        self.clients["CA"].send(data)

        while True:
            try:
                data = c.recv(2048)
            except:
                "Connection with CA closed"

            request = Requests.parse_request()
            if request.is_ca_response():
                username = request.data["username"]
                public_key = request.data["public_key"]
                ca_signature = request.data["signature"]

                if (not Database.check_user(username)):
                    Database.add_user_info(username, public_key, ca_signature)

                self.clients[username].send("Success. Account created.")

                # TODO: Let the client know that they are signed up and logged in

                break
            

    def broadcast(self, msg):
        for connection in self.clients.values():
            connection.send(Requests.broadcast(msg))

    def handle_client(self,c,username,addr):
        while True:
            try:
                data = c.recv(2048)
            except:
                c.shutdown(socket.SHUT_RDWR)
                del self.clients[username]
                
                print(username + " left the room.")
                self.broadcast(username + " has left the room.")

                break

            if data.decode() != "":
                self.handle_recipient(data)
                print("New message: " + str(data.decode()))

    def handle_recipient(self, data):
        request = Requests.parse_request(data)
        if request.is_initiate_direct_message():
            # Initiate new chat between 2 connections
            recipient = request.data["recipient"]
            sender = request.data["requester"]
            if recipient in self.clients:
                self.clients[recipient].send(data)
        elif request.is_initiate_group_chat():
            recipients = request.data["recipients"].split(",")
            recipient = request.data["recipient"]
            sender = request.data["requester"]
            # Skip sending back the handshake to the original sender in the group
            # message handshake 
            if recipient in self.clients and not (sender == recipient):
                self.clients[recipient].send(data)
        # Existing direct message
        elif request.is_direct_message():
            recipient = request.data["recipient"]
            print("dm")
            print(self.clients)
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
    
    # def check_database(self,user):
    #     if Database.check_user(user):
    #         print("User :", user, "in Database")
    #     else:
    #         print("Adding User: ",user, "to the database" )
    #         Database.add_user(user)


server = Server()