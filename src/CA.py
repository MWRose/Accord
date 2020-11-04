"""
Certificate Authority. Needs to create signitures over public keys and usernames to ensure the public key is the correct one.
"""
import socket
import sys
import Requests
import Crypto_Functions

SERVER_NAME = 1#
SERVER_PORT = 1#


class certifcateAuth:
    def __init__(self):
        pass
        
    def start_ca(self):   
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((SERVER_NAME, SERVER_PORT))
        self.s.listen(100)
        while True:
            c, addr = self.s.accept()

            data = c.recv(2048)
            request = Requests.parse_request(data)

            ## From Client (Encrypted<Username + Public_key : under CA public key>, Signature<Username + Public_key: Under Client Private>)
            ## From CA (Username, Public_key, Signature<Username + Public_key: Under CA Private>)
            if request.is_ca_request():
                username = request.data["username"]
                public_key_b64 = request.data["public_key"].encode(2:-1)
                public_key = base64.b64decode(enc_msg_b64)
                

    def sign_request(self, username, public_key, signature):
        self.check_signature(username, public_key, signature)
        

    def check_signature(self, username: str, public_key: str, signature):
        """ Takes a username and a public key and checks that the signature is correct """
        msg = username + public_key
        return Crypto_Functions.rsa_check_sign(msg, signature, public_key)

