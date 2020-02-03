import openstack


# Function: start_instance
# Date: 2020/01/03
# Purpose: Start instance
# Parameters:
#     conn: OpenStack connection
#     instance_name: The instance that needs to be started
# Return value:
#     True: If it is ACTIVE
#     False: If it is not ACTIVE

def start_instance(conn, instance_name):
    instance = conn.compute.find_server(instance_name)
    
    if(instance.status == "ACTIVE"):
        return True
    else:
        conn.compute.start_server(instance)
    try:
        conn.compute.wait_for_server(instance, status='ACTIVE',wait=10)
    except conn.compute.ResourceTimeout:
        return False
    else:
        return True

# Function: shut_off_instance
# Date: 2020/01/03
# Purpose: Shut off instance
# Parameters:
#     conn: OpenStack connection
#     instance_name: The instance that needs to be shutted off
# Return value:
#     True: If it is SHUTOFF
#     False: If it is not SHUTOFF

def shut_off_instance(conn, instance_name):
    instance = conn.compute.find_server(instance_name)
    
    if(instance.status == "SHUTOFF"):
        return True
    else:
        conn.compute.stop_server(instance)
    try:
        conn.compute.wait_for_server(instance, status='SHUTOFF',wait=10)
    except conn.compute.ResourceTimeout:
        return False
    else:
        return True

# Function: reboot_instance
# Date: 2020/02/03
# Purpose: Reboot instance
# Parameters:
#     conn: OpenStack connection
#     instance_name: The instance that needs to be shutted off
# Return value:
#     True: If it is ACTIVE
#     False: If it is not ACTIVE

def reboot_instance(conn, instance_name):
    instance = conn.compute.find_server(instance_name)

    if(instance.status == "ACTIVE"):
        conn.compute.reboot_server(instance, "SOFT")

    else:
        conn.compute.start_server(instance)   

    try:
        conn.compute.wait_for_server(instance, status='ACTIVE',wait=10)
    except conn.compute.ResourceTimeout:
        return False
    else:
        return True
