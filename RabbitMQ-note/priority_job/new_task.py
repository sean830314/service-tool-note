

#!/usr/bin/env python
import pika
import sys
from random import randint
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
priority = randint(0, 10)
channel.queue_declare(queue='task_queue', durable=True, arguments={'x-max-priority': 10})
message = ' '.join(sys.argv[1:]) or f'Hello World! {priority}'
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        priority=priority,
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent %r" % message)
connection.close()


