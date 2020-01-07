import pika

credentials = pika.PlainCredentials('rabbit','rabbit')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'rabbitmq',5672,'/',credentials))
channel = connection.channel()
