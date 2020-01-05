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
    return conn.compute.find_server(instance_name).status