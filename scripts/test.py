import numpy as np
import timeit
from scripts.cycle_logic import cycle_logic
from pre_processing import pre_process
from kucoin.market import market


if __name__ == "__main__":
    """all_sym = market.MarketData().get_symbol_list()
    sym_list = []
    for s in all_sym:
        sym_list.append(s['symbol'])
    print('ADA-USDT' in sym_list)"""



    order_book_all = pre_process.init_order_book()
    am = cycle_logic.order_book_to_adj_mat(order_book_all)
    cv = cycle_logic.calc_cycle_scores(am, [(0, 0, 0, 0),
                                            (1, 3, 3, 2),
                                            (3, 1, 2, 3)])
    print(am)
    print(cv)

