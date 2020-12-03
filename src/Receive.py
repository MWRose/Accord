from sqlite3.dbapi2 import Timestamp
import Crypto_Functions
import base64
import Requests
import datetime

def receive_direct(data, contacts, received_timestamps):
    '''
    Receiving direct private messages.
    Does necessary message conversion and checking then prints output
    '''

    sender = data["sender"]

    # Decode messages
    enc_msg_b64 = data["message"].encode()[2:-1]
    iv_b64 = data["iv"].encode()[2:-1]
    enc_msg = base64.b64decode(enc_msg_b64)
    iv = base64.b64decode(iv_b64)

    # Get shared key
    aes_key = contacts[sender]["aes_key"]
    hmac_key = contacts[sender]["hmac_key"]

     # Get timestamp
    msg_timestamp = data["timestamp"]
    current_timestamp = datetime.datetime.now().timestamp()

    # Check if the timestamp is accurate. If exceeds 20 seconds, then is deemed a replay
    if current_timestamp - float(msg_timestamp) > 20:
        print("Large difference in time sent and time recieved. Message was not received.")
        return

    
    # Check if the timestamp was already seen
    if msg_timestamp in received_timestamps and received_timestamps[msg_timestamp] == sender:
        print("There was an attempt at a replay attack, the message will not be viewed")
        return
    received_timestamps[msg_timestamp] = sender

    # Check tag
    tag = data["tag"]
    tag = base64.b64decode(tag.encode()[2:-1])
    tag_contents = str(base64.b64encode(enc_msg)) + msg_timestamp
    valid = Crypto_Functions.check_hmac_b64(tag_contents.encode(), tag, hmac_key)
    if not valid:
        raise Exception("HMAC not valid")

    # Decrypt message
    decrypted_msg = Crypto_Functions.aes_decrypt(enc_msg, iv, aes_key)

    print(sender + ": " + decrypted_msg)

    return msg_timestamp


def receive_group(data, groups, received_timestamps):
    '''
    Receiving group messages.
    Does necessary message conversion and checking then prints output
    '''

    sender = data["sender"]
    group_name = data["group_name"]

    # Decode messages
    enc_msg_b64 = data["message"].encode()[2:-1]
    iv_b64 = data["iv"].encode()[2:-1]
    enc_msg = base64.b64decode(enc_msg_b64)
    iv = base64.b64decode(iv_b64)

    # Get shared key
    aes_key = groups[group_name]["aes_key"]
    hmac_key = groups[group_name]["hmac_key"]

    # Get timestamp
    msg_timestamp = data["timestamp"]
    current_timestamp = datetime.datetime.now().timestamp()

    # Check if the timestamp is accurate
    if current_timestamp - float(msg_timestamp) > 20:
        print("Large difference in time sent and time recieved. Message was not received.")
        return

    # Check if the timestamp was already seen
    if msg_timestamp in received_timestamps and received_timestamps[msg_timestamp] == sender:
        # print("There was an attempt at a replay attack, the message will not be viewed")
        return
    received_timestamps[msg_timestamp] = sender
    
    # Check tag
    tag = data["tag"]
    tag = base64.b64decode(tag.encode()[2:-1])
    tag_contents = str(base64.b64encode(enc_msg)) + msg_timestamp
    valid = Crypto_Functions.check_hmac_b64(tag_contents.encode(), tag, hmac_key)
    if not valid:
        raise Exception("Tag not valid")

    # Decrypt message
    decrypted_msg = Crypto_Functions.aes_decrypt(enc_msg, iv, aes_key)

    print(sender + " to " + data["group_name"] + ": " + decrypted_msg)

def receive_direct_handshake(data, contacts, sender_public_key, recipient_private_key):
    '''
    Receiving direct private message handshake.
    Does not update directly
    '''

    sender = data["requester"]
    recipient = data["recipient"]
    encrypted_b64 = data["encrypted"]
    signed_b64 = data["signed"]

    encrypted = base64.b64decode(encrypted_b64.encode()[2:-1])
    signed = base64.b64decode(signed_b64.encode()[2:-1])

    signature_contents = (sender + recipient + str(encrypted_b64)).encode()
    if not Crypto_Functions.rsa_check_sign(signature_contents, signed, sender_public_key):
        print("Invalid signature")
        return {}
        
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


def receive_group_handshake(data,sender,groups,contacts,private_key):
    '''
    Receiving handshake from group message.
    Does not update directly
    '''

    if sender in data["recipients"].split(","):
        # Parsed message contents
        requester = data["requester"]
        encrypted_b64 = data["encrypted"]
        signed_b64 = data["signed"]
    
        encrypted = base64.b64decode(encrypted_b64.encode()[2:-1])
        signed = base64.b64decode(signed_b64.encode()[2:-1])

        # Check the signature
        members = data["recipients"].split(",")
        signature_contents = (requester + ",".join(members) + str(encrypted_b64)).encode()
        if not Crypto_Functions.rsa_check_sign(signature_contents, signed, contacts[requester]["public_key"]):
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
            return {"aes":aes_key, "hmac": hmac_key, "members": members, "group_name":group_name}

    else:
        print("User doesn't match intended recipient")

    return {}