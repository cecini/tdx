from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API
import pandas as pd
from tdx.utils.memoize import lazyval
from pytdx.util.best_ip import select_best_ip
from concurrent.futures import ThreadPoolExecutor
import concurrent

def stock_filter(code):
    if code[0] == '6' or code[0] == '0':
        return True
    if code.startswith("300") or code.startswith("1318"):
        return True
    return False

class Engine:

    def __init__(self,*args,**kwargs):
        if kwargs.pop('best_ip', False):
            self.ip = self.best_ip
        else:
            self.ip = '101.227.73.20'

        self.thread_num = kwargs.pop('thread_num', 8)

        self.api = TdxHq_API(args,kwargs)
        self.apis = [TdxHq_API(args,kwargs) for i in range(self.thread_num)]

        self.executor = ThreadPoolExecutor(self.thread_num)


    def connect(self):
        self.api.connect(self.ip)
        for api in self.apis:
            api.connect(self.ip)


    def __enter__(self):
        return self

    def exit(self):
        self.api.disconnect()
        for api in self.apis:
            api.disconnect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.api.disconnect()
        for api in self.apis:
            api.disconnect()

    def quotes(self,code):
        code = [code] if not isinstance(code,list) else code
        code = self.security_list[self.security_list.code.isin(code)].index.tolist()
        data = [self.api.to_df(self.api.get_security_quotes(
                code[80 * pos:80 * (pos + 1)])) for pos in range(int(len(code) / 80) + 1)]
        return pd.concat(data)
        # data = data[['code', 'open', 'high', 'low', 'price']]
        # data['datetime'] = datetime.datetime.now()
        # return data.set_index('code', drop=False, inplace=False)

    def stock_quotes(self):
        code = self.stock_list.index.tolist()
        res = {self.executor.submit(self.apis[pos % self.thread_num].get_security_quotes,code[80 * pos:80 * (pos + 1)]) \
               for pos in range(int(len(code) / 80) + 1)}
        return pd.concat([self.api.to_df(dic.result()) for dic in res])

    @lazyval
    def security_list(self):
        return pd.concat(
            [pd.concat([self.api.to_df(self.api.get_security_list(j, i * 1000)).assign(sse=0 if j == 0 else 1).set_index(
                ['sse', 'code'], drop=False) for i in range(int(self.api.get_security_count(j) / 1000) + 1)], axis=0) for j
                in
                range(2)], axis=0)

    @lazyval
    def stock_list(self):
        return self.security_list[self.security_list.code.apply(stock_filter)]

    @lazyval
    def best_ip(self):
        return select_best_ip()


class ExEngine:
    def __init__(self,*args,**kwargs):
        self.api = TdxExHq_API(args,kwargs)

    def connect(self):
        self.api.connect('61.152.107.141', 7727)

    def __enter__(self):
        return self

    def exit(self):
        self.api.disconnect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.api.disconnect()

    @lazyval
    def markets(self):
        return self.api.to_df(self.api.get_markets())