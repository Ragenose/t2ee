import libvirt
from lib.ConnectionUtilities import openConnection

def state(host, vmName):
    conn = openConnection('qemu+ssh://root@'+host+'/system')
    try:
        vm = conn.lookupByName(vmName)
        return vm.state()
    except:
        return False