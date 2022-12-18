import timeit
import numpy as np

import pre_processing.constants
from cycle_logic import cycle_logic
from pre_processing import pre_process


SYMBOLS_USED = ["BTC-USDT", "ETH-USDT", "ETH-BTC", "ADA-BTC", "ADA-USDT"]

if __name__ == "__main__":
    """all_sym = market.MarketData().get_symbol_list()
    sym_list = []
    for s in all_sym:
        sym_list.append(s['symbol'])
    print('ADA-USDT' in sym_list)"""


    order_book_all = pre_process.init_order_book()
    print(pre_processing.constants.SYMBOLS_USED)
    am = cycle_logic.order_book_to_adj_mat(order_book_all)
    print(am)
    cycle_indicies = pre_process.find_cycles(am)
    print(cycle_indicies)
    cycles_with_symbol = pre_process.find_cycles_with_symbol(cycle_indicies)
    print(cycles_with_symbol)
    cv = cycle_logic.calc_cycle_scores(am, cycle_indicies, False)
    cv_av_per_symbol = np.dot(cycles_with_symbol, cv)

    print(cv)
    print(cv_av_per_symbol)

