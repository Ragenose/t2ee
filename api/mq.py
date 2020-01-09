import pika
import json

credentials = pika.PlainCredentials('rabbit','rabbit')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'rabbitmq',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='instance',durable=True)
channel.queue_declare(queue='image',durable=True)

def mq_create_instance(ch, method, properties, body):
    payload = json.loads(body.decode("utf-8"))
    print(payload)

channel.basic_consume(on_message_callback=mq_create_instance,queue='instance', auto_ack=True)

channel.start_consuming()                          