#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user
from lib.DatabaseUtilities import create_db_connection, get_network_name
conn = create_connection_from_config()

class test_database(unittest.TestCase):
    def test_get_network_name(self):
        
        self.assertEqual(get_network_name(), "provider1")

if __name__ == '__main__':
    unittest.main()