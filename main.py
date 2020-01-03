#!/usr/bin/python3
from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import *
from lib.ImageUtilities import create_image_from_instance

conn = create_connection_from_config()

#check_instance_name_available(conn, "test")
#create_instance(conn, "CentOS7", "small", "provider1", "test")
#delete_instance(conn, "test")

create_image_from_instance(conn, "test", "test1", "Just for testing")

