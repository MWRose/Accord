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


        self.recipient = ""        # Direct message recipient
        self.recipient_group = ""  # Group message name
        self.group_names = []      # Names of members of the group
        self.private_key = ""      # Private key for the client
        self.public_keys = {}      # Public keys for other clients
        self.contacts = {}         # Contacts that have shared a key {"aes_key", "hmac_key"}
        self.groups = {}           # Group chats with a shared key and members {"aes_key", "hmac_key", "members"}
        self.username = input("Enter username: ") # Username of this client


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


    def choose_send(self):
        pass
        message_type = input("group or private? ")

        if (message_type == "private"):
            self.recipient = input("Recipient: ")
            self.recipient_group = ""
            self.populate_public_keys(self.recipient)
            self.send_private()

        elif (message_type == "group"):

            self.recipient = ""
                
            # Get user input for group or not
            is_new = False
            inp = input("Start a new group chat or chat with existing group chat? ")
            if (inp == "new" or "0"):
                is_new = True
            elif (inp == "existing" or "1"):
                is_new = False
            else: 
                print("Please type new or existing.")
        
            # Check if the group is new
            if (is_new):
                group = input("Type in the members separated with a comma: ")
                
                #TODO: A check for if these are valid group members?? 
                self.group_names = group.split(',')

            # The group already exists
            else:
                group = input("Enter group name: ")
                if not group in groups:
                    print("The group was not found")
                else:
                    self.recipient_group = group
                    self.group_names = groups[group]["members"]

            self.send_group()


    def handle_send(self):
        while True:
            if not self.recipient or not self.receive_group:
                message_type = input("group or private? ")
                if (message_type == "private"):
                    self.recipient = input("Recipient: ")
                    self.populate_public_keys(self.recipient)
                    self.send_private()

                elif (message_type == "group"):
                     
                    # Get user input for group or not
                    is_new = False
                    inp = input("Start a new group chat or chat with existing group chat? ")
                    if (inp == "new" or "0"):
                        is_new = True
                    elif (inp == "existing" or "1"):
                        is_new = False
                    else: 
                        print("Please type new or existing.")
                
                    # Check if the group is new
                    if (is_new):
                        group = input("Type in the members separated with a comma: ")
                        
                        #TODO: A check for if these are valid group members?? 
                        self.group_names = group.split(',')

                    # The group already exists
                    else:
                        group = input("Enter group name: ")
                        if not group in groups:
                            print("The group was not found")
                        else:
                            self.recipient_group = group
                            self.group_names = groups[group]["members"]

                    self.send_group()

                else: 
                    print("Enter valid response: group or private")
            

    def send_group(self):
        if (self.recipient_group not in self.groups):

            self.recipient_group = input("What would you like to name the group? ")

            # Send a handshake to each member in the group
            for recipient in self.group_names:
                self.populate_public_keys(recipient)
                
            self.send_handshake(True)
            self.recipient = ""
            self.send_msg_group()
        
        else:
            self.send_msg_group()

    def send_msg_group(self):  
        msg = input("Message: ")

        # Get shared key
        aes_key = self.groups[self.recipient_group]["aes"]
        hmac_key = self.groups[self.recipient_group]["hmac"]

        # Encrypt
        enc_msg, iv = Crypto_Functions.aes_encrypt(msg, aes_key)

        # Create message tag on encypted data
        tag = Crypto_Functions.hmac(enc_msg, hmac_key)

        # Encoding
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        self.s.send(Requests.group_message(self.username, ",".join(self.group_names), self.recipient_group, str(enc_msg_b64), str(iv_b64), tag)) 

    def send_private(self):
        
            # Check if chat has already been initiated with this recipient
            if (self.recipient not in self.contacts):
                self.send_handshake(False)
            else:
                msg = input("Message: ")

                # Get shared key
                aes_key = self.contacts[self.recipient]["aes"]
                hmac_key = self.contacts[self.recipient]["hmac"]

                # Encrypt
                enc_msg, iv = Crypto_Functions.aes_encrypt(msg, aes_key)

                # Create message tag on encypted data
                tag = Crypto_Functions.hmac(enc_msg, hmac_key)

                # Encoding
                enc_msg_b64 = base64.b64encode(enc_msg)
                iv_b64 = base64.b64encode(iv)
    
                self.s.send(Requests.message(self.username, self.recipient, str(enc_msg_b64), str(iv_b64), tag))


    def handle_receive(self):
        while True:
            data = self.s.recv(2048)
            request = Requests.parse_request(data)

            # Handle different message types
            if request.is_direct_message():
                self.receive_private(request)
            elif request.is_group_message():
                self.receive_group(request)
            elif request.is_broadcast():
                print(request.data["message"]) 

            # If its a group, recieve one way
            elif request.is_initiate_group_chat():
                print("type is initiate group chat")
                self.receive_handshake(request.data, True)
            elif request.is_initiate_direct_message():
                self.receive_handshake(request.data, False)
                
    
    def receive_private(self, request):
        sender = request.data["sender"]

        # Decode messages
        enc_msg_b64 = request.data["message"].encode()[2:-1]
        iv_b64 = request.data["iv"].encode()[2:-1]
        enc_msg = base64.b64decode(enc_msg_b64)
        iv = base64.b64decode(iv_b64)

        # Get shared key
        aes_key = self.contacts[sender]["aes"]
        hmac_key = self.contacts[sender]["hmac"]

        # Check tag
        tag = request.data["tag"]
        valid = Crypto_Functions.check_hmac(enc_msg, tag, hmac_key)
        if not valid:
            raise Exception("AHHHH")

        # Decrypt message
        decrypted_msg = Crypto_Functions.aes_decrypt(enc_msg, iv, aes_key)

        print(sender + ": " + decrypted_msg)


    def receive_group(self, request):
        sender = request.data["sender"]

        # Decode messages
        enc_msg_b64 = request.data["message"].encode()[2:-1]
        iv_b64 = request.data["iv"].encode()[2:-1]
        enc_msg = base64.b64decode(enc_msg_b64)
        iv = base64.b64decode(iv_b64)

        # Get shared key
        print(self.groups)
        aes_key = self.groups[sender]["aes"]
        hmac_key = self.groups[sender]["hmac"]
        
        # Check tag
        tag = request.data["tag"]
        valid = Crypto_Functions.check_hmac(enc_msg, tag, hmac_key)
        if not valid:
            raise Exception("AHHHH")

        # Decrypt message
        decrypted_msg = Crypto_Functions.aes_decrypt(enc_msg, iv, aes_key)

        print(sender + " to " + data["group_name"] + ": " + decrypted_msg)

    
    def send_handshake(self, is_group: bool):

        # Message contents
        username = self.username
        recipient = self.recipient
        key = Crypto_Functions.generate_session_key()

        # RSA encrypt the msg
        key_b64 = base64.b64encode(key)
        encrypt_msg = username + "," + recipient + "," + str(key_b64)
        encrypted = Crypto_Functions.rsa_encrypt(encrypt_msg, self.public_keys[recipient])
        encrypted_b64 = base64.b64encode(encrypted)

        # Create a signature for the message contents
        if is_group:
            signature = (username + ",".join(self.group_names) + str(encrypted_b64)).encode()
        else:
            signature = (username + recipient + str(encrypted_b64)).encode()
        signed = Crypto_Functions.rsa_sign(signature, self.private_key)
        signed_b64 = base64.b64encode(signed)

        # Transform key into two keys
        aes_key, hmac_key = Crypto_Functions.hash_keys(key)

        if is_group:
            request = Requests.initiate_group_chat(self.username, ",".join(self.group_names), str(encrypted_b64), str(signed_b64))
            self.groups[self.recipient_group] = {"aes": aes_key, "hmac": hmac_key, "members": self.group_names}
        else:
            request = Requests.initiate_direct_message(self.username, self.recipient, str(encrypted_b64), str(signed_b64))
            self.contacts[recipient] = {"aes": aes_key, "hmac": hmac_key}
            
        self.s.send(request)


    def receive_handshake(self, data, is_group: bool):
        print(is_group)
        if (is_group and self.username in data["recipients"].split(",")) or self.username == data["recipient"]:
            # Parsed message contents
            requester = data["requester"]
            encrypted_b64 = data["encrypted"]
            signed_b64 = data["signed"]

            encrypted = base64.b64decode(encrypted_b64.encode()[2:-1])
            signed = base64.b64decode(signed_b64.encode()[2:-1])
            
            # Check if we have the requesters public_key, and if not get it
            if requester not in self.public_keys:
                self.populate_public_keys(requester)

            # Check the signature
            recipient = data["recipients"] if is_group else data["recipient"]
            signature_contents = (requester + recipient + str(encrypted_b64)).encode()
            if not Crypto_Functions.rsa_check_sign(signature_contents, signed, self.public_keys[requester]):
                print("Invalid signature")
            else:
                # Parse encrpyted message
                decrypted_msg = Crypto_Functions.rsa_decrypt(encrypted, self.private_key)
                decrypted_msg_split = decrypted_msg.split(",", 2)

                # Check the contents of the sender and re
                enc_sender = decrypted_msg_split[0]
                enc_recipient = decrypted_msg_split[1]

                key_b64 = decrypted_msg_split[2].encode()[2:-1]
                key = base64.b64decode(key_b64)

                # Transform key into two keys
                aes_key, hmac_key = Crypto_Functions.hash_keys(key)
                if is_group:
                    group_name = data["group_name"]
                    members = data["members"].split(",")
                    self.groups[group_name] = {"aes":aes_key, "hmac": hmac_key, "members": members, "group_name":group_name}
                else: 
                    self.contacts[requester] = {"aes":aes_key, "hmac": hmac_key}
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