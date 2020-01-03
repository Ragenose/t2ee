#!/usr/bin/python3
import pymongo
import yaml

with open("config/database.yaml", 'r') as stream:
            data_loaded = yaml.safe_load(stream) 

url = data_loaded["url"]
