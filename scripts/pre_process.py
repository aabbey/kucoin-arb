from kucoin.client import WsToken
from kucoin.client import Market
import os


symbols_used = {"BTC-USDT", "ETH-USDT", "ETH-BTC"}
config = {
    "key": os.getenv('API_KEY'),
    "secret": os.getenv('API_SECRET'),
    "passphrase": os.getenv('API_PASSPHRASE'),
    "is_sandbox": False,
}

market_client = Market(**config)


def init_order_book():
    full_ob = dict.fromkeys(symbols_used)
    for s in symbols_used:
        ob = market_client.get_aggregated_orderv3(symbol=s)
        ob['bids'] = ob['bids'][:5]
        ob['asks'] = ob['asks'][:5]
        full_ob[s] = ob
        full_ob[s]['timestamp'] = full_ob[s].pop('time')
    return full_ob


def build_graph():
    pass


def find_cycles(symbols):
    cycles_with_symbol = {}
    for s in symbols:
        b, q = s.split('-')
