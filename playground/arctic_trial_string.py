import json

import pymongo
# from arctic import Arctic, TICK_STORE

if __name__ == '__main__':
    # arctic = Arctic('localhost')
    # arctic.initialize_library('test_tick_store', lib_type=TICK_STORE)
    #
    # test_tick_store_lib = arctic['test_tick_store']

    file_name = 'iex_201219.txt'
    txt_file = open(file_name, 'r')
    write_txt_file = open(f'{file_name[:-4]}_parse.txt', 'w+')


    def string_parse(line: str):
        dict_obj = json.loads(line)
        if dict_obj['messageType'] == 'A':
            write_txt_file.write(f"{','.join(str(item) for item in dict_obj['data'])}\n")


    print('parsing')
    for line in txt_file:
        string_parse(line)
