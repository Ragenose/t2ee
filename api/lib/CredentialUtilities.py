from lib.DatabaseUtilities import create_db_connection, create_user_document
import sys

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

# Function: check_email_available
# Date: 2020/01/04
# Purpose: Check if the email is taken
# Parameters:
#     conn: OpenStack connection
#     name: The user name that needs to be checked
# Return value:
#     True: If it is not taken
#     False: If it is taken

def check_email_available(conn, email):
    client = create_db_connection()
    db = client["t2ee"]
    user_col = db["user"]
    result = user_col.find({"email": email})
    if(result.retrieved == 0):
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

# Function: update_user_email
# Date: 2020/01/05
# Purpose: Update user email
# Parameters:
#     conn: OpenStack connection
#     name: User name
#     email: User's new email
# Return value:
#     False: If update failed
#     True: If update succeed

def update_user_email(conn, name, email):
    try:
        user = conn.identity.find_user(name)
        conn.identity.update_user(
            user,
            email = email
        )
    except Exception:
        return False
    else:
        try:
            client = create_db_connection()
            db = client["t2ee"]
            user_col = db["user"]
            query = {"name": name}
            new_email = {"$set": {"email": email}}
            print(user_col.find_one(query), file=sys.stderr)
            user_col.update_one(query, new_email)
        except Exception:
            return False
        else:
            return True

# Function: update_user_password
# Date: 2020/01/05
# Purpose: Update user email
# Parameters:
#     conn: OpenStack connection
#     name: User name
#     email: User's new email
# Return value:
#     False: If update failed
#     True: If update succeed

def update_user_password(conn, name, password):
    try:
        user = conn.identity.find_user(name)
        conn.identity.update_user(
            user,
            password = password
        )
    except Exception:
        return False
    else:
        try:
            client = create_db_connection()
            db = client["t2ee"]
            user_col = db["user"]
            query = {"name": name}
            new_password = {"$set" : {"password" : password}}
            user_col.update_one(query, new_password)
        except Exception:
            return False
        else:
            return True

# Function: check_credential
# Date: 2020/01/05
# Purpose: Check user credential
# Parameters:
#     name: User name
#     password: User's password
# Return value:
#     False: Credential not found
#     True: Credential found

def check_credential(name, password):
    client = create_db_connection()
    db = client["t2ee"]
    user_col = db["user"]
    result = user_col.find_one({"name" : name, "password" : password})
    if(result is None):
        return False
    else:
        return True