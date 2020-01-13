import yaml
import pymongo
from lib.ConnectionUtilities import create_connection_from_config

# Function: create_db_connection
# Date: 2020/01/02
# Purpose: create database connection
# Parameters:
#     None
# Return value:
#     client: pymongo.MongoClient object

def create_db_connection():
    with open("config/database.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    url = data_loaded["url"]
    client = pymongo.MongoClient(url)
    return client

# Function: create_user_document
# Date: 2020/01/02
# Purpose: create user document in mongodb
# Parameters:
#     user: OpenStack user object
#     password: User's password
# Return value:
#     None

def create_user_document(user, password):
    client = create_db_connection()
    db = client["t2ee"]
    user_col = db["user"]
    user_data = {
        'name' : user.name,
        'password' : password,
        'email' : user.email,
        'id' : user.id,
        'key': '',
        'root_password': '',
        'instance' : [],
        'image' : []
    }
    user_col.insert_one(user_data)
    client.close()

# Function: create_image_document
# Date: 2020/01/02
# Purpose: create image document in mongodb
# Parameters:
#     user: OpenStack user object
#     password: User's password
# Return value:
#     None

def create_image_document(name, image_name, instance_name, description):
    client = create_db_connection()
    db = client["t2ee"]
    image_col = db["image"]
    conn = create_connection_from_config()
    
    instance = conn.compute.find_server(instance_name)
    try:
        image_id = conn.compute.get_server(instance.id).image.id
    except:
        return
    else:
        base_image_name = conn.image.find_image(image_id).name
        print(base_image_name)
        image_data = {
            "username" : name,
            "image_id": image_id,
            "image_name": image_name,
            "base_image_name": base_image_name,
            "description": description,
            "count": 0
        }
        image_col.insert_one(image_data)
    client.close()

# Function: get_network_name
# Date: 2020/01/08
# Purpose: Get network name from database
# Parameters:
#     None
# Return value:
#     Network name

def get_network_name():
    client = create_db_connection()
    db = client["t2ee"]
    openstack_col = db['openstack']
    result = openstack_col.find_one()
    client.close()
    return result["network"][0]

# Function: get_keypair
# Date: 2020/01/12
# Purpose: Get key name of user
# Parameters:
#     user: User's name
# Return value:
#     None: If user doesn't have a key registered 
#           or user doesn't exist
#     result['key']: User's key name
def get_keypair(user):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    result = user_col.find_one(
        {'name' : user}
    )
    if(result is None):
        return None
    else:
        if(result['key'] == ""):
            return None
        else:
            return result['key']

# Function: add_instance_to_user
# Date: 2020/01/08
# Purpose: Add instance under user's name
# Parameters:
#     user: User's name
#     instance_name: Instance name
#     instance_id: Instance id
# Return value:
#     None

def add_instance_to_user(user, instance_name, instance_id):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$push": {"instance": {"instance_name": instance_name, "instance_id": instance_id}}}
    )
    client.close()

# Function: remove_instance_from_user
# Date: 2020/01/09
# Purpose: Remove instance under user's name
# Parameters:
#     user: User's name
#     instance_name: Instance name
# Return value:
#     None

def remove_instance_from_user(user, instance_name):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$pull": {"instance": {"instance_name": instance_name}}}
    )
    client.close()

# Function: add_image_to_user
# Date: 2020/01/10
# Purpose: Add image under user's name
# Parameters:
#     user: User's name
#     image_name: Image name
#     image_id: Image id
# Return value:
#     None

def add_image_to_user(user, image_name, image_id):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$push": {"image": {"image_name": image_name, "image_id": image_id}}}
    )
    client.close()

# Function: remove_image_from_user
# Date: 2020/01/09
# Purpose: Remove image under user's name
# Parameters:
#     user: User's name
#     image_name: Image name
# Return value:
#     None

def remove_image_from_user(user, image_name):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$pull": {"image": {"image_name": image_name}}}
    )
    client.close()

# Function: add_keypair_to_user
# Date: 2020/01/11
# Purpose: Add keypair under user's name
# Parameters:
#     user: User's name
#     keypair: Keypair name
# Return value:
#     None

def add_keypair_to_user(user, keypair):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$set" : {"key" : keypair}}
    )
    client.close()

# Function: remove_keypair_from_user
# Date: 2020/01/12
# Purpose: Remove keypair under user's name
# Parameters:
#     user: User's name
# Return value:
#     None

def remove_keypair_from_user(user):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$set" : {"key" : ""}}
    )
    client.close()

# Function: add_root_password_to_user
# Date: 2020/01/12
# Purpose: Add root password under user's name
# Parameters:
#     user: User's name
#     root_password: Root password
# Return value:
#     None

def add_root_password_to_user(user, root_password):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$set" : {"root_password" : root_password}}
    )
    client.close()

# Function: remove_root_password_from_user
# Date: 2020/01/12
# Purpose: Remove root password under user's name
# Parameters:
#     user: User's name
# Return value:
#     None

def remove_root_password_from_user(user):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update(
        {"name": user},
        {"$set" : {"root_password" : ""}}
    )
    client.close()