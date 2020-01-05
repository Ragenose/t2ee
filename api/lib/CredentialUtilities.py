from lib.DatabaseUtilities import create_user_document

# Function: check_user_available
# Date: 2020/01/04
# Purpose: Check if the user name is taken
# Parameters:
#     conn: OpenStack connection
#     name: The user name that needs to be checked
# Return value:
#     True: If it is not taken
#     False: If it is taken
def check_user_available(conn, name):
    user = conn.identity.find_user(name)
    if(user is None):
        return True
    else:
        return False

# Function: create_user
# Date: 2020/01/02
# Purpose: Create user
# Parameters:
#     conn: OpenStack connection
#     name: User name
#     password: User password
#     email: User email
# Return value:
#     False: If creation failed
#     instance: openstack.compute.v2.server.Server object

def create_user(conn, name, password, email):
    try:
        user = conn.identity.create_user(
            name = name,
            password = password,
            email = email,
        )
    except Exception:
        return False
    else:
        create_user_document(user, password)
        return user
