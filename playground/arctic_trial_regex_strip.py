import json
import re

import pymongo
from arctic import Arctic, TICK_STORE

if __name__ == '__main__':
    arctic = Arctic('localhost')
    arctic.initialize_library('test_tick_store', lib_type=TICK_STORE)

    test_tick_store_lib = arctic['test_tick_store']
    #
    # regex_pattern = r'{\"messageType\": \"A\", \"data\": \[\"([A-Z])\", \"([0-9a-zA-Z\S]*)\", ([a-zA-Z0-9]+), \"([a-zA-Z0-9]+)\", ([a-zA-Z0-9\W]*)\], .*'
    # file_name = 'iex_201219.txt'
    # txt_file = open(file_name, 'r')
    # write_txt_file = open(f'{file_name[:-4]}_parse.txt', 'w+')
    #
    #
    # def regex_parse(line: str):
    #     re_match = re.match(regex_pattern, line)
    #     if re_match is not None:
    #         write_txt_file.write(','.join(re_match.groups()).replace(' ', '') + '\n')
    #
    #
    # print('parsing')
    # for line in txt_file:
    #     regex_parse(line)
