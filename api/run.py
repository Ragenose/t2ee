#!/usr/bin/python3
from flask import Flask, request, Response, jsonify
from CreateDatabase import update_database_config
from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user, update_user_email, update_user_password, check_credential
from lib.SecretUtilities import update_keypair
from lib.DatabaseUtilities import add_root_password_to_user, get_images, get_user_info
from lib.StatusUtilites import get_instance_status, get_instance_address
from lib.LifecycleUtilities import start_instance, shut_off_instance, reboot_instance
from lib.InstanceUtilities import check_instance_ownership
import logging
import sys
import pika
import json

app = Flask(__name__)
credentials = pika.PlainCredentials('rabbit', 'rabbit')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'rabbitmq', 5672, '/', credentials, heartbeat=0))


def check_user_credential(request):
    try:
        username = request.authorization.get('username')
        password = request.authorization.get('password')
    except:
        return False
    else:
        return check_credential(username, password)


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
                403
            )
        # Creation succeed, return 200
        else:
            conn.close()
            return Response(
                response=json.dumps({'username': username}),
                status=200
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


@app.route('/api/user/root_password/update', methods=['POST'])
def api_update_root_password():
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    username = request.authorization.get('username')
    content = request.get_json()
    try:
        root_password = content["root_password"]
    except KeyError:
        return Response(
            "Bad Request, insufficient data",
            400
        )
    else:
        add_root_password_to_user(username, root_password)
        return Response(
            "OK",
            200
        )


@app.route('/api/user/keypair/update', methods=['POST'])
def api_update_keypair():
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    username = request.authorization.get('username')
    content = request.get_json()
    try:
        pubkey = content["pubkey"]
    except KeyError:
        return Response(
            "Bad Request, insufficient data",
            400
        )
    else:
        update_keypair(username, pubkey)
        return Response(
            "OK",
            200
        )


@app.route('/api/user/info', methods=['GET'])
def api_get_user_info():
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    username = request.authorization.get('username')
    conn = create_connection_from_config()
    result = get_user_info(username)
    if(result is not None):
        for instance in result['instance']:
            instance['status'] = get_instance_status(
                conn, instance["instance_name"])
            address = get_instance_address(
                conn, instance["instance_name"])
            instance['address'] = list(address[list(address)[0]])[0]
    conn.close()
    return Response(
        response=json.dumps(result),
        status=200
    )


@app.route('/api/user/login', methods=['POST'])
def api_user_login():
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    return Response(
        response=json.dumps(
            {'username': request.authorization.get('username')}),
        status=200
    )


@app.route('/api/instance/create', methods=['POST'])
def api_create_instance():
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    content = request.get_json()
    try:
        username = request.authorization.get('username')
        flavor = content['flavor']
        instance_name = content['instance_name']
        image = content['image']
        root_password = content['root_password']
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
            'image': image,
            'root_password': root_password
        }
        channel = connection.channel()
        channel.basic_publish(exchange='',
                              routing_key='instance',
                              body=json.dumps(payload),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        channel.close()
        return Response(
            response=json.dumps({"status": "OK"}),
            status=200
        )


@app.route('/api/instance/delete/<string:instance_name>', methods=['DELETE'])
def api_delete_instance(instance_name):
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    username = request.authorization.get('username')
    payload = {
        'method': 'delete',
        'name': username,
        'instance_name': instance_name
    }
    channel = connection.channel()
    channel.basic_publish(exchange='',
                          routing_key='instance',
                          body=json.dumps(payload),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    channel.close()
    return Response(
        response=json.dumps({"status": "OK"}),
        status=200
    )

@app.route('/api/instance/lifecycle/<string:type>/<string:instance_name>', methods=['POST'])
def api_instance_lifecycle(type, instance_name):
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    username = request.authorization.get('username')
    if(check_instance_ownership(username, instance_name) is False):
         return Response(
            "Invalid Credential",
            401
        )

    if(type == "start"):
        conn = create_connection_from_config()
        if(start_instance(conn, instance_name) is True):
            conn.close()
            return Response(
            response=json.dumps({"status": "OK"}),
            status=200
        )
    elif(type == "shutdown"):
        conn = create_connection_from_config()
        if(shut_off_instance(conn, instance_name) is True):
            conn.close()
            return Response(
            response=json.dumps({"status": "OK"}),
            status=200
        )
    elif(type == "reboot"):
        conn = create_connection_from_config()
        if(reboot_instance(conn, instance_name) is True):
            conn.close()
            return Response(
            response=json.dumps({"status": "OK"}),
            status=200
        )
    else:
        return Response(
            "Invalid operation",
            500
        )
    return Response(
        "Failed",
        500
    )

@app.route('/api/image/create', methods=['POST'])
def api_create_image():
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
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
        channel = connection.channel()
        channel.basic_publish(exchange='',
                              routing_key='image',
                              body=json.dumps(payload),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        channel.close()
        return Response(
            "OK",
            200
        )


@app.route('/api/image/delete/<string:image_name>', methods=['DELETE'])
def api_delete_image(image_name):
    if(check_user_credential(request) is False):
        return Response(
            "Invalid Credential",
            401
        )
    username = request.authorization.get('username')
    payload = {
        'method': 'delete',
        'name': username,
        'image_name': image_name
    }
    channel = connection.channel()
    channel.basic_publish(exchange='',
                          routing_key='image',
                          body=json.dumps(payload),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    channel.close()
    return Response(
        "OK",
        200
    )


@app.route('/api/image/list', methods=['GET'])
def api_get_images():
    data = get_images()
    return Response(
        response=json.dumps(data),
        status=200
    )


if __name__ == '__main__':
    # Every time the app runs, it updates the OpenStack config
    update_database_config()

    # Declare queues for the project
    channel = connection.channel()
    channel.queue_declare(queue='instance', durable=True)
    channel.queue_declare(queue='image', durable=True)
    channel.close()
    # Start the server
    app.run(debug=True, host="0.0.0.0")
