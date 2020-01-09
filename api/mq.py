import pika
import json
from callback.Instance import mq_instance

credentials = pika.PlainCredentials('rabbit','rabbit')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'rabbitmq',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='instance',durable=True)
channel.queue_declare(queue='image',durable=True)


channel.basic_consume(on_message_callback=mq_instance,queue='instance', auto_ack=True)

channel.start_consuming()                          