import pika
import json
from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import create_instance, check_instance_name_available
from lib.DatabaseUtilities import create_db_connection, get_network_name, add_instance_to_user

# Function: mq_instance
# Date: 2020/01/08
# Purpose: Multiplexing instance requests from message
# Parameters:
#     ch, method, properties, body: RabbitMQ parameters
# Return value:
#     instance: openstack.compute.v2.server.Server object

def mq_instance(ch, method, properties, body):
    payload = json.loads(body.decode("utf-8"))
    try:
        if(payload['method'] == "create"):
            mq_create_instance(payload['name'], payload['instance_name'], payload['image'], payload['flavor'])
    except KeyError:
        print("KeyError")
    

# Function: mq_instance
# Date: 2020/01/08
# Purpose: Multiplexing instance requests from message
# Parameters:
#     ch, method, properties, body: RabbitMQ parameters
# Return value:
#     instance: openstack.compute.v2.server.Server object

def mq_create_instance(username, instance_name, image, flavor):
    conn = create_connection_from_config()
    if(check_instance_name_available(conn, instance_name) is True):
        create_instance(conn, image, flavor, get_network_name(), instance_name)
        add_instance_to_user(username, instance_name)