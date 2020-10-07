# Generate RSA key pair and write them to files on disk
key_pair = RSA.generate(2048)
file = open('private.pem', 'wb')
file.write(key_pair.export_key('PEM'))
file.close()

pubkey = key_pair.publickey()
f = open('public.pem', 'wb')
f.write(pubkey.exportKey('PEM'))
f.close()

# Load public key from a file on disk and encrypt data
f = open("public.pem", "rb")
key = RSA.import_key(f.read())
cipher_rsa = PKCS1_OAEP.new(key)
encrypted_data = cipher_rsa.encrypt(data)

# Write encrypted data to a file on disk
f = open("secret.pem", "wb")
f.write(enc_session_key)
f.close()

# Load private key from a file on disk
f = open("private.pem", "rb")
encoded_key = f.read()
key = RSA.import_key(encoded_key)
cipher_rsa = PKCS1_OAEP.new(key)
f.close

# Decrypt data stored in a file
f = open("secret.pem", "rb")
data = f.read()
f.close
return cipher_rsa.decrypt(data)