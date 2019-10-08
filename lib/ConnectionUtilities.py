import libvirt

def openConnection(host):
    conn = libvirt.open(host)
    return conn
