import sys
import socket
import threading
from pyfiglet import Figlet
import Crypto_Functions
import Send, Receive
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
        self.contacts = {}         # {user:  {"aes_key", "hmac_key", "public_key"}}
        self.groups = {}           # {group_name: {"aes_key", "hmac_key", "members"}}
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
        
        message_type = input("group or direct? ")

        if (message_type == "direct"):
            self.recipient = input("Recipient: ")
            self.recipient_group = ""
            self.populate_public_keys(self.recipient)
            self.send_direct()

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
                message_type = input("group or direct? ")
                if (message_type == "direct"):
                    self.recipient = input("Recipient: ")
                    self.populate_public_keys(self.recipient)
                    if (recipient not in self.contacts or "aes_key" not in self.contacts[recipient]):
                        # keys = {"aes": ..., "hmac": ...}
                        keys = Send.send_direct_handshake(self.username, self.recipient, self.s, self.private_key, self.contacts[self.recipient]["public_key"])
                        self.contacts[recipient] = {
                            "aes": keys["aes"],
                            "hmac": keys["hmac"],
                            "public_key": self.contacts[recipient]["public_key"]
                        }
                    else:
                        msg = input("Message: ")
                        Send.send_direct(self.recipient, self.contacts, message)

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

                    if (self.recipient_group not in self.groups):
                        self.recipient_group = input("What would you like to name the group? ")
                        # Send a handshake to each member in the group
                        for recipient in self.group_names:
                            self.populate_public_keys(recipient)
                            # TODO Pavle continue here
                            Send.send_group_handshake(self.username, recipient, )
                    else:
                        msg = input("Message: ")
                        Send.self.send_group(msg, self.username, self.recipient_group)
                else: 
                    print("Enter valid response: group or direct")

    def handle_receive(self):
        while True:
            data = self.s.recv(2048)
            request = Requests.parse_request(data)

            # Handle different message types
            if request.is_direct_message():
                Receive.receive_direct(request.data, self.contacts)
            elif request.is_group_message():
                Receive.receive_group(request.data, self.groups)
            elif request.is_broadcast():
                print(request.data["message"]) 

            # Initiate the group chat and save keys
            elif request.is_initiate_group_chat():
                print("type is initiate group chat")
                keys = Receive.receive_group_handshake(request.data, self.username, self.groups, self.private_key)
                group_name = keys["group_name"]
                aes_key = keys["aes"]
                hmac_key = keys["hmac"]
                members = keys["members"]

                # This will completely overwrite or add a new one
                self.groups[group_name] = {"aes_key": aes_key, "hmac_key": hmac_key, "members": members}

            elif request.is_initiate_direct_message():
                keys = Receive.receive_direct_handshake(request.data, self.username, self.contacts, self.private_key)
                aes_key = keys["aes"]
                hmac_key = keys["hmac"]
                requester = keys["requester"]

                # This will add or overwrite two fields to the requester's contact, leaving the others
                self.contacts[requester]{"aes_key"} = keys["aes"]
                self.contacts[requester]{"hmac_key"} = keys["hmac"]

    
    def populate_public_keys(self, user_name: str):
        with open('public_{}.pem'.format(user_name), 'rb') as public:
            self.public_keys[user_name] = public.read() # This is still a string

    def populate_private_key(self):
        f =  open('private_{}.pem'.format(self.username), 'rb')
        self.private_key = f.read()
        f.close()
            
        
client = Client()