#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user
from lib.DatabaseUtilities import create_db_connection, get_network_name, add_instance_to_user

conn = create_connection_from_config()
client = create_db_connection()
db = client["t2ee"]

class test_database(unittest.TestCase):
    def test_get_network_name(self):
        self.assertEqual(get_network_name(), "provider1")
    
    def test_add_instance_to_user(self):
        add_instance_to_user("test_user1", "test_instance")
        user_col = db["user"]
        result = user_col.find_one({"name": "test_user1", "instance": {"$elemMatch":{"instance_name":"test_instance"}}})
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()