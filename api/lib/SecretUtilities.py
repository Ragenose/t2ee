import pymongo
from lib.ConnectionUtilities import create_connection_from_config
from lib.DatabaseUtilities import add_keypair_to_user

def create_keypair(user, pubkey):
    conn = create_connection_from_config()
    conn.compute.create_keypair(
        name = user+"_key",
        public_key = pubkey
    )
    add_keypair_to_user(user, user+"_key")
    conn.close()
    