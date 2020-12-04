import unittest
import Database
import os


class TestDatabase(unittest.TestCase):

    def test_username_database(self):
        # init database
        Database.initialize_username_database()

        # populate and check
        self.assertEqual(Database.get_all_users(), [])
        self.assertTrue(Database.add_user_info("user1@email.com", "PUBLICKEY", "CASIGNATURE"))
        self.assertTrue(Database.check_user("user1@email.com"))

        # check all
        dc = Database.get_all_users()
        self.assertEqual(dc, [{"user": "user1@email.com", "public_key": "PUBLICKEY", "ca_signature": "CASIGNATURE"}])

        # overwrite
        self.assertTrue(Database.add_user_info("user1@email.com", "NEWKEY", "NEWCASIGNATURE"))

        # test overwrite
        dc = Database.get_user_info("user1@email.com")
        self.assertEqual(dc, {"user": "user1@email.com", "public_key": "NEWKEY", "ca_signature": "NEWCASIGNATURE"})

        # check user that does not exist in the database
        dc = Database.get_user_info("use2@email.com")
        self.assertEqual(dc, {})

        # delete test database
        os.remove("Accord.db")

    def test_saved_accounts_database(self):
        # init database
        Database.initialize_saved_accounts_database()

        # populate the database
        self.assertTrue(Database.add_user_account("user1@email.com", "PRIVKEY1", "IV1", "TAG1"))
        self.assertTrue(Database.add_user_account("user2@email.com", "PRIVKEY2", "IV2", "TAG2"))

        # check if correctly populated
        ls = Database.get_user_accounts()
        self.assertEqual(ls, [{"user": "user1@email.com", "private_key": "PRIVKEY1", "aes_iv": "IV1", "hmac": "TAG1"},
                              {"user": "user2@email.com", "private_key": "PRIVKEY2", "aes_iv": "IV2", "hmac": "TAG2"}])

        # overwrite
        self.assertTrue(Database.add_user_account("user1@email.com", "NEWPRIVKEY1", "IV1", "TAG1"))

        # test overwrite
        ls = Database.get_user_accounts()
        self.assertEqual(ls, [{"user": "user2@email.com", "private_key": "PRIVKEY2", "aes_iv": "IV2", "hmac": "TAG2"},
                              {"user": "user1@email.com", "private_key": "NEWPRIVKEY1", "aes_iv": "IV1",
                               "hmac": "TAG1"}])

        # populate contacts for user1
        self.assertTrue(Database.add_contact_info(
            "user1", "contact1", "contact_aes1", "signature1", "iv_aes1", "hmac_key1", "iv_hmac1"))
        self.assertTrue(Database.add_contact_info(
            "user1", "contact2", "contact_aes2", "signature2", "iv_aes2", "hmac_key2", "iv_hmac2", "public_key2"))

        # check if populate correct
        contacts = Database.get_user_contact_info("user1")
        self.assertEqual(contacts[1]["contact_aes"], "contact_aes2")

        # overwrite and check
        self.assertTrue(Database.add_contact_info(
            "user1", "contact2", "contact_aes_new2", "signature2", "iv_aes2", "hmac_key2", "iv_hmac2", "public_key2"))
        contacts = Database.get_user_contact_info("user1")
        self.assertEqual(contacts[1]["contact_aes"], "contact_aes_new2")

        # check user not a list
        contacts = Database.get_user_contact_info("user2")
        self.assertEqual(contacts, [])

        # remove temp database
        os.remove("Accord_saved_accounts.db")

    def test_group_database(self):
        # init database
        Database.initialize_groups_database()

        # populate group_one
        self.assertTrue(
            Database.add_group("group_one", "a", "sign1", "aes_key_one", "aes_iv1", "hmac_key1", "hmac_iv1"))
        self.assertTrue(
            Database.add_group("group_one", "b", "sign1", "aes_key_one", "aes_iv1", "hmac_key1", "hmac_iv1"))
        self.assertTrue(
            Database.add_group("group_one", "c", "sign1", "aes_key_one", "aes_iv1", "hmac_key1", "hmac_iv1"))

        # populate group_two
        self.assertTrue(
            Database.add_group("group_two", "b", "sign2", "aes_key_two", "aes_iv2", "hmac_key2", "hmac_iv2"))
        self.assertTrue(
            Database.add_group("group_two", "d", "sign2", "aes_key_two", "aes_iv2", "hmac_key2", "hmac_iv2"))

        # check group_two participants
        self.assertEqual(Database.get_group_participants("group_two"), [
            {"group_name": "group_two", "participant": "b", "signature": "sign2", "aes_key": "aes_key_two",
             "aes_iv": "aes_iv2", "hmac_key": "hmac_key2", "hmac_iv": "hmac_iv2"},
            {"group_name": "group_two", "participant": "d", "signature": "sign2", "aes_key": "aes_key_two",
             "aes_iv": "aes_iv2", "hmac_key": "hmac_key2", "hmac_iv": "hmac_iv2"}])

        # check user b's groups
        self.assertEqual(Database.get_username_groups("b"), [
            {"group_name": "group_one", "participant": "b", "signature": "sign1", "aes_key": "aes_key_one",
             "aes_iv": "aes_iv1", "hmac_key": "hmac_key1", "hmac_iv": "hmac_iv1"},
            {"group_name": "group_two", "participant": "b", "signature": "sign2", "aes_key": "aes_key_two",
             "aes_iv": "aes_iv2", "hmac_key": "hmac_key2", "hmac_iv": "hmac_iv2"}])
        os.remove("Accord_groups.db")


if __name__ == '__main__':
    unittest.main()
