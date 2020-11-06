"""
Certificate Authority. Needs to create signitures over public keys and usernames to ensure the public key is the correct one.
"""
import socket
import sys
import Requests
import Crypto_Functions
import base64


class CertAuth:
    def __init__(self):
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
        # Get command line arguments and check correctness
        args = sys.argv
        if len(args) != 3:
            print("correct usage: python3 CA.py <server hostname> <server port>")
        server_hostname = int(args[1])
        server_port = int(args[2])

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((server_hostname, server_port))
        self.s.listen(100)

        setup_request = Requests.login_request("CA")
        self.s.send(setup_request)
        
        while True:
            # c, addr = self.s.accept()

            data = self.s.recv(2048)
            request = Requests.parse_request(data)
            if request.is_ca_request():
                self.receive_request(request.data)
                

    def receive_request(self, data):

        encrypted_b64 = data["encrypted"].encode()[2:-1]
        encrypted = base64.b64decode(encrypted_b64)
        signature_b64 = data["signature"].encode()[2:-1]
        signature = base64.b64decode(signature_b64)

        # Decrypt encrypted using CA private key
        username, public_key = self.decrypt_ca_request(encrypted)

        # Check signature
        signature_contents = encrypted_b64
        if self.check_signature(signature_contents, signature, public_key):
            message = username + "," + str(public_key)
            ca_signature = Crypto_Functions.rsa_sign(message.encode(), self.private_key)
            ca_response = Requests.ca_response(username, public_key, ca_signature)
            print(ca_response)
        else:
            print("Signature not signed with the correct public key")

    def decrypt_ca_request(self, encrypted: bytes):
        decrypted = Crypto_Functions.rsa_decrypt(encrypted, self.private_key)
        username, public_key_str = decrypted.split(",")
        public_key = public_key_str.encode()[2:-1]
        return username, public_key


    def check_signature(self, message, signature, public_key: str):
        """ Takes a username and a public key and checks that the signature is correct """
        return Crypto_Functions.rsa_check_sign(message, signature, public_key)