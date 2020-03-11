import pika
import json
import logging
from lib.ConnectionUtilities import create_connection_from_config
from lib.ImageUtilities import\
    create_image_from_instance,\
    delete_image,\
    check_image_name_available
from lib.DatabaseUtilities import\
    create_db_connection,\
    create_image_document,\
    add_image_to_user,\
    remove_image_from_user,\
    remove_image_from_image_database

# Function: mq_image
# Date: 2020/01/08
# Purpose: Multiplexing image requests from message
# Parameters:
#     ch, method, properties, body: RabbitMQ parameters
# Return value:
#     None

def mq_image(ch, method, properties, body):
    payload = json.loads(body.decode("utf-8"))
    logging.warning(payload)
    try:
        if(payload['method'] == "create"):
            mq_create_image(payload['name'], payload['image_name'], payload['instance_name'], payload['description'])
        if(payload['method'] == "delete"):
            mq_delete_image(payload['name'], payload['image_name'])
    except KeyError:
        print("KeyError")

# Function: mq_create_image
# Date: 2020/01/09
# Purpose: Create image
# Parameters:
#     username
#     image_name
#     instance_name
#     description
# Return value:
#     None

def mq_create_image(username, image_name, instance_name, description):
    conn = create_connection_from_config()
    if(check_image_name_available(conn, image_name) is True):
        image = create_image_from_instance(conn, instance_name, image_name, description)
        create_image_document(username, image_name, instance_name, description)
        add_image_to_user(username, image_name, image.id)
    conn.close()

# Function: mq_delete_image
# Date: 2020/03/10
# Purpose: Delete image
# Parameters:
#     username
#     image_name
# Return value:
#     None

def mq_delete_image(username, image_name):
    conn = create_connection_from_config()
    remove_image_from_user(username, image_name)
    remove_image_from_image_database(image_name)
    delete_image(conn, image_name)
    conn.close()