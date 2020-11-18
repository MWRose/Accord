"""
Certificate Authority. Needs to create signitures over public keys and usernames to ensure the public key is the correct one.
"""
import socket
import sys
import Requests
import Crypto_Functions
import base64
import threading
import CA_Database
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

        CA_Database.initialize_database()

        self.start_ca()
        

    def start_ca(self):   
        
        # Get command line arguments and check correctness
        args = sys.argv
        if len(args) != 2:
            print("correct usage: python3 CA.py <port>")

        hostname = socket.gethostbyname(socket.gethostname())
        ca_port = int(args[1])

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((hostname, ca_port))
        self.s.listen(100)

        self.clients = dict()

        print("Running on host: " + str(hostname))
        print("Running on port: " + str(ca_port))
        
        while True:
            print("In while loop in CA")
            c, addr = self.s.accept()
            data = c.recv(4096)

            request = Requests.parse_request(data)
            print("Received from the client: ", data)

            if len(request.data) == 0:
                print("There was in issue with the received data. Received the following raw data: ", data)
            elif request.is_ca_request():
                username = request.data["username"]
                print("New request. Username: " + str(username))
                self.clients[username] = c
                # Communicate with a client on a separate thread
                threading.Thread(target=self.handle_client, args=(c,username,addr,request.data,)).start()
                
    def handle_client(self, c, username, address, data):   
        if CA_Database.username_exists(username):
            print("Username " + username + " exists in the CA database.")
            ca_response = Requests.ca_response_invalid()
            self.clients[username].send(ca_response)
        else:
            public_key_b64 = data["public_key"].encode()[2:-1]
            public_key = base64.b64decode(public_key_b64)
            message = username + "," + public_key.decode()
            ca_signature = Crypto_Functions.rsa_sign(message.encode(), self.private_key)
            ca_signature_b64 = base64.b64encode(ca_signature)
            ca_response = Requests.ca_response_valid(username, data["public_key"], str(ca_signature_b64))
            print("Signed public key for the user: " + username)
            print("Adding user info to the CA database.")
            CA_Database.add_user(username, data["public_key"], str(ca_signature_b64))
            print("Sending the signature back to the client.")
            self.clients[username].send(ca_response)
            

ca = CertAuth()