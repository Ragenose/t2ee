from lib.DatabaseUtilities import create_db_connection

# Function: check_instance_name_available
# Date: 2020/01/02
# Purpose: Check if the instance name is taken
# Parameters:
#     conn: OpenStack connection
#     instance_name: The instance name that needs to be checked
# Return value:
#     True: If it is not taken
#     False: If it is taken

def check_instance_name_available(conn, instance_name):
    instance = conn.compute.find_server(instance_name)
    if(instance is None):
        return True
    else:
        return False


# Function: create_instance
# Date: 2019/12/31
# Purpose: Create instance
# Parameters:
#     conn: OpenStack connection
#     image_name: Image that the instance is created from
#     flavor_name: Flavor that the instance is created from
#     network_name: Network that the instance is running on
#     instance_name: The name of instance
# Return value:
#     instance: openstack.compute.v2.server.Server object

def create_instance(conn, image_name, flavor_name, network_name, instance_name, root_password="", keypair=None):
    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor(flavor_name)
    network = conn.network.find_network(network_name)

    if(keypair is not None):
        instance = conn.compute.create_server(
            name = instance_name, image_id = image.id, flavor_id = flavor.id,
            networks = [{"uuid": network.id}], key_name = keypair)
        conn.compute.wait_for_server(instance, status='ACTIVE', wait=60)
        return instance
    else:
        instance = conn.compute.create_server(
            name = instance_name, image_id = image.id, flavor_id = flavor.id,
            networks = [{"uuid": network.id}])
        return instance
    #instance = conn.compute.wait_for_server(instance)
    return None


# Function: delete_instance
# Date: 2020/01/02
# Purpose: Delete instance
# Parameters:
#     conn: OpenStack connection
#     instance_name: The name of instance
# Return value:
#     None

def delete_instance(conn, instance_name):
    instance = conn.compute.find_server(instance_name)
    conn.compute.delete_server(instance) 

# Function: check_instance_ownership
# Date: 2020/01/09
# Purpose: check instance ownership
# Parameters:
#     name: User's name
#     instance_name: The name of instance
# Return value:
#     True: If the user owns the instance
#     False: If the user doesn't own the instance

def check_instance_ownership(name, instance_name):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    result = user_col.find_one({"name": name, "instance": {"$elemMatch":{"instance_name":instance_name}}})
    client.close()
    if(result is not None):
        return True
    else:
        return False
