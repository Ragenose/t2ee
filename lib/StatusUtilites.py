import libvirt
from lib.ConnectionUtilities import openConnection

STATE_MAP = {0: 'no state',
             1: 'running',
             2: 'blocked',
             3: 'paused',
             4: 'being shut down',
             5: 'shutdown',
             6: 'crashed'}

def state(host, vmName):
    conn = openConnection('qemu+ssh://root@'+host+'/system')
    try:
        vm = conn.lookupByName(vmName)
        return STATE_MAP[vm.state()[0]]
    except:
        return False