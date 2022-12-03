import os
from kucoin.client import Market


symbols_used = {"BTC-USDT", "ETH-USDT", "ETH-BTC", "ADA-BTC", "ADA-USDT"}
config = {
    "key": os.getenv('API_KEY'),
    "secret": os.getenv('API_SECRET'),
    "passphrase": os.getenv('API_PASSPHRASE'),
    "is_sandbox": False,
}

market_client = Market(**config)


def get_unique_curr(symbols):
    full_list = []
    for s in symbols:
        b, q = s.split('-')
        full_list.append(b)
        full_list.append(q)
    return set(full_list)


currencies = sorted(list(get_unique_curr(symbols_used)))
print(currencies)
num_curr = len(currencies)
num_cycles = 4
