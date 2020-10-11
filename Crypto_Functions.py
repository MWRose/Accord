from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad


def aes_encrypt(msg_str: str, iv: bytes, aes_key: bytes) -> bytes:
    """
    Takes msg and encrypts it under aes_key using AES-256 CBC
    """

    msg = msg_str.encode()
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    enc_msg = cipher.encrypt(pad(msg, AES.block_size))
    
    return enc_msg


def aes_decrypt(enc_msg: bytes, iv: bytes, aes_key: bytes) -> str:
    """
    Takes enc_msg and decrypts it with aes_key using AES-256 CBC
    """

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    msg = unpad(cipher.decrypt(enc_msg), AES.block_size)
    
    return msg.decode()


def rsa_encrypt(msg_str: str, public_key: bytes) -> bytes:
    """
    Takes msg and encrypts it under public_key
    """
    
    msg = msg_str.encode()
    key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    msg_enc = cipher_rsa.encrypt(msg)

    return msg_enc


def rsa_decrypt(enc_msg: bytes, private_key: bytes) -> str:
    """
    Takes enc_msg and decrypts it with private_key
    """

    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    msg = cipher_rsa.decrypt(enc_msg)

    return msg.decode()