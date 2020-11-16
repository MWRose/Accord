"""
Certificate Authority. Needs to create signitures over public keys and usernames to ensure the public key is the correct one.
"""
import socket
import sys
import Requests
import Crypto_Functions
import base64
import threading
from pyfiglet import Figlet

class CertAuth:
    def __init__(self):
        f = Figlet(font="smslant")
        print(f.renderText("Certificate Authority"))

        # Load the private key for CA
        f =  open('private_ca.pem', 'rb')
        self.private_key = f.read()
        f.close()    

        # Load the public key for CA
        f =  open('public_ca.pem', 'rb')
        self.public_key = f.read()
        f.close()

        self.start_ca()
        
    def start_ca(self):   
        hostname = socket.gethostbyname(socket.gethostname())
        # Get command line arguments and check correctness
        args = sys.argv
        if len(args) != 2:
            print("correct usage: python3 CA.py <port>")
        ca_port = int(args[1])

        self.clients = dict()

        self.s.bind((server_name, ca_port))
        self.s.listen(100)

        print("Running on host: " + str(hostname))
        print("Running on port: " + str(ca_port))
        
        while True:
            print("In while loop in CA")
            data = self.s.recv(4096)

            request = Requests.parse_request(data)
            print("Received from the client: ", data)

            if len(request.data) == 0:
                print("There was in issue with the received data. Received the following raw data: ", data)
            elif request.is_ca_request():
                username = request.data["username"]
                print("New CA request. Username: " + str(username))
                self.clients[username] = c
                # Communicate with a client on a separate thread
                threading.Thread(target=self.handle_client, args=(c,username,addr,data,)).start()
                
    def handle_client(self, username, address, data)
        while True:
            try:
                data = c.recv(4096)
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
        username = data["username"]
        public_key = data["public_key"]
        if username not in self.clients:
            print("Provided username does not match any connected client")
            return
        message = username + "," + public_key.decode()
        ca_signature = Crypto_Functions.rsa_sign(message.encode(), self.private_key)
        ca_signature_b64 = base64.b64encode(ca_signature)
        ca_response = Requests.ca_response(username, public_key_b64, str(ca_signature_b64))
        self.clients[recipient].send(ca_response)

ca = CertAuth()