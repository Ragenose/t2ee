#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import create_instance, check_instance_name_available, delete_instance

conn = create_connection_from_config()

class test_instance(unittest.TestCase):
    def test_creating(self):
        conn = create_connection_from_config()
        create_instance(conn, "	Ubuntu16.04", "small", "provider1", "test")
        self.assertFalse(check_instance_name_available(conn, "test"))
    def test_deleting(self):
        conn = create_connection_from_config()
        self.assertTrue(delete_instance(conn, "test"))
    def test_change_password(self):
        conn = create_connection_from_config()
        conn.compute.change_server_password(conn.compute.find_server("test_creation2"), "whatever")
if __name__ == '__main__':
    unittest.main()