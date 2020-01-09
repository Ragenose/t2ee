import yaml
import pymongo


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
        'instance' : [],
        'image' : []
    }
    user_col.insert_one(user_data)

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

# Function: add_instance_to_user
# Date: 2020/01/08
# Purpose: Add instance under user's name
# Parameters:
#     None
# Return value:
#     Network name
def add_instance_to_user(user, instance_name):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    user_col.update_one(
        {"name": user},
        {"$push": {"instance": {"instance_name": instance_name}}}
    )