#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='main_queue', durable=True, arguments={
  'x-message-ttl' : 5500, # Delay until the message is transferred in milliseconds.
  'x-dead-letter-exchange' : '', # Basic Exchange used to transfer the message from A to B.
  'x-dead-letter-routing-key' : 'wating_queue' # Name of the queue we want the message transferred to.
}) # Main Queue
channel.queue_declare(queue='dead_queue', durable=True) # Main Queue
channel.queue_declare(queue='wating_queue', durable=True,  arguments={
  'x-message-ttl' : 5500, # Delay until the message is transferred in milliseconds.
  'x-dead-letter-exchange' : '', # Basic Exchange used to transfer the message from A to B.
  'x-dead-letter-routing-key' : 'dead_queue' # Name of the queue we want the message transferred to.
})
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='main_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent %r" % message)
connection.close()
