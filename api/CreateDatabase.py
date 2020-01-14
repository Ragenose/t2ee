#!/usr/bin/python3
import pymongo
import yaml

# Function: update_database_config
# Date: 2020/01/04
# Purpose: update openstack config in MongoDB
# Parameters:
#     None
# Return value:
#     None

def update_database_config():
    with open("config/database.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    url = data_loaded["url"]

    client = pymongo.MongoClient(url)

    db = client["t2ee"]

    openstack_col = db["openstack"]

    with open("config/compute.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    with open("config/openstack.yaml", 'r') as stream:
        openstack_data = yaml.safe_load(stream)

    data = {**data_loaded, **openstack_data}
    #Delete all documents in the collection
    openstack_col.delete_many({})
    #Insert the new document in the collection
    openstack_col.insert_one(data)