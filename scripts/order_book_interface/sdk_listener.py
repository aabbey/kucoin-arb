import asyncio
import json
import sys

import numpy as np
import timeit
from cycle_logic import cycle_logic
from pre_processing import pre_process
import pre_processing.constants as c
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient


async def main(order_book_all, client, cycle_indicies, cycles_with_symbol):
    stored_cycle_vals = []
    stored_symbol_scores = []
    cycle_indicies_str = [str(x) for x in cycle_indicies.T]
    stored_cycle_vals_dict = dict(zip(cycle_indicies_str, [[]]*len(list(cycle_indicies.T))))
    ind_for_sym_str = [str(x) for x in c.IND_FOR_SYM]
    stored_symbol_scores_dict = dict(zip(ind_for_sym_str, [[]]*len(c.IND_FOR_SYM)))
    count = 0

    async def handle_msg(msg):
        # get symbol and update the local order book
        symbol = msg['topic'].split(':', 1)[1]
        order_book_all[symbol] = msg['data']

        # calculate cycle values and average cycle values per symbol
        am = cycle_logic.order_book_to_adj_mat(order_book_all)
        cv = cycle_logic.calc_cycle_scores(am, cycle_indicies, False)
        cv_av_per_symbol = np.dot(cycles_with_symbol, cv)

        # store info for training
        stored_cycle_vals.append(cv)
        stored_symbol_scores.append(cv_av_per_symbol)

    ws_client = await KucoinWsClient.create(None, client, handle_msg, private=False)
    await ws_client.subscribe('/spotMarket/level2Depth5:' + ','.join(c.SYMBOLS_USED))
    while True:
        await asyncio.sleep(5)
        save_cycle_values(stored_cycle_vals, stored_cycle_vals_dict)
        save_symbol_scores(stored_symbol_scores, stored_symbol_scores_dict)
        sys.exit()


def save_cycle_values(stored_cycle_vals, stored_cycle_vals_dict):
    stored_cycle_vals_v = np.array(stored_cycle_vals).T
    stored_cycle_vals_dict = dict(zip(stored_cycle_vals_dict.keys(), stored_cycle_vals_v.tolist()))
    with open('cycle_values.txt', 'w') as convert_file:
        convert_file.write(json.dumps(stored_cycle_vals_dict))


def save_symbol_scores(stored_symbol_scores, stored_symbol_scores_dict):
    stored_symbol_scores_v = np.array(stored_symbol_scores).T
    print(np.shape(stored_symbol_scores_v))
    stored_symbol_scores_dict = dict(zip(stored_symbol_scores_dict.keys(), stored_symbol_scores_v.tolist()))
    '''i = 0
    for key, value in stored_symbol_scores_dict.items():
        stored_symbol_scores_dict[key].extend(stored_symbol_scores_v[i].tolist())
        i += 1'''
    with open('symbol_scores.txt', 'w') as convert_file:
        convert_file.write(json.dumps(stored_symbol_scores_dict))

"""async def scanning_loop():
    scanning_task = asyncio.create_task(main())
    await scanning_task"""


"""if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())"""
