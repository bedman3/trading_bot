from websocket import create_connection
import json
import pika

from pika.channel import Channel

if __name__ == '__main__':
    ws = create_connection("wss://api.tiingo.com/iex")

    # connection = pika.BlockingConnection(pika.ConnectionParameters('amqp://martin:martin@vpn.desktop.martinwongsk.com:5672/'))

    credentials = pika.PlainCredentials('martin', 'martin')

    connection = pika.BlockingConnection(pika.ConnectionParameters('vpn.desktop.martinwongsk.com', 5672, '/', credentials))
    channel: Channel = connection.channel()
    channel.queue_declare('')

    subscribe = {
        'eventName': 'subscribe',
        'authorization': '90818697771bcf20991692e3e1541cb8c2fbe7aa',
        'eventData': {
            'thresholdLevel': 0
        }
    }

    ws.send(json.dumps(subscribe))
    while True:
        with open('iex_191219.txt', 'a+') as f:
            recv_wss = ws.recv()
            if 'data' in recv_wss:
                f.write(f'{recv_wss}\n')
                print(recv_wss)
