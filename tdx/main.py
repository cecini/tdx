# -*- coding:utf-8 –*-

from tdx.engine import Engine,ExEngine
import time
import datetime
from tdx.utils.round import precise_round


# def process_quotes(quotes):
#     quotes['change'] = quotes['price'] / quotes['last_close'] - 1
#     quotes['up_limit'] = (quotes['last_close'] * 1.1).apply(precise_round) == quotes['price']
#     quotes['down_limit'] = (quotes['last_close'] * 0.9).apply(precise_round) == quotes['price']
#     quotes.sort_values('change', ascending=False, inplace=True)
#     quotes.set_index('code',inplace=True)
#     quotes = engine.concept.set_index('code').join(quotes)
#     quotes.to_csv('quotes.csv',encoding='gbk')
#     grouped = quotes.groupby('blockname').sum()[['up_limit','down_limit','amount']]
#     grouped.to_csv('groupby.csv',encoding='gbk')
#
#
# def test_minute_time_data():
#     stock_list = engine.stock_list.index.tolist()
#
#     now = datetime.datetime.now()
#
#     for stock in stock_list:
#         fs = engine.api.to_df(engine.api.get_minute_time_data(stock[0], stock[1]))
#         # print(fs)
#
#     print((datetime.datetime.now() - now).total_seconds())
#
#
# def test_quotes():
#     # while True:
#     quote = engine.stock_quotes()
#     process_quotes(quote)

# engine = Engine(auto_retry=True,multithread=True,best_ip=True,thread_num=8)
# engine.connect()
#
# test_quotes()
#
# engine.exit()

# data = open('blocknew.cfg','rb').read()
#
# pos = 0
#
#
# names = []
# while pos < len(data):
#     n1 = data[pos:pos+50].decode('gbk','ignore').rstrip("\x00")
#     n2 = data[pos+50:pos+120].decode('gbk', 'ignore').rstrip("\x00")
#     pos = pos + 120
#     names.append((n1,n2))
#
# print(names)

BlockReader_TYPE_FLAT = 0
BlockReader_TYPE_GROUP = 1

import pandas as pd
import os


class BlockReader(object):

    def get_df(self, fname, result_type=BlockReader_TYPE_FLAT):
        result = self.get_data(fname, result_type)
        return pd.DataFrame(result)

    def get_data(self, fname, result_type=BlockReader_TYPE_FLAT):

        result = []

        if not os.path.isdir(fname):
            raise NotADirectoryError

        block_file = os.path.join(fname,'blocknew.cfg')

        if not os.path.exists(block_file):
            raise FileNotFoundError

        block_data = open(block_file,'rb').read()

        pos = 0
        res = {}
        # print(block_data.decode('gbk','ignore'))
        while pos < len(block_data):
            n1 = block_data[pos:pos + 50].decode('gbk', 'ignore').rstrip("\x00")
            n2 = block_data[pos + 50:pos + 120].decode('gbk', 'ignore').rstrip("\x00")
            pos = pos + 120

            bf = os.path.join(fname,n2 + '.blk')
            if not os.path.exists(bf):
                raise FileNotFoundError

            codes = open(bf).read().splitlines()
            res[n1] = codes

        return res

block_reader = BlockReader()
res = block_reader.get_df('C:/Users/jayso/Desktop/blocknew')
print(res)