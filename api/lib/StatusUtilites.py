import openstack


# Function: get_instance_status
# Date: 2020/01/03
# Purpose: Get instance status
# Parameters:
#     conn: OpenStack connection
#     instance_name: The instance that needs to be started
# Return value:
#     status

def get_instance_status(conn: openstack.connection.Connection, instance_name):
    #return conn.compute.find_server(instance_name).power_state
    instance = conn.compute.find_server(instance_name)
    state = conn.compute.get_server(instance).power_state
    return return_power_state(state)

# Function: get_instance_address
# Date: 2020/01/13
# Purpose: Get instance addresses
# Parameters:
#     conn: OpenStack connection
#     instance_name: The instance that needs to be started
# Return value:
#     IP addresses

def get_instance_address(conn: openstack.connection.Connection, instance_name):
    instance = conn.compute.find_server(instance_name)
    return conn.compute.get_server(instance).addresses

# Function: return_power_state
# Date: 2020/01/13
# Purpose: convert status code into actual state
# Parameters:
#     status code from OpenStack
# Return value:
#     power state

def return_power_state(code):
    state = [
        'NO STATE',
        'RUNNING',
        'BLOCKED',
        'PAUSED',
        'SHUTDOWN',
        'SHUTOFF',
        'CRASHED',
        'SUSPENDED',
        'FAILED',
        'BUILDING']
    return state[code]