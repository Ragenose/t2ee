#!/usr/bin/python3
import libvirt
import unittest
import time
import sys, os

#sys.path.append('~/t2ee')

from lib.LifecycleUtilities import *
from lib.StatusUtilites import *


class TestLifecycle(unittest.TestCase):
    def test_start(self):
        start("t2ee-c1", "centos")
        self.assertEqual("running", state("t2ee-c1", "centos"))


if __name__ == '__main__':
    shutdown("t2ee-c1","centos")
    while state("t2ee-c1","centos") != "shutdown" :
        pass
    unittest.main()