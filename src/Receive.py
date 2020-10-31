import Crypto_Functions
import base64
import Requests

def receive_direct(data, contacts):
    '''Receiving direct private messages '''
    sender = data["sender"]

    # Decode messages
    enc_msg_b64 = data["message"].encode()[2:-1]
    iv_b64 = data["iv"].encode()[2:-1]
    enc_msg = base64.b64decode(enc_msg_b64)
    iv = base64.b64decode(iv_b64)

    # Get shared key
    aes_key = contacts[sender]["aes"]
    hmac_key = contacts[sender]["hmac"]

    # Check tag
    tag = data["tag"]
    valid = Crypto_Functions.check_hmac(enc_msg, tag, hmac_key)
    if not valid:
        raise Exception("AHHHH")

    # Decrypt message
    decrypted_msg = Crypto_Functions.aes_decrypt(enc_msg, iv, aes_key)

    return sender + ": " + decrypted_msg


def receive_group(data, groups):
    '''Receiving group messages '''
    sender = data["sender"]

    # Decode messages
    enc_msg_b64 = data["message"].encode()[2:-1]
    iv_b64 = data["iv"].encode()[2:-1]
    enc_msg = base64.b64decode(enc_msg_b64)
    iv = base64.b64decode(iv_b64)

    # Get shared key
    aes_key = groups[sender]["aes"]
    hmac_key = groups[sender]["hmac"]
    
    # Check tag
    tag = data["tag"]
    valid = Crypto_Functions.check_hmac(enc_msg, tag, hmac_key)
    if not valid:
        raise Exception("AHHHH")

    # Decrypt message
    decrypted_msg = Crypto_Functions.aes_decrypt(enc_msg, iv, aes_key)

    return sender + " to " + data["group_name"] + ": " + decrypted_msg

def receive_direct_handshake(data, contacts, sender_public_key, recipient_private_key):
    '''receiving direct private message handshake'''
    sender = data["requester"]
    encrypted_b64 = data["encrypted"]
    signed_b64 = data["signed"]

    encrypted = base64.b64decode(encrypted_b64.encode()[2:-1])
    signed = base64.b64decode(signed_b64.encode()[2:-1])

    signature_contents = (sender + recipient + str(encrypted_b64)).encode()
    if not Crypto_Functions.rsa_check_sign(signature_contents, signed, sender_public_key):
        print("Invalid signature")
    else:
            # Parse encrpyted message
        decrypted_msg = Crypto_Functions.rsa_decrypt(encrypted, recipient_private_key)
        decrypted_msg_split = decrypted_msg.split(",", 2)

        # Check the contents of the sender and re
        enc_sender = decrypted_msg_split[0]
        enc_recipient = decrypted_msg_split[1]

        key_b64 = decrypted_msg_split[2].encode()[2:-1]
        key = base64.b64decode(key_b64)

        # Transform key into two keys
        aes_key, hmac_key = Crypto_Functions.hash_keys(key)
    
    return {"aes":aes_key, "hmac": hmac_key}


def receive_group_handshake(data,sender,groups,private_key):
    '''receiving handshake from group message'''
    if (sender in data["recipients"].split(",")) or sender == data["recipient"]:
        # Parsed message contents
        requester = data["requester"]
        encrypted_b64 = data["encrypted"]
        signed_b64 = data["signed"]

        encrypted = base64.b64decode(encrypted_b64.encode()[2:-1])
        signed = base64.b64decode(signed_b64.encode()[2:-1])

        # Check the signature
        recipient = data["recipients"] if is_group else data["recipient"]
        signature_contents = (requester + recipient + str(encrypted_b64)).encode()
        if not Crypto_Functions.rsa_check_sign(signature_contents, signed, group[requester]["public_key"]):
            print("Invalid signature")
        else:
            # Parse encrpyted message
            decrypted_msg = Crypto_Functions.rsa_decrypt(encrypted, private_key)
            decrypted_msg_split = decrypted_msg.split(",", 2)

            # Check the contents of the sender and re
            enc_sender = decrypted_msg_split[0]
            enc_recipient = decrypted_msg_split[1]

            key_b64 = decrypted_msg_split[2].encode()[2:-1]
            key = base64.b64decode(key_b64)

            # Transform key into two keys
            aes_key, hmac_key = Crypto_Functions.hash_keys(key)

            group_name = data["group_name"]
            members = data["members"].split(",")
            return {"aes":aes_key, "hmac": hmac_key, "members": members, "group_name":group_name}

    else:
        print("User doesn't match intended recipient")

    return {}