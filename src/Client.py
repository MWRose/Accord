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
from PasswordChecker import PasswordChecker 

# Argument: IP address, port number
# Can run this multiple times for multiple different users
class Client:
    def __init__(self):
        # Print Accord client side messages
        f = Figlet(font="smslant")
        print (f.renderText("Welcome to ACCORD"))
        print ("Chat away!")

        self.recipient = ""        # Direct message recipient
        self.group_name = ""       # Group message name
        self.group_members = []    # Names of members of the group
        self.private_key = ""      # Private key for the client
        self.public_keys = {}      # Public keys for other clients TODO: Remove
        self.contacts = {}         # {user:  {"aes_key", "hmac_key", "public_key"}}
        self.groups = {}           # {group_name: {"aes_key", "hmac_key", "members"}}
        self.username = "" # Username of this client
        self.loggedin = False
        self.ca_public_key = ""
        self.password_aes = b""
        self.password_hmac = b""
        
        Database.initialize_username_database() # initializes the database w/username, public key, signatures

        self.create_connection()

        '''
        # Sign in to existing account
        if (Database.check_email(self.username)):
           self.password = input("Enter your password: ")
           if (Database.check_password(self.username, self.password)):
            #    Gen.generate_key_pair(self.username)
            #    self.populate_private_key()
               self.create_connection()
        else:             
            strong_password = False
            while not strong_password:
                self.password = input("Create new password: ")
                passwordChecker = PasswordChecker(self.password)
                if(passwordChecker.password_checker()):
                    Database.add_user_info(self.username, self.password)
                    Gen.generate_key_pair(self.username)
                    self.populate_private_key()
                    self.create_connection()
                    strong_password = True
                else: 
                    print("The password you typed in was not secure. Password must use a mix of letters and numbers and must be at least 8 characters.")
    '''

    '''
    Users
    -----
    (pavle@pomona.edu, private_key)
    
    Contacts
    --------
    (username, contact, aes_key)

    pavle@pomona.edu, asasdsdfgbsdsdfgfds
    pavle@pomona.edu, asdsdasdasadds
    pavle@pomona.edu, adwsasdasasdas
    max@pomona.edu

    Messages (pavle@)
    --------
    from, to, timestamp, message
    '''

    def authenticate(self):
        choice = input("Login or signup: ")
        if choice == "login":
            self.login()
        else:
            self.create_account()

    def create_account(self):
        valid_username = False 
        while not valid_username:
            self.username = input("Enter email: ")
            if(Database.check_user(self.username)):
                print("Username already exists in the system.")
            else:
                valid_username = True
                
        strong_password = False
        while not strong_password:
            self.password = input("Create new password: ")
            passwordChecker = PasswordChecker(self.password)
            if(passwordChecker.password_checker()):
                strong_password = True

                #Database.add_user_info(self.username, self.password)
                Gen.generate_key_pair(self.username)
                
                # Get user's public key
                f =  open('public_{}.pem'.format(self.username), 'rb')
                public_key = f.read()
                f.close()
                
                # Get user's private key
                self.populate_private_key()
                
                # Get CA public key TODO: Make this a hardcoded static var
                f = open('public_ca.pem', 'rb')
                self.ca_public_key = f.read()
                f.close()

                # Construct a message for CA
                aes_key = Crypto_Functions.generate_session_key()
                aes_keyb64 = base64.b64encode(aes_key)
                aes_key_encrypted = Crypto_Functions.rsa_encrypt(str(aes_keyb64), self.ca_public_key)
                aes_key_encryptedb64 = base64.b64encode(aes_key_encrypted)

                aes_key_signature = str(aes_key_encryptedb64).encode()
                aes_key_signed = Crypto_Functions.rsa_sign(aes_key_signature, self.private_key)
                aes_key_signedb64 = base64.b64encode(aes_key_signed)

                message = self.username + "," + public_key.decode()
                message_b64 = base64.b64encode(message.encode())
                encrypted, iv = Crypto_Functions.aes_encrypt(str(message_b64), aes_key)
                encrypted_b64 = base64.b64encode(encrypted)
                iv_b64 = base64.b64encode(iv)

                # Create a signature for the message contents
                signature = str(encrypted_b64).encode()
                signed = Crypto_Functions.rsa_sign(signature, self.private_key)
                signed_b64 = base64.b64encode(signed)

                request = Requests.ca_request(str(aes_key_encryptedb64), str(aes_key_signedb64), str(iv_b64), str(encrypted_b64), str(signed_b64), self.username)
                print("Request for CA: ", request)
                self.s.send(request)

                while True:
                    data = self.s.recv(4096)
                    request = Requests.parse_request(data)
                    # TODO: This needs to be worked on
                    if request.is_account_created():
                        print("Account successfully created! Please log in with your new credentials.")
                        break
                    elif request.is_account_not_created():
                        print("Account was not created. Please try again.")
                        self.create_account()
            else: 
                print("The password you typed in was not secure. Password must use a mix of letters and numbers and must be at least 8 characters.")
            self.login()


    def login(self):
        self.username = input("Please enter username: ")
        #TODO: Check if username exists in the database (this will probably need to be a send to server)

        # request = Requests.login_request(self.username)
        # self.s.send(request)

        # while True:
        #     data = self.s.recv(2048)
        #     request = Requests.parse_request(data)

        #     # Wait for the login response
        #     if request.is_login_response():
        #         #TODO: Parse the response and populate the correct dictionaries
        #         print("todo")
        #     break


        # Receive information that is stored in the database
        contacts = Database.get_user_contact_info(self.username)
        password = input("Please enter your password: ")
        self.password_aes, self.password_hmac = Crypto_Functions.hash_keys(password.encode())

        for contact in contacts:

            # Get contact info
            recipient = contact["contact"]
            enc_aes_b64 = contact["contact_aes"].encode()[2:-1]
            enc_aes = base64.b64decode(enc_aes_b64)
            enc_hmac_b64 = contact["hmac_key"].encode()[2:-1]
            enc_hmac = base64.b64decode(enc_hmac_b64)
            signed_b64 = contact["signature"].encode()[2:-1]
            signed = base64.b64decode(signed_b64)
            iv_aes_b64 = contact["iv_aes"]
            iv_aes = base64.b64decode(iv_aes_b64)
            iv_hmac_b64 = contact["iv_hmac"]
            iv_hmac = base64.b64decode(iv_hmac_b64)
            
            # Check signature
            signature_contents = self.username + recipient + contact["enc_aes"] + contact["enc_hmac"] + contact["iv_aes"] + contact["iv_hmac"]
            Crypto_Functions.check_hmac(signature_contents, signed, self.password_hmac)

            # Decrypt keys
            iv_aes.encode()[2:1]
            aes_key = Crypto_Functions.aes_decrypt(enc_aes, iv_aes, self.password_aes)
            hmac_key = Crypto_Functions.aes_decrypt(enc_hmac, iv_hmac, self.password_aes)

            
            self.contacts[recipient] = {"aes_key": aes_key, "hmac_key": hmac_key}

            # TODO: Add functionality to save the public_keys in the future

        self.loggedin = True


    def sign_off(self):
        pass


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

        self.authenticate()
        
        # Handles threading of sending and receiving messages for a client
        send_handler = threading.Thread(target=self.handle_send, args=())
        send_handler.start()

        receive_handler = threading.Thread(target=self.handle_receive,args=())
        receive_handler.start()


    # def account_create(self):
        
    #     username = input("Please enter your username: ")

    #     # Check password
    #     while True:
    #         password = input("Please enter your password: ")
    #         pass_check = new



    def choose_send(self):
        
        message_type = input("group or direct? ")

        if (message_type == "direct"):
            self.recipient = input("Recipient: ")
            self.populate_public_keys(self.recipient)
            self.group_name = ""
            self.group_members = []

            # Check whether we have to send handshake
            if (self.recipient not in self.contacts or "aes_key" not in self.contacts[self.recipient]):
                # Send handshake 
                # keys = {"aes": ..., "hmac": ...}
                keys = Send.send_direct_handshake(self.username, self.recipient, self.s, self.private_key, self.contacts[self.recipient]["public_key"])
                
                # Update recipient's keys
                self.contacts[self.recipient]["aes_key"] = keys["aes"]
                self.contacts[self.recipient]["hmac_key"] = keys["hmac"]

                # Update the Database
                email = self.username
                contact = self.recipient

                # Get encrypted aes under self.password_aes
                contact_aes = base64.b64encode(["aes"])
                enc_contact_aes, iv_aes = Crypto_Functions.aes_encrypt(str(contact_aes), self.password_aes)
                enc_contact_aes = str(base64.b64encode(enc_contact_aes))
                iv_aes = str(base64.b64encode(iv_aes))
                
                # Get encrypted hmac under self.password_aes
                hmac_key = base64.b64encode(["hmac"])
                enc_hmac_key, iv_hmac = Crypto_Functions.aes_encrypt(str(hmac_key), self.password_aes)
                enc_hmac_key = str(base64.b64encode(enc_hmac_key))
                iv_hmac = str(base64.b64encode(iv_hmac))

                # Create the signature
                signature_contents = contact + contact_aes + enc_hmac_key
                



                
            
            
        #TODO: Clean up this logic, need to check if it's existing
        elif (message_type == "group"):
            self.recipient = ""
            

            while True:

                inp = input("new or existing? ")
                # Check if the group is new
                if inp == "new" or inp == "0":

                    # Get group name and members
                    group = input("Type in the members separated with a comma: ")
                    self.group_name = input("What would you like to name the group? ")
                    self.group_members = group.split(',')
                    break
                    

                # The group already exists
                elif inp == "existing" or inp == "1":
                    group = input("Enter group name: ")

                    if not group in self.groups:
                        print("The group was not found")

                    else:

                        # Get group name and members
                        self.group_name = group
                        self.group_members = self.groups[group]["members"]
                        break

                else:
                    print("Please type new or existing.")


            if (self.group_name not in self.groups):

                # Initialize the group dict
                self.groups[self.group_name] = {}
                self.groups[self.group_name]["members"] = self.group_members

                # Send a handshake to each member in the group
                key = Crypto_Functions.generate_session_key()
                for recipient in self.group_members:
                    
                    # Make sure we have a public key
                    if recipient not in self.contacts.keys():
                        self.populate_public_keys(recipient)

                    keys = Send.send_group_handshake(self.username, recipient, self.group_members, self.s, self.private_key, self.contacts[recipient]["public_key"], key, self.group_name)
                    # TODO: Probably don't need to reassign as it should be the same
                    self.groups[self.group_name]["aes_key"] = keys["aes"]
                    self.groups[self.group_name]["hmac_key"] = keys["hmac"]
          
        else: 
            print("Enter valid response: group or direct")


    def handle_send(self):
        while True:
            if not self.recipient and not self.group_name:
                self.choose_send()

            else:

                msg = input("Message: ")
                if msg.lower() == "choose" or msg.lower() == "change":
                    self.choose_send()

                if self.recipient and not self.group_name:
                    
                    # Send the message
                    Send.send_direct(self.username, self.recipient, self.contacts, msg, self.s)

                elif self.group_name:
                    Send.send_group_message(msg, self.username, self.group_name, self.s, self.group_members, self.groups)

                else:
                    print("This should not print")
                    print(bool(self.recipient), bool(self.group_name))
                    self.choose_send()

    def handle_receive(self):
        while True:
            data = self.s.recv(4096)
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

                requester = request.data["requester"]
                # Make sure we have the contact
                if requester not in self.contacts or "public_key" not in self.contacts[requester].keys():
  
                    self.populate_public_keys(requester)

                # Recieve the handshake
                keys = Receive.receive_group_handshake(request.data, self.username, self.groups, self.contacts, self.private_key)
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

                # Update the database
                # TODO

    def populate_public_keys(self, username: str):
        
        # Get the public key from the data base
        info = Database.get_user_info(username)
        public_key = info["public_key"]
        ca_signature = info["ca_signature"]

        # Check the CA's signature
        signature_contents = username + "," + str(public_key)
        if not Crypto_Functions.rsa_check_sign(signature_contents, ca_signature, self.ca_public_key):
            print("The requested public key and signature do not match for " + username)
            return

        if username not in self.contacts:
            self.contacts[username] = dict()
        self.contacts[username]["public_key"] = public_key

    def populate_private_key(self):
        f =  open('private_{}.pem'.format(self.username), 'rb')
        self.private_key = f.read()
        f.close()
            
        
client = Client()