from websocket import create_connection
import simplejson as json

if __name__ == '__main__':
    ws = create_connection("wss://api.tiingo.com/iex")

    subscribe = {
            'eventName':'subscribe',
            'authorization':'90818697771bcf20991692e3e1541cb8c2fbe7aa',
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
                