import unittest
import os

class TestPrivateMessaging(unittest.TestCase):
    def setup_testenv(self):
        # # aes, hmac, public examples
        # Client.client.contacts = {"test1": , "test2": }
        # run_server = os.system("cd ..")
        run_server = os.system("python3 Server.py 5000")
        # run_client1 = subprocess.run(["python3 Client.py #IP 5000"])
        # run_client2 = subprocess.run(["python3 Client.py #IP 5000"])

    def test_initiate_private_message(self):
        self.setup_testenv()

    def test_existing_private_message(self):
        self.setup_testenv()


    def test_wrong_recipient(self): 
        self.setup_testenv()

    
    
if __name__ == '__main__':
    unittest.main()