import unittest
import sys
from . import Database

class TestDatabase(unittest.TestCase):

    def test_username_initialization(self):
        self.assertTrue(Database.initialize_username_database())
    
    
if __name__ == '__main__':
    unittest.main()