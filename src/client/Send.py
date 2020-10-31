import Crypto_Functions    
    
def send_direct_handshake(sender, recipient, socket, sender_private_key, recipient_public_key):
    # Message contents
    key = Crypto_Functions.generate_session_key()

    # RSA encrypt the msg
    key_b64 = base64.b64encode(key)
    encrypt_msg = sender + "," + recipient + "," + str(key_b64)
    encrypted = Crypto_Functions.rsa_encrypt(encrypt_msg, recipient_public_key)
    encrypted_b64 = base64.b64encode(encrypted)

    # Create a signature for the message contents
    signature = (sender + recipient + str(encrypted_b64)).encode()
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
    encrypt_msg = sender + "," + recipient + "," + str(key_b64)
    encrypted = Crypto_Functions.rsa_encrypt(encrypt_msg, recipient_public_key)
    encrypted_b64 = base64.b64encode(encrypted)

    # Create a signature for the message contents
    signature = (sender + ",".join(members) + str(encrypted_b64)).encode()
    signed = Crypto_Functions.rsa_sign(signature, sender_private_key)
    signed_b64 = base64.b64encode(signed)

    # Transform key into two keys
    aes_key, hmac_key = Crypto_Functions.hash_keys(key)

    request = Requests.initiate_group_chat(sender, ",".join(members), str(encrypted_b64), str(signed_b64))
    socket.send(request)

    return {"aes": aes_key, "hmac": hmac_key}

# NOTE: Note used, can be deleted
def send_group(group_names, recipient):
    # Send a handshake to each member in the group
    for recipient in group_names:
    send_handshake(True)
    recipient = ""
    send_msg_group()

def send_group_message(message, sender, recipient, group_name, socket, group_members):
    # Get shared key
    aes_key = groups[group_name]["aes"]
    hmac_key = groups[group_name]["hmac"]

    # Encrypt
    enc_msg, iv = Crypto_Functions.aes_encrypt(msg, aes_key)

    # Create message tag on encypted data
    tag = Crypto_Functions.hmac(enc_msg, hmac_key)

    # Encoding
    enc_msg_b64 = base64.b64encode(enc_msg)
    iv_b64 = base64.b64encode(iv)

    socket.send(Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), tag))

def send_direct(recipient, contacts, message, socket):
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

    socket.send(Requests.message(username, recipient, str(enc_msg_b64), str(iv_b64), tag))