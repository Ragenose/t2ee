#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import *

conn = create_connection_from_config()


if __name__ == '__main__':
    shutdown("t2ee-c1","centos")
    while state("t2ee-c1","centos") != "shutdown" :
        pass
    unittest.main()