from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256, HMAC
from Crypto.Signature import pkcs1_15
from Crypto.Random import get_random_bytes

from typing import Tuple


def generate_session_key() -> bytes:
    return get_random_bytes(16)


def aes_encrypt(msg_str: str, aes_key: bytes) -> Tuple[bytes, bytes]:
    """
    Takes msg and encrypts it under aes_key using AES-256 CBC
    """

    msg = msg_str.encode()
    cipher = AES.new(aes_key, AES.MODE_CBC)
    enc_msg = cipher.encrypt(pad(msg, AES.block_size))
    iv = cipher.iv
    
    return enc_msg, iv


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


def rsa_sign(msg: bytes, private_key: bytes) -> bytes:
    """
    Takes msg and uses private_key to sign it with RSA
    """

    key = RSA.import_key(private_key)
    h = SHA256.new()
    h.update(msg)
    return pkcs1_15.new(key).sign(h)


def rsa_check_sign(msg: bytes, signature: bytes, public_key: bytes) -> bool:
    """
    Takes msg and uses public_key to check the signature
    """

    valid = False
    key = RSA.import_key(public_key)
    h = SHA256.new()
    h.update(msg)

    try:
        pkcs1_15.new(key).verify(h, signature)
        print("valid")
        valid = True
    except (ValueError, TypeError):
        valid = False
        print("not valid")

    return valid
    


