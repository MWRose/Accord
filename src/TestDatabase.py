import unittest
import Database
import os
class TestDatabase(unittest.TestCase):

    
    def test_username_database(self):
        #init database
        Database.initialize_username_database()

        #populate and check 
        self.assertEqual(Database.get_all_users(),[])
        self.assertTrue(Database.add_user_info("user1@email.com","PUBLICKEY","CASIGNATURE"))
        self.assertTrue(Database.check_user("user1@email.com"))
        
        #check all
        dc = Database.get_all_users()
        self.assertEqual(dc,[{"user":"user1@email.com","public_key":"PUBLICKEY","ca_signature":"CASIGNATURE"}])
        
        #overwrite
        self.assertTrue(Database.add_user_info("user1@email.com","NEWKEY","NEWCASIGNATURE"))
        
        #test overwrite
        dc = Database.get_user_info("user1@email.com")
        self.assertEqual(dc,{"user":"user1@email.com","public_key":"NEWKEY","ca_signature":"NEWCASIGNATURE"})
        
        #check user that does not exist in the database
        dc = Database.get_user_info("use2@email.com")
        self.assertEqual(dc,{})
        
        #delete test database
        os.remove("Accord.db")

    def test_saved_accounts_database(self):
        #init database
        Database.initialize_saved_accounts_database()
        
        #populate the database
        self.assertTrue(Database.add_user_account("user1@email.com","PRIVKEY1"))
        self.assertTrue(Database.add_user_account("user2@email.com","PRIVKEY2"))
        
        #check if correctly populated
        ls = Database.get_user_accounts()
        self.assertEqual(ls,[{"user":"user1@email.com","private_key":"PRIVKEY1"},{"user":"user2@email.com","private_key":"PRIVKEY2"}])
        
        #overwrite
        self.assertTrue(Database.add_user_account("user1@email.com","NEW_PRIVKEY1"))
        
        #test overwrite
        ls = Database.get_user_accounts()
        self.assertEqual(ls,[{"user":"user2@email.com","private_key":"PRIVKEY2"},{"user":"user1@email.com","private_key":"NEW_PRIVKEY1"}])
        
        #populate contacts for user1
        self.assertTrue(Database.add_contact_info(
            "user1","contact1","contact_aes1","signature1","iv_aes1","hmac_key1","iv_hmac1"))
        self.assertTrue(Database.add_contact_info(
            "user1","contact2","contact_aes2","signature2","iv_aes2","hmac_key2","iv_hmac2","public_key2"))
        
        #check if populate correct
        contacts = Database.get_user_contact_info("user1")
        self.assertEqual(contacts[1]["contact_aes"],"contact_aes2")

        #overwrite and check
        self.assertTrue(Database.add_contact_info(
            "user1","contact2","contact_aes_new2","signature2","iv_aes2","hmac_key2","iv_hmac2","public_key2"))
        contacts = Database.get_user_contact_info("user1")
        self.assertEqual(contacts[1]["contact_aes"],"contact_aes_new2")

        #check user not a list 
        contacts = Database.get_user_contact_info("user2")
        self.assertEqual(contacts,[])

        #remove temp database
        os.remove("Accord_saved_accounts.db")

    def test_group_database(self):
        #init database
        Database.initialize_groups_database()

        #populate group_one
        self.assertTrue(Database.add_group("group_one",["a","b","c"],"aes_key_one"))

        #populate group_two
        self.assertTrue(Database.add_group("group_two",["b","d"],"aes_key_two"))

        #check group_two participants
        self.assertEqual(Database.get_group_participants("group_two"),[{"group_name":"group_two","username":"b","aes_key":"aes_key_two"},{"group_name":"group_two","username":"d","aes_key":"aes_key_two"}])
        
        #check user b's groups
        self.assertEqual(Database.get_username_groups("b"),[{"group_name":"group_one","username":"b","aes_key":"aes_key_one"},{"group_name":"group_two","username":"b","aes_key":"aes_key_two"}])
        os.remove("Accord_groups.db")


if __name__ == '__main__':
    unittest.main()

    