from tdx.engine import Engine


def test_engine():
    yield engine_func, True, 1
    yield engine_func, False, 4


def engine_func(best_ip, thread_num):
    engine = Engine(best_ip=best_ip, thread_num=thread_num)

    with engine.connect():
        assert engine.best_ip is not None
        assert engine.gbbq is not None
        assert engine.security_list is not None
        assert engine.stock_quotes() is not None
        assert engine.customer_block is not None
        assert engine.quotes('000001') is not None
        assert engine.get_security_bars('000001', '1m') is not None
        assert engine.get_security_bars('000001', '1d') is not None
        assert engine.get_security_bars('000300', '1m', index=True) is not None
        assert engine.get_security_bars('000300', '1d', index=True) is not None
        assert engine.concept is not None
        assert engine.fengge is not None
        assert engine.index is not None
        assert engine.stock_list is not None


def transactions():
    eg = Engine()
    eg.connect()
    # df = eg.get_k_data('000001','20171117','20171117',freq='1 Min')
    # df = eg.time_and_price('000001').price.resample('1 Min',label='right',closed='left').ohlc()
    print(eg._get_transaction('000001',20171117).price)
    print(eg.time_and_price('000001').price)
    # print(df)

transactions()
