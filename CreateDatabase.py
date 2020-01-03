#!/usr/bin/python3
import pymongo
import yaml

with open("config/database.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream) 

url = data_loaded["url"]

client = pymongo.MongoClient(url)

db = client["t2ee"]

openstack_col = db["openstack"]

with open("config/compute.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream) 

openstack_col.insert_one(data_loaded)