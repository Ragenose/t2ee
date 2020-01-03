import openstack

'''
Function: create_user
Date: 2020/01/02
Purpose: Create user
Parameters: 
    conn: OpenStack connection
    name: User name
    password: User password
    email: User email
Return value: 
    instance: openstack.compute.v2.server.Server object
'''
def create_user(conn, name, password, email):
    return conn.identity.create_user(
        name = name,
        password = password,
        email = email,
    )