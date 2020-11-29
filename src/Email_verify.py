import smtplib
import re 
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):
        return True
    else:
        return False 

def get_verification_code():
    r = random.randint(100000, 999999)
    return r
    
if __name__ == '__main__' :
    CA_EMAIL = 'accord_no_reply_register@outlook.com'
    CA_PASS = 'acccord123@'
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com','587')
        server.starttls()
        server.login(CA_EMAIL,CA_PASS)
    except Exception as e:
        print(e)
        pass 
    
    while True: 
        email = input("Enter an email:")
        if check(email):
            code = get_verification_code() 
            msg = MIMEMultipart()
            msg['From'] = CA_EMAIL
            msg['To'] = email
            msg['Subject'] = 'Accord Webchat Verification Code'

            body = 'A request for account an creation in Accord was sent to this email. Verification Code: ' + str(code)
            msg.attach(MIMEText(body,'plain'))
            text = msg.as_string()
            server.sendmail(CA_EMAIL,email,text)
            verification_code = input("Please enter verification number sent to this email address: ")
            if str(verification_code) == str(code):
                print("Account Creation Succesful")
        else:
            print("Email not valid")