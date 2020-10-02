import os
import pika

def main():
    status = os.getenv("STATUS")
    filehash = os.getenv("FILEHASH")
    filename = os.getenv("FILENAME")
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-service'))
    channel = connection.channel()
    channel.basic_publish(
        exchange='adaptation-exchange', 
        routing_key='adaptation-outcome', 
        body='{"status": "%s", "filehash": "%s", "filename": "%s"}' %(status, filehash, filename))