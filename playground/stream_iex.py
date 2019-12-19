from websocket import create_connection
import json
import pika

from pika.channel import Channel

if __name__ == '__main__':
    ws = create_connection("wss://api.tiingo.com/iex")

    RABBITMQ_EXCHANGE_NAME = 'iex_rabbitmq_exchange'
    RABBITMQ_QUEUE_NAME = 'iex_rabbitmq_queue'

    credentials = pika.PlainCredentials('martin', 'martin')

    connection = pika.BlockingConnection(pika.ConnectionParameters('desktop.martinwongsk.com', 5672, '/', credentials))
    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, credentials=credentials))
    channel: Channel = connection.channel()
    channel.exchange_declare(RABBITMQ_EXCHANGE_NAME)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE_NAME, queue=RABBITMQ_QUEUE_NAME   )
    channel.queue_declare(RABBITMQ_QUEUE_NAME, durable=True)


    subscribe = {
        'eventName': 'subscribe',
        'authorization': '90818697771bcf20991692e3e1541cb8c2fbe7aa',
        'eventData': {
            'thresholdLevel': 0
        }
    }

    ws.send(json.dumps(subscribe))
    print('Receiving data')
    while True:
        with open('iex_191219.txt', 'a+') as f:
            recv_wss = ws.recv()
            if 'data' in recv_wss:
                f.write(f'{recv_wss}\n')
                channel.basic_publish(
                    exchange=RABBITMQ_EXCHANGE_NAME,
                    routing_key=RABBITMQ_QUEUE_NAME,
                    body=recv_wss,
                    properties=pika.BasicProperties(
                        delivery_mode=2
                    )
                )
