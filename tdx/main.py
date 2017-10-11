# -*- coding:utf-8 –*-

from tdx.engine import Engine,ExEngine
import time
import datetime
from tdx.utils.round import precise_round


def process_quotes(quotes):
    quotes['change'] = quotes['price'] / quotes['last_close'] - 1
    quotes['up_limit'] = (quotes['last_close'] * 1.1).apply(precise_round) == quotes['price']
    quotes['down_limit'] = (quotes['last_close'] * 0.9).apply(precise_round) == quotes['price']
    quotes.sort_values('change', ascending=False, inplace=True)
    quotes.set_index('code',inplace=True)
    quotes = engine.concept.set_index('code').join(quotes,how='inner')
    quotes.to_csv('quotes.csv',encoding='gbk')
    grouped = quotes.groupby('blockname').sum()[['up_limit','down_limit','amount']]
    grouped.to_csv('groupby.csv',encoding='gbk')


def test_minute_time_data():
    stock_list = engine.stock_list.index.tolist()

    now = datetime.datetime.now()

    for stock in stock_list:
        fs = engine.api.to_df(engine.api.get_minute_time_data(stock[0], stock[1]))
        # print(fs)

    print((datetime.datetime.now() - now).total_seconds())


def test_quotes():
    # while True:
    quote = engine.stock_quotes()
    process_quotes(quote)

engine = Engine(auto_retry=True,multithread=True,best_ip=True,thread_num=8)
engine.connect()

test_quotes()

engine.exit()
