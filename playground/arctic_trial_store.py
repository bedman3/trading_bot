import threading

import pandas as pd
from arctic import Arctic, TICK_STORE

if __name__ == '__main__':
    arctic = Arctic('mongodb://martin:martin@localhost')
    arctic.initialize_library('test_tick_store', lib_type=TICK_STORE)

    test_tick_store_lib = arctic['test_tick_store']

    columns = ['Update Message Type', 'Date', 'Nanoseconds', 'Ticker', 'Bid Size', 'Bid Price', 'Mid Price',
               'Ask Price', 'Ask Size', 'Last Price', 'Last Size', 'Halted', 'After Hours',
               'Intermarket Sweep Order (ISO)', 'Oddlot', 'NMS Rule 611']

    print('reading csv')
    iex_df = pd.read_csv('iex_201219_parse.txt', header=None, names=columns)
    print('set index to Date')
    iex_df.set_index('Date', inplace=True)
    print('convert index')
    iex_df.index = pd.to_datetime(iex_df.index)

    print('initialize semaphore')
    semaphore = threading.Semaphore(10)
    threads = []
    counter = 1

    def process_symbol(symbol):
        semaphore.acquire()
        global counter
        print(counter, symbol)
        set_df = iex_df[iex_df['Ticker'] == symbol]
        try:
            test_tick_store_lib.write(symbol, set_df)
        except Exception as e:
            print(e)
            # pass
        counter += 1
        semaphore.release()

    print('get symbols set')
    set_symbols = set(filter(lambda x: x == x, iex_df['Ticker']))
    print('Start')
    for symbol in set_symbols:
        print(symbol)
        thread = threading.Thread(target=process_symbol, args=symbol)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print('End')