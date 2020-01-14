import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user, update_user_email, update_user_password

conn = create_connection_from_config()

class test_user(unittest.TestCase):
    def test_update_user_email(self):
        #Delete the user before creating it
        if(conn.identity.find_user("test_user") is not None):
            conn.identity.delete_user(conn.identity.find_user("test_user"))
        create_user(conn, "test_user", "test123", "old@123.com")
        
        update_user_email(conn, "test_user", "new@123.com")
        user = conn.identity.find_user("test_user")
        self.assertEqual(user.name, "test_user")
        self.assertEqual(user.email, "new@123.com")

if __name__ == '__main__':
    unittest.main()