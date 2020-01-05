#!/usr/bin/python3
from flask import Flask, request, Response
from CreateDatabase import update_database_config
from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user

app = Flask(__name__)

@app.route('/api/user/create', methods=['POST'])
def api_create_user():
    content = request.get_json()

    #Try to get data from json body
    try:
        username = content["username"]
        password = content["password"]
        email = content["email"]
    
    #If data is not correct in the body, return 400
    except TypeError:
        return Response(
            "Bad Request",
            400
        )
    
    #Create user
    else:
        #Open conenction
        conn = create_connection_from_config()
        #If creation failed, return 500
        if(create_user(conn, username, password, email) is False):
            conn.close()
            return Response(
                "Creating failed",
                500
            )
        #Creation succeed, return 200
        else:
            conn.close()
            return Response(
                "OK",
                200
            )

if __name__ == '__main__':
    #Every time the app runs, it updates the OpenStack config
    update_database_config()

    #Start the server
    app.run(debug = True, host="0.0.0.0")