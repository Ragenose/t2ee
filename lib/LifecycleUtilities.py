import libvirt
from lib.ConnectionUtilities import openConnection

STATE_MAP = {0: 'running',
             1: 'running',
             2: 'running',
             3: 'paused',
             4: 'shutdown',
             5: 'shutdown',
             6: 'crashed'}


def start(host, vmName):
    conn = openConnection('qemu+ssh://root@'+host+'/system')
    try:
        vm = conn.lookupByName(vmName)
        #Start VM
        vm.create()
        return True
    except:
        return False

def shutdown(host, vmName):
    conn = openConnection('qemu+ssh://root@'+host+'/system')
    try:
        vm = conn.lookupByName(vmName)
        #shutdown VM
        vm.shutdown()
        return True
    except:
        return False

def destory(host, vmName):
    conn = openConnection('qemu+ssh://root@'+host+'/system')
    try:
        vm = conn.lookupByName(vmName)
        #Force off VM
        vm.destroy()
        return True
    except:
        return False

def reboot(host, vmName):
    conn = openConnection('qemu+ssh://root@'+host+'/system')
    try:
        vm = conn.lookupByName(vmName)
        #reboot VM
        vm.reboot()
        return True
    except:
        return False
