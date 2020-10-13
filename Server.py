import sys
import socket
import threading
from pyfiglet import Figlet
import Requests

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

            if request.is_login():
                username = request.data["username"]
                print("New connection. Username: " + str(username))

                self.broadcast(username + " has entered the chat.")

                self.clients[username] = c
                print("clients: ", self.clients)

                threading.Thread(target=self.handle_client,args=(c,username,addr,)).start()

    def broadcast(self, msg):
        for connection in self.clients.values():
            print(connection)
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
        recipient = request.data["recipient"]
        if request.is_initiate_chat():
            # Initiate new chat between 2 connections
            if recipient in self.clients: 
                self.clients[recipient].send(data)
        # Existing chat
        elif request.is_message():
            if recipient in self.clients: 
                self.clients[recipient].send(data)

    def check_database(self,user):
        if Database.check_email(user):
            print("User :", user, "in Database")
        else:
            print("Adding User: ",user, "to the database" )
            Database.add_user_email(user)


server = Server()