import sys
import socket
import threading
from pyfiglet import Figlet
import Requests

# Argument: port number
class Server:
    def __init__(self):
        # Print Accord server side messages
        f = Figlet(font="smslant")
        print (f.renderText("Welcome to ACCORD (server side)"))

        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_name = socket.gethostbyname(socket.gethostname())

        # Get command line arguments and check correctness
        args = sys.argv
        if len(args) != 2:
            print("correct usage: python3 Server.py <port>")
        server_port = int(args[1])

        self.clients = []

        self.s.bind((server_name, server_port))
        self.s.listen(100)
    
        print("Running on host: " + str(server_name))
        print("Running on port: " + str(server_port))

        self.curr_users = {}

        while True:
            c, addr = self.s.accept()

            data = c.recv(1024)
            request = Requests.parse_request(data)

            if request.is_login():
                username = request.data["username"]
                print("New connection. Username: " + str(username))
                
                self.broadcast(username + " has entered the chat.")

                self.curr_users[username] = addr
                print(self.curr_users)

                self.clients.append(c)
                
                threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg):
        for connection in self.clients:
            connection.send(Requests.broadcast(msg))

    def handle_client(self,c,addr):
        while True:
            try:
                data = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                
                print(str(self.curr_users[c])+ " left the room.")
                self.broadcast(str(self.curr_users[c])+ " has left the room.")

                break

            if data.decode() != "":
                self.handle_recipient(data)
                print("New message: " + str(data.decode()))

    def handle_recipient(self, data):
        self.client_index = -1
        request = Requests.parse_request(data)
        if request.is_initiate_chat():
            requester = request.data["requester"]
            recipient = request.data["recipient"]
            if recipient in self.curr_users: 
                self.client_index = list(self.curr_users.keys()).index(recipient)
                self.clients[self.client_index].send(Requests.broadcast(requester + " has started chatting with you."))
        elif request.is_message():
            if self.client_index == -1:
                print(data)
                self.broadcast(request.data["message"])
            else:
                self.clients[self.client_index].send(data)

server = Server()