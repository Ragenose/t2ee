import pymongo
from lib.ConnectionUtilities import create_connection_from_config

def create_keypair(user, pubkey):
    conn = create_connection_from_config()
    conn.compute.create_keypair(
        name = user,
        public_key = pubkey
    )
    