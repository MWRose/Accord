import Crypto_Functions
import base64    
import Requests
import socket
import sys
import datetime

def send_direct_handshake(sender, recipient, s, sender_private_key, recipient_public_key):
    """"
    Send the direct handshake to a user.
    Does not update anything directly.
    """
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
    s.send(request)
    
    return {"aes": aes_key, "hmac": hmac_key}

def send_group_handshake(sender, recipient, members, s, sender_private_key, recipient_public_key, key, group_name):
    """
    Send a handshake to each group member.
    Does not update anything directly
    """

    # RSA encrypt the msg
    key_b64 = base64.b64encode(key)
    encrypt_msg = sender + "," + "_".join(members) + "," + str(key_b64)
    encrypted = Crypto_Functions.rsa_encrypt(encrypt_msg, recipient_public_key)
    encrypted_b64 = base64.b64encode(encrypted)

    # Create a signature for the message contents
    signature = (sender + ",".join(members) + str(encrypted_b64)).encode()
    signed = Crypto_Functions.rsa_sign(signature, sender_private_key)
    signed_b64 = base64.b64encode(signed)

    # Transform key into two keys
    aes_key, hmac_key = Crypto_Functions.hash_keys(key)

    request = Requests.initiate_group_chat(sender, recipient, ",".join(members), str(encrypted_b64), str(signed_b64), group_name)
    s.send(request)

    return {"aes": aes_key, "hmac": hmac_key}

def send_group_message(message, sender, group_name, s, group_members, groups):
    """
    Send a message to each member in the group.
    This is done through one send request
    """
    # Get shared key
    aes_key = groups[group_name]["aes_key"]
    hmac_key = groups[group_name]["hmac_key"]

    # Encrypt
    enc_msg, iv = Crypto_Functions.aes_encrypt(message, aes_key)
    
    # Create message tag on encypted data
    timestamp = str(datetime.datetime.now().timestamp())
    tag_contents = str(base64.b64encode(enc_msg)) + timestamp
    tag = Crypto_Functions.hmac_b64(tag_contents.encode(), hmac_key)

    # Encoding
    enc_msg_b64 = base64.b64encode(enc_msg)
    iv_b64 = base64.b64encode(iv)

    s.send(Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), timestamp, str(tag)))

def send_direct(sender, recipient, contacts, message, s):
    """
    Sends an encrypted direct message to the recipient.
    """
    # Get keys
    aes_key = contacts[recipient]["aes_key"]
    hmac_key = contacts[recipient]["hmac_key"]

    # Encrypt
    enc_msg, iv = Crypto_Functions.aes_encrypt(message, aes_key)

    # Create message tag on encypted data
    timestamp = str(datetime.datetime.now().timestamp())
    tag_contents = str(base64.b64encode(enc_msg)) + timestamp
    tag = Crypto_Functions.hmac_b64(tag_contents.encode(), hmac_key)

    # Encoding
    enc_msg_b64 = base64.b64encode(enc_msg)
    iv_b64 = base64.b64encode(iv)

    s.send(Requests.direct_message(sender, recipient, str(enc_msg_b64), str(iv_b64), timestamp, str(tag)))