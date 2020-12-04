import Crypto_Functions
import Gen
import unittest
import os
import base64


class TestCryptoFunctions(unittest.TestCase):

    def test_generate_session_key(self):
        keys = {}
        for i in range(20):
            key = Crypto_Functions.generate_session_key()
            self.assertFalse(key in keys)
            keys[key] = None
    
    def test_aes(self):
        key_one = Crypto_Functions.generate_session_key()
        key_two = Crypto_Functions.generate_session_key()
        input_msg = "Hello"

        # Correct Decryption
        encrypted, iv = Crypto_Functions.aes_encrypt(input_msg, key_one)
        output_msg = Crypto_Functions.aes_decrypt(encrypted, iv, key_one)
        self.assertEqual(input_msg, output_msg)

        # Incorrect Decryption
        with self.assertRaises(ValueError):
            Crypto_Functions.aes_decrypt(encrypted, iv, key_two)

    def test_rsa(self):
        key_one = Gen.generate_key_pair("unittest1")
        key_two = Gen.generate_key_pair("unittest2")

        f = open('private_unittest1.pem',  'rb')
        private_key_one = f.read()
        f.close()

        f = open('public_unittest1.pem', 'rb')
        public_key_one = f.read()
        f.close()

        f = open('private_unittest2.pem', 'rb')
        private_key_two = f.read()
        f.close()

        input_msg = "Hello There"

        # Correct Decryption
        encrypted_msg = Crypto_Functions.rsa_encrypt(input_msg, public_key_one)
        output_msg = Crypto_Functions.rsa_decrypt(encrypted_msg, private_key_one)
        self.assertEqual(input_msg, output_msg)

        # Incorrect Decryption
        with self.assertRaises(ValueError):
            Crypto_Functions.rsa_decrypt(encrypted_msg, private_key_two)

        os.remove("private_unittest1.pem")
        os.remove("public_unittest1.pem")
        os.remove("private_unittest2.pem")
        os.remove("public_unittest2.pem")
        

    def test_rsa_sign(self):
        key_one = Gen.generate_key_pair("unittest1")
        key_two = Gen.generate_key_pair("unittest2")

        f = open('private_unittest1.pem',  'rb')
        private_key_one = f.read()
        f.close()

        f = open('public_unittest1.pem', 'rb')
        public_key_one = f.read()
        f.close()

        f = open('private_unittest2.pem', 'rb')
        private_key_two = f.read()
        f.close()

        input_msg = b"Hello There"

        # Correct checking of signature
        sign = Crypto_Functions.rsa_sign(input_msg, private_key_one)
        self.assertTrue(Crypto_Functions.rsa_check_sign(b"Hello There", sign, public_key_one))

        # Incorrect msg
        sign = Crypto_Functions.rsa_sign(input_msg, private_key_one)
        self.assertFalse(Crypto_Functions.rsa_check_sign(b"Hello", sign, public_key_one))

        # Incorrect checking of signature
        sign = Crypto_Functions.rsa_sign(input_msg, private_key_two)
        self.assertFalse(Crypto_Functions.rsa_check_sign(b"Hello There", sign, public_key_one))

        

    def test_hash_keys(self):
        key = Crypto_Functions.generate_session_key()

        key1, key2 = Crypto_Functions.hash_keys(key)

        self.assertNotEqual(key1, key2, key)
        self.assertEqual([len(key), len(key1), len(key2)], [32,32,32])

    def test_hmac(self):
        key_one = Crypto_Functions.generate_session_key()
        key_two = Crypto_Functions.generate_session_key()

        msg = b"Hello There"

        # Correct
        tag = Crypto_Functions.hmac(msg, key_one)
        self.assertTrue(Crypto_Functions.check_hmac(msg, tag, key_one))

        # Incorrect
        tag = Crypto_Functions.hmac(msg, key_two)
        self.assertFalse(Crypto_Functions.check_hmac(msg, tag, key_one))

        tag = Crypto_Functions.hmac(msg, key_one)
        self.assertFalse(Crypto_Functions.check_hmac(b"Hello", tag, key_one))


    def test_hmac_b64(self):
        key_one = Crypto_Functions.generate_session_key()
        key_two = Crypto_Functions.generate_session_key()

        msg = b"Hello There"

        # Correct
        tag = Crypto_Functions.hmac_b64(msg, key_one)
        tag = base64.b64decode(tag)
        self.assertTrue(Crypto_Functions.check_hmac_b64(msg, tag, key_one))

        # Incorrect
        tag = Crypto_Functions.hmac_b64(msg, key_two)
        tag = base64.b64decode(tag)
        self.assertFalse(Crypto_Functions.check_hmac_b64(msg, tag, key_one))

        tag = Crypto_Functions.hmac_b64(msg, key_one)
        tag = base64.b64decode(tag)
        self.assertFalse(Crypto_Functions.check_hmac_b64(b"Hello", tag, key_one))

if __name__ == '__main__':
    unittest.main()