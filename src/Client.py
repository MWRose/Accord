import sys
import socket
import threading
from pyfiglet import Figlet
import Crypto_Functions
import Send, Receive
import Requests
import base64
import Gen
import Database
import PasswordChecker

# Argument: IP address, port number
# Can run this multiple times for multiple different users
class Client:
    def __init__(self):
        # Print Accord client side messages
        f = Figlet(font="smslant")
        print (f.renderText("Welcome to ACCORD"))
        print ("Chat away!")


        self.recipient = ""        # Direct message recipient
        self.group_name = ""  # Group message name
        self.group_members = []      # Names of members of the group
        self.private_key = ""      # Private key for the client
        self.public_keys = {}      # Public keys for other clients
        self.contacts = {}         # {user:  {"aes_key", "hmac_key", "public_key"}}
        self.groups = {}           # {group_name: {"aes_key", "hmac_key", "members"}}
        self.username = input("Enter username: ") # Username of this client

        # TODO Establish public and private keys
        Gen.generate_key_pair(self.username)

        
        self.populate_private_key()
        self.create_connection()

        # self.username = input("Enter email: ") # Username of this client
        

        
        # Database.initialize_database()
        # # Sign in to existing account
        # if (Database.check_email(self.username)):
        #    self.password = input("Enter your password: ")
        # #    if (Database.check_password(self.username, self.password)):
        # #         # Correct password
        # #         # TODO: continue
        # #         continue
        # # Create new account 
        # #else: 
        #     self.password = input("Create new password: ")
        #     if (PasswordChecker(self.password).password_checker()):
        #         # Save new password
        #         Database.add_user_info(self.username, self.password)
        #     else: 
        #         print("The password you typed in was not secure. Password must use a mix of letters and numbers and must be at least 8 characters.")



        # # TODO Establish public and private keys
        # Gen.generate_key_pair(self.username)

        
        # self.populate_private_key()
        # self.create_connection()

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
            self.group_name = ""
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
                self.group_members = group.split(',')

            # The group already exists
            else:
                group = input("Enter group name: ")
                if not group in groups:
                    print("The group was not found")
                else:
                    self.group_name = group
                    self.group_members = groups[group]["members"]

            self.send_group()


    def handle_send(self):
        while True:
            if not self.recipient or not self.group_name:
                message_type = input("group or direct? ")
                if (message_type == "direct"):
                    self.recipient = input("Recipient: ")
                    self.populate_public_keys(self.recipient)

                    # Check whether we have to send handshake
                    if (self.recipient not in self.contacts or "aes_key" not in self.contacts[self.recipient]):
                        # Send handshake 
                        # keys = {"aes": ..., "hmac": ...}
                        keys = Send.send_direct_handshake(self.username, self.recipient, self.s, self.private_key, self.contacts[self.recipient]["public_key"])
                        
                        # Update recipient's keys
                        self.contacts[self.recipient]["aes_key"] = keys["aes"]
                        self.contacts[self.recipient]["hmac_key"] = keys["hmac"]
                    
                    # Send the message
                    msg = input("Message: ")
                    Send.send_direct(self.username, self.recipient, self.contacts, msg, self.s)

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
                        self.group_members = group.split(',')

                    # The group already exists
                    else:
                        group = input("Enter group name: ")
                        if not group in self.groups:
                            print("The group was not found")
                        else:
                            self.group_name = group
                            self.group_members = self.groups[group]["members"]

                    if (self.group_name not in self.groups):
                        self.group_name = input("What would you like to name the group? ")
                        # Send a handshake to each member in the group
                        for recipient in self.group_members:
                            self.populate_public_keys(recipient)
                            keys = Send.send_group_handshake(self.username, recipient, self.group_members, self.s, self.private_key, self.contacts[recipient]["public_key"])
                            self.groups[self.group_name] = keys
                    else:
                        msg = input("Message: ")
                        for recipient in self.group_members:
                            Send.send_group_message(msg, self.username, recipient, self.group_name, self.s, self.group_members, self.groups)
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
                requester = request.data["requester"]
                if requester not in self.contacts:
                    self.populate_public_keys(requester)
                keys = Receive.receive_direct_handshake(request.data, self.contacts, self.contacts[requester]["public_key"], self.private_key)
                aes_key = keys["aes"]
                hmac_key = keys["hmac"]

                # This will add or overwrite two fields to the requester's contact, leaving the others
                self.contacts[requester]["aes_key"] = aes_key
                self.contacts[requester]["hmac_key"] = hmac_key

    def populate_public_keys(self, username: str):
        with open('public_{}.pem'.format(username), 'rb') as public:
            if username not in self.contacts:
                self.contacts[username] = dict()
            self.contacts[username]["public_key"] = public.read() # This is still a string

    def populate_private_key(self):
        f =  open('private_{}.pem'.format(self.username), 'rb')
        self.private_key = f.read()
        f.close()
            
        
client = Client()