from lib.DatabaseUtilities import create_user_document


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