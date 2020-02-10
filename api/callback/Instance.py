import pika
import json
import logging
import time
import openstack
from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import\
    create_instance,\
    check_instance_name_available,\
    delete_instance,\
    check_instance_ownership
from lib.DatabaseUtilities import \
    create_db_connection,\
    get_network_name,\
    add_instance_to_user,\
    remove_instance_from_user,\
    get_keypair,\
    get_root_password

# Function: mq_instance
# Date: 2020/01/08
# Purpose: Multiplexing instance requests from message
# Parameters:
#     ch, method, properties, body: RabbitMQ parameters
# Return value:
#     None

def mq_instance(ch, method, properties, body):
    payload = json.loads(body.decode("utf-8"))
    logging.warning(payload)
    try:
        if(payload['method'] == "create"):
            mq_create_instance(payload['name'], payload['instance_name'], payload['image'], payload['flavor'], payload['root_password'])
        if(payload['method'] == "delete"):
            mq_delete_instance(payload['name'], payload['instance_name'])
    except KeyError:
        print("KeyError")
    

# Function: mq_create_instance
# Date: 2020/01/09
# Purpose: Create instance
# Parameters:
#     username
#     instance_name
#     image
#     flavor
# Return value:
#     None

def mq_create_instance(username, instance_name, image, flavor, root_password):
    conn = create_connection_from_config()
    if(check_instance_name_available(conn, instance_name) is True):
        keypair = get_keypair(username)
        instance = create_instance(conn, image, flavor, get_network_name(), instance_name, root_password=root_password, keypair=keypair)
        add_instance_to_user(username, instance_name, instance.id)
        # Wait for 30 second to let instance boot up
        time.sleep(30)
        # Try to set the root password if it fails
        for i in range(0,10):
            while True:
                try:
                    conn.compute.change_server_password(instance, root_password)
                except openstack.exceptions.HttpException:
                    continue
            break
        
    conn.close()

# Function: mq_delete_instance
# Date: 2020/01/09
# Purpose: Delete instance
# Parameters:
#     username
#     instance_name
# Return value:
#     instance: openstack.compute.v2.server.Server object

def mq_delete_instance(username, instance_name):
    if(check_instance_ownership(username, instance_name) is False):
        return
    conn = create_connection_from_config()
    delete_instance(conn, instance_name)
    remove_instance_from_user(username, instance_name)
    print(username)
    conn.close()