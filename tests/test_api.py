from pytdx.hq import TdxHq_API
import pandas as pd
import datetime
from six import PY2


def test_api():
    ip = '14.17.75.71'
    api = TdxHq_API()
    api.connect(ip)

    freq = 8
    exchange = 0
    code = '000001'
    SECURITY_BARS_PATCH_SIZE = 800
    SECURITY_BARS_PATCH_NUM2 = 30

    now = datetime.datetime.now()
    for i in range(3):
        dd = [api.get_security_bars(freq, exchange, code,
                                    (SECURITY_BARS_PATCH_NUM2 - i - 1) * SECURITY_BARS_PATCH_SIZE,
                                    SECURITY_BARS_PATCH_SIZE) for i in range(SECURITY_BARS_PATCH_NUM2)]

    print((datetime.datetime.now() - now).total_seconds())


if not PY2:
    from tdx.engine import ConcurrentApi


    def test_concurrent_minute_bars():
        best_ip = '14.17.75.71'
        num = 2

        capi = ConcurrentApi(thread_num=num, ip=best_ip)

        freq = 8
        exchange = 0
        code = '000001'
        SECURITY_BARS_PATCH_SIZE = 800
        SECURITY_BARS_PATCH_NUM2 = 30

        now = datetime.datetime.now()
        for i in range(3):
            data = {capi.to_df(
                capi.get_security_bars(freq, exchange, code,
                                       (SECURITY_BARS_PATCH_NUM2 - i - 1) * SECURITY_BARS_PATCH_SIZE,
                                       SECURITY_BARS_PATCH_SIZE)) for i in
                range(SECURITY_BARS_PATCH_NUM2)}
            dd = [i.result() for i in data]

        print((datetime.datetime.now() - now).total_seconds())
