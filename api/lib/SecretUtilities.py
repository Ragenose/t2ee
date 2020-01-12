import pymongo
from lib.ConnectionUtilities import create_connection_from_config
from lib.DatabaseUtilities import create_db_connection, add_keypair_to_user

# Function: create_keypair
# Date: 2020/01/11
# Purpose: Create keypair in OpenStack
# Parameters:
#     user: User's name
#     pubkey: The public key
# Return value:
#     True: If succeed
#     False: If failed

def create_keypair(user, pubkey):
    conn = create_connection_from_config()
    try:
        conn.compute.create_keypair(
            name = user+"_key",
            public_key = pubkey
        )
    except:
        conn.close()
        return False
    else:
        add_keypair_to_user(user, user+"_key")
        conn.close()
        return True

# Function: update_keypair
# Date: 2020/01/11
# Purpose: Update keypair in OpenStack
# Parameters:
#     user: User's name
#     pubkey: The public key
# Return value:
#     True: If succeed
#     False: If failed

def update_keypair(user, pubkey):
    client = create_db_connection()
    user_col = client["t2ee"]["user"]
    result = user_col.find_one({
        "name": user
    })
    if(result is None):
        return False
    if(result["key"] == ""):
        return create_keypair(user, pubkey)
    else:
        conn = create_connection_from_config()
        key = conn.compute.find_keypair(result["key"])
        if(key is not None):
            conn.compute.delete_keypair(key)
            return create_keypair(user, pubkey)
        return False