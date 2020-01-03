#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import *
from lib.ImageUtilities import *

conn = create_connection_from_config()

class test_image(unittest.TestCase):
    def test_creating(self):
        if(check_image_name_available(conn, "test_image") == False):
            delete_image(conn, "test_image")
        if(check_instance_name_available(conn, "test_image") == False):
            delete_instance(conn, "test_image")
        create_instance(conn, "Ubuntu16.04", "small", "provider1", "test_image")
        create_image_from_instance(conn, "test_image", "test_image","Unit testing image creation")
        self.assertFalse(check_image_name_available(conn, "test_image"))
    # def test_deleting(self):
    #     conn = create_connection_from_config()
    #     self.assertTrue(delete_instance(conn, "test"))

if __name__ == '__main__':
    unittest.main()