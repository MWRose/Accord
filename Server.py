import sys
import socket
import threading

# Argument: port number
class Server:
    def __init__(self):
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_name = socket.gethostbyname(socket.gethostname())

        # Get command line arguments and check correctness
        args = sys.argv
        if len(args != 2):
            print("correct usage: python3 Server.py <port>")
        server_port = int(args[1])

        # server_port = int(input("Enter what port number to run the host server on: "))

        self.clients = []

        self.s.bind((server_name, server_port))
        self.s.listen(100)
    
        print("Running on host: " + str(server_name))
        print("Running on port: " + str(server_port))

        self.curr_users = {}

        while True:
            c, addr = self.s.accept()

            username = c.recv(1024).decode()
            
            print("New connection. Username: " + str(username))
            self.broadcast(username + " has entered the chat.")

            self.curr_users[c] = username

            self.clients.append(c)
             
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg):
        for connection in self.clients:
            connection.send(msg.encode())

    def handle_client(self,c,addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                
                print(str(self.curr_users[c])+ " left the room.")
                self.broadcast(str(self.curr_users[c])+ " has left the room.")

                break

            if msg.decode() != "":
                print("New message: " + str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)

server = Server()