import libvirt
from lib.ConnectionUtilities import openConnection

STATE_MAP = {0: 'running',
             1: 'running',
             2: 'running',
             3: 'paused',
             4: 'shutdown',
             5: 'shutdown',
             6: 'crashed'}


def boot(hostname):
    conn = openConnection('qemu+ssh://root@t2ee-c1/system')
    try:
        vm = conn.lookupByName(hostname)
        vm.create()
        return True
    except:
        return False

def shutdown(hostname):
    conn = openConnection('qemu+ssh://root@t2ee-c1/system')
    try:
        vm = conn.lookupByName(hostname)
        vm.shutdown()
        return True
    except:
        return False

def reboot(hostname):
    conn = openConnection('qemu+ssh://root@t2ee-c1/system')
    try:
        vm = conn.lookupByName(hostname)
        vm.reboot()
        return True
    except:
        return False