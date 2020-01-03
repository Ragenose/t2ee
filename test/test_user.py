#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import *

conn = create_connection_from_config()

class test_user(unittest.TestCase):
    def test_creating(self):
        #Delete the user before creating it
        if(conn.identity.find_user("test_user") != None):
            conn.identity.delete_user(conn.identity.find_user("test_user"))

        create_user(conn, "test_user", "test123", "test@123.com")
        user = conn.identity.find_user("test_user")
        print(user.id)
        self.assertEqual(user.name, "test_user")
        self.assertEqual(user.email, "test@123.com")

if __name__ == '__main__':
    unittest.main()