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
import random
import smtplib
from pyfiglet import Figlet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

CA_EMAIL = 'accord.no.reply.register@gmail.com'
CA_PASS = 'acccord123@'

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
            print("Received from the client: ", request.data)
            if len(request.data) == 0:
                print("There was in issue with the received data. Received the following raw data: ", data)
            elif request.is_establish_connection():
                threading.Thread(target=self.handle_client,args=(c,addr,)).start()
                
    def handle_client(self,c,addr):
        while True:
            try:
                data = c.recv(4096)
            except:
                c.shutdown(socket.SHUT_RDWR)
                break

            self.handle_receive(data, c)

    def handle_receive(self, data, c):
        request = Requests.parse_request(data)
        if len(request.data) == 0:
                print("There was in issue with the received data. Received the following raw data: ", data)
        elif request.is_ca_request():
            username = request.data["username"]
            print("New request. Username: " + str(username))  
            if CA_Database.username_exists(username):
                print("Username " + username + " exists in the CA database.")
                ca_response = Requests.ca_response_invalid()
                c.send(ca_response)
            else:
                public_key_b64 = request.data["public_key"].encode()[2:-1]
                public_key = base64.b64decode(public_key_b64)
                message = username + "," + public_key.decode()
                ca_signature = Crypto_Functions.rsa_sign(message.encode(), self.private_key)
                ca_signature_b64 = base64.b64encode(ca_signature)
                ca_response = Requests.ca_response_valid(username, request.data["public_key"], str(ca_signature_b64))
                print("Signed public key for the user: " + username)
                print("Adding user info to the CA database.")
                CA_Database.add_user(username, request.data["public_key"], str(ca_signature_b64))
                print("Sending the signature back to the client.")
                c.send(ca_response)
        elif request.is_send_email():
            username = request.data["username"]
            print("CA received email: " + username)
            self.send_email(username)
    
        elif request.is_verify_email():
            code = request.data["code"]
            if (self.verify_code(code)):
                ca_response = Requests.ca_response_email_valid()
                c.send(ca_response)
            else:
                ca_response = Requests.ca_response_email_invalid()
                c.send(ca_response)

    def verify_code(self, verification_code):
        return str(verification_code) == str(self.code)


    def send_email(self, email):
        try:
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.ehlo()
            self.server.starttls()
            self.server.login(CA_EMAIL,CA_PASS)
        except Exception as e:
            print("Unable to login to system email.")
            return False 
    
        self.code = self.get_verification_code() 
        msg = MIMEMultipart()
        msg['From'] = CA_EMAIL
        msg['To'] = email
        msg['Subject'] = 'Accord Webchat Verification Code'

        body = 'A request for account creation in Accord was sent to this email. Verification Code: ' + str(self.code)
        msg.attach(MIMEText(body,'plain'))
        text = msg.as_string()
    
        self.server.sendmail(CA_EMAIL,email,text)
        self.server.quit()
    
    def get_verification_code(self):
        r = random.randint(100000, 999999)
        return r

ca = CertAuth()