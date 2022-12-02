from kucoin.client import WsToken
from kucoin.client import Market
import os
from pre_processing import variables



def init_order_book():
    full_ob = dict.fromkeys(variables.symbols_used)
    for s in variables.symbols_used:
        ob = variables.market_client.get_aggregated_orderv3(symbol=s)
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
