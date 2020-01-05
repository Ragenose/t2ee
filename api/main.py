#!/usr/bin/python3
from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import create_instance

conn = create_connection_from_config()
create_instance(conn, "Ubuntu16.04", "small", "provider1", "test_docker")