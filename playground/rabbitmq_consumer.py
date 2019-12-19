import json
import pika

from pika.channel import Channel

if __name__ == '__main__':

    RABBITMQ_EXCHANGE_NAME = 'iex_rabbitmq_exchange'
    RABBITMQ_QUEUE_NAME = 'iex_rabbitmq_queue'

    credentials = pika.PlainCredentials('martin', 'martin')

    connection = pika.BlockingConnection(pika.ConnectionParameters('vpn.desktop.martinwongsk.com', 5672, '/', credentials))
    channel: Channel = connection.channel()
    # channel.exchange_declare(RABBITMQ_EXCHANGE_NAME)
    # channel.queue_bind(exchange=RABBITMQ_EXCHANGE_NAME, queue=RABBITMQ_QUEUE_NAME   )
    channel.queue_declare(RABBITMQ_QUEUE_NAME, durable=True)
    print(" [*] Going to get message from queue")

    file = open('iex_191219_consumer.txt', 'a+')

    def msg_callback(ch, method, properties, body):
        file.write(f'{body.decode()}\n')


    channel.basic_consume(queue=RABBITMQ_QUEUE_NAME, auto_ack=True, on_message_callback=msg_callback)
    channel.start_consuming()
