from tdx.engine import Engine,ExEngine
import datetime

engine = Engine(auto_retry=True,multithread=True)
engine.connect()

while True:
    quotes = engine.stock_quotes()
    print(datetime.datetime.now(),quotes.shape)

engine.exit()
