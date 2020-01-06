#!/usr/bin/python3
from flask import Flask, request, Response
from CreateDatabase import update_database_config
from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user, update_user_email, update_user_password, check_credential
import sys

app = Flask(__name__)

def load_user_from_request(request):
    if request.authorization is None:
        return None
    username = request.authorization.get('username')
    password = request.authorization.get('password')
    print(username, password)
    return check_credential(username, password)

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

@app.route('/api/user/update/<string:field>', methods=['POST'])
def api_update_user(field):
    #If the variable is not email or password, return 404
    if(field != ("email" or "password")):
        return Response(
                "URL not found",
                404
            )
    #Check if the username and password in authorization is correct
    if(load_user_from_request(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    else:
        content = request.get_json()
        #Update email
        if(field == "email"):
            try:
                username = request.authorization.get('username')
                email = content["email"]
             #If data is not correct in the body, return 400
            except TypeError:
                return Response(
                    "Bad Request, insufficient data",
                    400
                )
            else:
                conn = create_connection_from_config()
                if(update_user_email(conn, username, email) is True):
                    return Response(
                        "OK",
                        200
                    )
                else:
                    return Response(
                        "Update email failed",
                        400
                    )
        #Update password
        if(field == "password"):
            try:
                username = request.authorization.get('username')
                password = content["password"]
             #If data is not correct in the body, return 400
            except TypeError:
                return Response(
                    "Bad Request, insufficient data",
                    400
                )
            else:
                conn = create_connection_from_config()
                if(update_user_password(conn, username, password) is True):
                    return Response(
                        "OK",
                        200
                    )
                else:
                    return Response(
                        "Update password failed",
                        400
                    )

if __name__ == '__main__':
    #Every time the app runs, it updates the OpenStack config
    update_database_config()

    #Start the server
    app.run(debug = True, host="0.0.0.0")