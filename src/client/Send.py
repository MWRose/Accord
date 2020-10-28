import Crypto_Functions    
    
def send_direct_handshake(self, sender, recipient, socket, sender_private_key, recipient_public_key):
    # Message contents
    key = Crypto_Functions.generate_session_key()

    # RSA encrypt the msg
    key_b64 = base64.b64encode(key)
    encrypt_msg = username + "," + recipient + "," + str(key_b64)
    encrypted = Crypto_Functions.rsa_encrypt(encrypt_msg, recipient_public_key)
    encrypted_b64 = base64.b64encode(encrypted)

    # Create a signature for the message contents
    signature = (username + recipient + str(encrypted_b64)).encode()
    signed = Crypto_Functions.rsa_sign(signature, sender_private_key)
    signed_b64 = base64.b64encode(signed)

    # Transform key into two keys
    aes_key, hmac_key = Crypto_Functions.hash_keys(key)
    
    request = Requests.initiate_direct_message(sender, recipient, str(encrypted_b64), str(signed_b64))
    socket.send(request)
    
    return {"aes": aes_key, "hmac": hmac_key}

def send_group_handshake(sender, recipient, members, socket, sender_private_key, recipient_public_key):
    # Message contents
    key = Crypto_Functions.generate_session_key()

    # RSA encrypt the msg
    key_b64 = base64.b64encode(key)
    encrypt_msg = username + "," + recipient + "," + str(key_b64)
    encrypted = Crypto_Functions.rsa_encrypt(encrypt_msg, recipient_public_key)
    encrypted_b64 = base64.b64encode(encrypted)

    # Create a signature for the message contents
    signature = (username + ",".join(members) + str(encrypted_b64)).encode()
    signed = Crypto_Functions.rsa_sign(signature, sender_private_key)
    signed_b64 = base64.b64encode(signed)

    # Transform key into two keys
    aes_key, hmac_key = Crypto_Functions.hash_keys(key)

    request = Requests.initiate_group_chat(sender, ",".join(members), str(encrypted_b64), str(signed_b64))
    socekt.send(request)

    return {"aes": aes_key, "hmac": hmac_key}

def send_group():
    # Send a handshake to each member in the group
    for recipient in self.group_names:
        self.populate_public_keys(recipient)
        
    self.send_handshake(True)
    self.recipient = ""
    send_msg_group()

def send_msg_group(message, groups, recipient_group):  
    # Get shared key
    aes_key = groups[recipient_group]["aes"]
    hmac_key = groups[recipient_group]["hmac"]

    # Encrypt
    enc_msg, iv = Crypto_Functions.aes_encrypt(msg, aes_key)

    # Create message tag on encypted data
    tag = Crypto_Functions.hmac(enc_msg, hmac_key)

    # Encoding
    enc_msg_b64 = base64.b64encode(enc_msg)
    iv_b64 = base64.b64encode(iv)

    self.s.send(Requests.group_message(self.username, ",".join(self.group_names), self.recipient_group, str(enc_msg_b64), str(iv_b64), tag)) 

def send_direct(recipient, contacts, message):
    # Get shared key
    aes_key = contacts[recipient]["aes"]
    hmac_key = contacts[recipient]["hmac"]

    # Encrypt
    enc_msg, iv = Crypto_Functions.aes_encrypt(msg, aes_key)

    # Create message tag on encypted data
    tag = Crypto_Functions.hmac(enc_msg, hmac_key)

    # Encoding
    enc_msg_b64 = base64.b64encode(enc_msg)
    iv_b64 = base64.b64encode(iv)

    self.s.send(Requests.message(username, recipient, str(enc_msg_b64), str(iv_b64), tag))