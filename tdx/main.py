from tdx.engine import Engine,ExEngine
import time
import datetime

# data['change'] = data['price'] / data['last_close'] - 1
# data['up_limit'] = (data['last_close'] * 1.1).apply(precise_round)
# data['down_limit'] = (data['last_close'] * 0.9).apply(precise_round)

engine = Engine(auto_retry=True,multithread=True,best_ip=True,thread_num=8)
engine.connect()

while True:
    now = datetime.datetime.now()
    print(engine.stock_quotes().shape,(datetime.datetime.now() - now).total_seconds())

engine.exit()
