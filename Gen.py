from Crypto.PublicKey import RSA

def generate_key_pair(name: str):
    """
    Generates a new RSA key pair and stores the private key in private_name.pem
    and public key in public_name.pem
    """
    # Generate RSA key pair
    key_pair = RSA.generate(2048)
    # Write private key to private_name.pem
    file = open('private_{}.pem'.format(name), 'wb')
    file.write(key_pair.export_key('PEM'))
    file.close()
    # Write public key to public_name.pem
    pubkey = key_pair.publickey()
    f = open('public_{}.pem'.format(name), 'wb')
    f.write(pubkey.exportKey('PEM'))
    f.close()