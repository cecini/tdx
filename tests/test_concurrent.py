from six import PY2

if not PY2:
    from tdx.engine import ConcurrentApi, Engine
    from datetime import datetime
    from pytdx.hq import TdxHq_API
    import time


    def concurrent_api(num=4):
        capi = ConcurrentApi(thread_num=num)
        now = datetime.now()
        data = {capi.get_security_list(0, 100) for i in range(100)}
        dd = [i.result() for i in data]
        return (datetime.now() - now).total_seconds()


    def normal_api():
        api = TdxHq_API()
        api.connect()
        now = datetime.now()
        dd = [api.get_security_list(0, 100) for i in range(100)]
        return (datetime.now() - now).total_seconds()


    def concurrent_quotes(code,best_ip,num=4):
        capi = ConcurrentApi(thread_num=num, ip=best_ip)
        now = datetime.now()
        data = {capi.get_security_quotes(
            code[80 * pos:80 * (pos + 1)]) for pos in range(int(len(code) / 80) + 1)}

        dd = [i.result() for i in data]
        return (datetime.now() - now).total_seconds()


    def normal_quotes(code,best_ip):
        api = TdxHq_API()
        api.connect(best_ip)
        now = datetime.now()
        data = [api.get_security_quotes(
            code[80 * pos:80 * (pos + 1)]) for pos in range(int(len(code) / 80) + 1)]
        return (datetime.now() - now).total_seconds()


    def concurrent_engine_quotes(num=4):
        engine = Engine(best_ip=True, thread_num=num)
        engine.connect()
        engine.stock_list.index.tolist()
        now = datetime.now()
        engine.stock_quotes()
        return (datetime.now() - now).total_seconds()


    def normal_engine_quotes():
        engine = Engine(best_ip=True)
        engine.connect()
        engine.stock_list.index.tolist()
        now = datetime.now()
        engine.stock_quotes()
        return (datetime.now() - now).total_seconds()


    def test_security_list():
        engine = Engine(best_ip=True)
        engine.connect()
        code = engine.stock_list.index.tolist()
        api = TdxHq_API()
        api.connect()
        best_ip = engine.best_ip

        concurrent_api(2)
        normal_api()

        concurrent_quotes(code,best_ip,2)
        normal_quotes(code,best_ip)

        concurrent_engine_quotes(2)
        normal_engine_quotes()
