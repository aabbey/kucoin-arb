import os
from kucoin.client import Market, WsToken


SYMBOLS_USED = ["BTC-USDT", "ETH-USDT", "ETH-BTC", "ADA-BTC", "ADA-USDT", "DOGE-BTC", "DOGE-USDT", "KCS-ETH",
                "KCS-BTC", "KCS-USDT", "ADA-KCS", "DOGE-KCS"]
config = {
    "key": os.getenv('API_KEY'),
    "secret": os.getenv('API_SECRET'),
    "passphrase": os.getenv('API_PASSPHRASE'),
    "is_sandbox": False,
}

market_client = Market(**config)
ws_client = WsToken(**config)


def get_unique_curr(symbols):
    full_list = []
    for s in symbols:
        b, q = s.split('-')
        full_list.append(b)
        full_list.append(q)
    return set(full_list)


def find_cycles(adj_mat):
    pass


CURRENCIES = sorted(list(get_unique_curr(SYMBOLS_USED)))
print(CURRENCIES)
num_curr = len(CURRENCIES)
num_cycles = 4
