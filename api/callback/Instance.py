import pika
import json
from lib.ConnectionUtilities import create_connection_from_config
from lib.InstanceUtilities import create_instance
from lib.DatabaseUtilities import create_db_connection

def mq_instance(ch, method, properties, body):
    payload = json.loads(body.decode("utf-8"))
    try:
        if(payload['method'] == "create"):
            mq_create_instance(payload['name'], payload['instance_name'], payload['image'], payload['flavor'])
    except KeyError:
        print("KeyError")
    


def mq_create_instance(username, instance_name, image, flavor):
    conn = create_connection_from_config()
    create_instance(conn, image, flavor, "provider1", instance_name)