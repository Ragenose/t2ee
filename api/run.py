#!/usr/bin/python3
from flask import Flask, request, Response
from CreateDatabase import update_database_config
from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user, update_user_email, update_user_password, check_credential
import sys
import pika
import json

app = Flask(__name__)
credentials = pika.PlainCredentials('rabbit', 'rabbit')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'rabbitmq', 5672, '/', credentials))
channel = connection.channel()


def load_user_from_request(request):
    if request.authorization is None:
        return None
    username = request.authorization.get('username')
    password = request.authorization.get('password')
    print(username, password)
    return check_credential(username, password)


def check_user_credential(request):
    load_user_from_request(request)


@app.route('/api/user/create', methods=['POST'])
def api_create_user():
    content = request.get_json()

    # Try to get data from json body
    try:
        username = content["username"]
        password = content["password"]
        email = content["email"]

    # If data is not correct in the body, return 400
    except TypeError:
        return Response(
            "Bad Request",
            400
        )

    # Create user
    else:
        # Open conenction
        conn = create_connection_from_config()
        # If creation failed, return 500
        if(create_user(conn, username, password, email) is False):
            conn.close()
            return Response(
                "Creating failed",
                500
            )
        # Creation succeed, return 200
        else:
            conn.close()
            return Response(
                "OK",
                200
            )


@app.route('/api/user/update/<string:field>', methods=['POST'])
def api_update_user(field):
    # If the variable is not email or password, return 404
    if(field != ("email" or "password")):
        return Response(
            "URL not found",
            404
        )
    # Check if the username and password in authorization is correct
    check_user_credential(request)
    content = request.get_json()
    # Update email
    if(field == "email"):
        try:
            username = request.authorization.get('username')
            email = content["email"]
        # If data is not correct in the body, return 400
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
        # Update password
    if(field == "password"):
        try:
            username = request.authorization.get('username')
            password = content["password"]
         # If data is not correct in the body, return 400
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


@app.route('/api/instance/create', methods=['POST'])
def api_create_instance():
    check_user_credential(request)
    content = request.get_json()
    try:
        username = request.authorization.get('username')
        flavor = content['flavor']
        instance_name = content['instance_name']
        image = content['image']
    except KeyError:
        return Response(
            "Bad Request, insufficient data",
            400
        )
    else:
        payload = {
            'method': 'create',
            'name': username,
            'flavor': flavor,
            'instance_name': instance_name,
            'image': image
        }
        channel.basic_publish(exchange='',
                              routing_key='instance',
                              body=json.dumps(payload),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        return Response(
            "OK",
            200
        )


@app.route('/api/instance/delete/<string:instance_name>', methods=['POST'])
def api_delete_instance(instance_name):
    check_user_credential(request)
    username = request.authorization.get('username')
    payload = {
        'method': 'delete',
        'name': username,
        'instance_name': instance_name
    }
    channel.basic_publish(exchange='',
                          routing_key='instance',
                          body=json.dumps(payload),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    return Response(
        "OK",
        200
    )


@app.route('/api/image/create', methods=['POST'])
def api_create_image():
    check_user_credential(request)
    content = request.get_json()
    try:
        username = request.authorization.get('username')
        instance_name = content['instance_name']
        image_name = content['image_name']
        description = content['description']
    except KeyError:
        return Response(
            "Bad Request, insufficient data",
            400
        )
    else:
        payload = {
            'method': 'create',
            'name': username,
            'instance_name': instance_name,
            'image_name': image_name,
            'description': description
        }
        channel.basic_publish(exchange='',
                              routing_key='image',
                              body=json.dumps(payload),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        return Response(
            "OK",
            200
        )


@app.route('/api/image/delete/<string:image_name>', methods=['POST'])
def api_delete_image(image_name):
    check_user_credential(request)
    username = request.authorization.get('username')
    payload = {
        'method': 'delete',
        'name': username,
        'image_name': image_name
    }
    channel.basic_publish(exchange='',
                          routing_key='image',
                          body=json.dumps(payload),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    return Response(
        "OK",
        200
    )

if __name__ == '__main__':
    # Every time the app runs, it updates the OpenStack config
    update_database_config()

    # Declare queues for the project
    channel.queue_declare(queue='instance', durable=True)
    channel.queue_declare(queue='image', durable=True)

    # Start the server
    app.run(debug=True, host="0.0.0.0")
