from tdx.engine import Engine, AsyncEngine


def test_engine():
    yield engine_func, True, 4


def test_async_engine():
    engine = AsyncEngine(best_ip=True)

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
    eg = Engine(best_ip=True)
    eg.connect()
    m1 = eg.get_security_bars('000001', '1m')
    df = eg.time_and_price('000001')
    ohlcv = df.price.resample('1 Min', label='right', closed='left').ohlc()
    ohlcv['volume'] = df.vol.resample('1 Min', label='right', closed='left').sum()


transactions()
