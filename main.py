#!/usr/bin/python3
import libvirt
from lib.LifecycleUtilities import *

print(STATE_MAP.get(1,"unknown"))


print(boot("centos"))
#shutdown("test-vm")
#reboot("centos")