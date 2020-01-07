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