import pytest
from tdx.engine import Engine


@pytest.mark.parametrize("best_ip", [True, False])
@pytest.mark.parametrize("thread_num", [4,None])
def test_engine_func(best_ip, thread_num):
    engine = Engine(best_ip=best_ip,thread_num=thread_num)

    with engine.connect():
        assert engine.best_ip is not None
        assert engine.gbbq is not None
        assert engine.security_list is not None
        assert engine.stock_quotes() is not None
        assert engine.customer_block is not None
        assert engine.quotes('000001') is not None
        assert engine.get_security_bars('000001', '1m') is not None
        assert engine.get_security_bars('000001', '1D') is not None
        assert engine.get_security_bars('000300', '1m', index=True) is not None
        assert engine.get_security_bars('000300', '1m', index=True) is not None
        assert engine.concept is not None
        assert engine.fengge is not None
        assert engine.index is not None
        assert engine.stock_list is not None
