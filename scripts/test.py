import timeit
import numpy as np
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
    cycles_with_symbol = np.array([[0.5, 0, 0.5, 0],
                                [0, 0, 0, 1],
                                [0, 0, 1, 0],
                                [1, 0, 0, 0],
                                [0, 1, 0, 0]])

    s = timeit.default_timer()
    am = cycle_logic.order_book_to_adj_mat(order_book_all)
    e1 = timeit.default_timer()
    cv = cycle_logic.calc_cycle_scores(am, [(0, 0, 1, 1),
                                            (1, 3, 3, 2),
                                            (3, 1, 2, 3)],
                                       False)
    cv_av_per_curr = np.dot(cycles_with_symbol, cv)

    print(cv)
    print(cv_av_per_curr)

