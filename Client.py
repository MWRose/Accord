import sys
import socket
import threading
from pyfiglet import Figlet
import Crypto_Functions
import Requests
import base64
import Gen

# Argument: IP address, port number
# Can run this multiple times for multiple different users
class Client:
    def __init__(self):
        # Print Accord client side messages
        f = Figlet(font="smslant")
        print (f.renderText("Welcome to ACCORD"))
        print ("Chat away!")


        self.recipient = ""
        self.private_key = ""
        self.public_keys = {}
        self.contacts = {}
        self.username = input("Enter username: ")


        # TODO Establish public and private keys
        Gen.generate_key_pair(self.username)

        self.populate_private_key()
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Get command line arguments and check correctness
            args = sys.argv
            if len(args) != 3:
                print("correct usage: python3 Server.py <server name> <port>")
                sys.exit(0)

            server_name = args[1]
            server_port = int(args[2])

            self.s.connect((server_name, server_port))
        except:
            print("Couldn't connect to server, please type in valid host name and port.")
            sys.exit(0)

        self.s.send(Requests.login(self.username))
        
        # Handles threading of sending and receiving messages for a client
        send_handler = threading.Thread(target=self.handle_send, args=())
        send_handler.start()

        receive_handler = threading.Thread(target=self.handle_receive,args=())
        receive_handler.start()

    def handle_send(self):
        while True:
            if not self.recipient:
                self.recipient = input("Recipient: ")
            self.populate_public_keys(self.recipient)
            # Check if chat has already been initiated with this recipient
            if (self.recipient not in self.contacts):
                self.send_handshake()
            else:
                msg = input("Message: ")
                print(self.contacts[self.recipient])
                msg, iv = Crypto_Functions.aes_encrypt(msg, self.contacts[self.recipient])

                # Encoding
                msg_b64 = base64.b64encode(msg)
                iv_b64 = base64.b64encode(iv)
    
                self.s.send(Requests.message(self.username, self.recipient, str(msg_b64), str(iv_b64))) 

    def handle_receive(self):
        while True:
            data = self.s.recv(2048)
            request = Requests.parse_request(data)
            print(data)
            # Handle different message types
            if request.is_message():
                sender = request.data["sender"]
                print("receive message", sender)

                # Decode messages
                enc_msg_b64 = request.data["message"].encode()[2:-1]
                iv_b64 = request.data["iv"].encode()[2:-1]
                enc_msg = base64.b64decode(enc_msg_b64)
                iv = base64.b64decode(iv_b64)

                # Decrypt message
                print(self.contacts[sender])

                decrypted_msg = Crypto_Functions.aes_decrypt(enc_msg, iv, self.contacts[sender])
    
                print(sender + ": " + decrypted_msg)
            elif request.is_broadcast():
                print(request.data["message"]) 
            elif request.is_initiate_chat():
                self.receive_handshake(request.data)

    def send_handshake(self):

        # Message contents
        username = self.username
        recipient = self.recipient
        aes_key = Crypto_Functions.generate_session_key()
        print("reg",aes_key)

        # RSA encrypt the key
        # sender, recipient, encrypted(sender, recipient, aes_key), signed(encrpyted(---))
        aes_key_b64 = base64.b64encode(aes_key)
        encrypt_msg = username + "," + recipient + "," + str(aes_key_b64)
        encrypted = Crypto_Functions.rsa_encrypt(encrypt_msg, self.public_keys[recipient])
        print("b64",str(aes_key_b64))
        encrypted_b64 = base64.b64encode(encrypted)

        # Create a signature for the message contents
        signature = (username + recipient + str(encrypted_b64)).encode()
        signed = Crypto_Functions.rsa_sign(signature, self.private_key)
        signed_b64 = base64.b64encode(signed)

        request = Requests.initiate_chat(self.username, self.recipient, str(encrypted_b64), str(signed_b64))
        self.s.send(request)
        self.contacts[recipient] = aes_key


    def receive_handshake(self, data):
        recipient = data["recipient"]
        
        if recipient == self.username:
            # Parsed message contents
            requester = data["requester"]
            encrypted_b64 = data["encrypted"]
            signed_b64 = data["signed"]

            encrypted = base64.b64decode(encrypted_b64.encode()[2:-1])
            signed = base64.b64decode(signed_b64.encode()[2:-1])
            #print(signed, type(signed))
            
            # Check if we have the requesters public_key, and if not get it
            if requester not in self.public_keys:
                self.populate_public_keys(requester)

            # Check the signature
            signature_contents = (requester + recipient + str(encrypted_b64)).encode()
            if not Crypto_Functions.rsa_check_sign(signature_contents, signed, self.public_keys[requester]):
                print("Invalid signature")
            else:
                # Parse encrpyted message
                decrypted_msg = Crypto_Functions.rsa_decrypt(encrypted, self.private_key)
                decrypted_msg_split = decrypted_msg.split(",", 2)
                print(decrypted_msg_split)

                # Check the contents of the sender and re
                enc_sender = decrypted_msg_split[0]
                enc_recipient = decrypted_msg_split[1]
                # TODO: Check that these are the same

                aes_key_b64 = decrypted_msg_split[2].encode()[2:-1]
                # print(aes_key_b64)
                aes_key = base64.b64decode(aes_key_b64)
                # print("aes key", aes_key)
                self.contacts[requester] = aes_key
        else:
            print("User doesn't match intended recipient")
    
        
    def populate_public_keys(self, user_name: str):
        with open('public_{}.pem'.format(user_name), 'rb') as public:
            self.public_keys[user_name] = public.read() # This is still a string

    def populate_private_key(self):
        f =  open('private_{}.pem'.format(self.username), 'rb')
        self.private_key = f.read()
        f.close()
            
        
        
        
        
    

client = Client()