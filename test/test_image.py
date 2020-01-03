#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import create_instance, delete_instance, check_instance_name_available
from lib.ImageUtilities import create_image_from_instance, check_image_name_available, delete_image
from lib.DatabaseUtilities import create_db_connection

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
    def test_deleting(self):
        client = create_db_connection()
        db = client['db']
        image_col = db['image']

        id = conn.compute.find_image("test_image").id
        delete_image(conn, "test_image")
        query = {'id' : id}
        result = image_col.find(query)
        self.assertEqual(0, result.retrieved)
        self.assertTrue(check_image_name_available(conn, "test_image"))

if __name__ == '__main__':
    unittest.main()