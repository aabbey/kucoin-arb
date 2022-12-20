from kucoin.client import WsToken
from kucoin.client import Market
import os
import numpy as np
from pre_processing import constants


CYCLE_LEN = 3


def init_order_book():
    full_ob = dict.fromkeys(constants.SYMBOLS_USED)
    for s in constants.SYMBOLS_USED:
        ob = constants.market_client.get_part_order(pieces=20, symbol=s)
        ob['bids'] = ob['bids'][:5]
        ob['asks'] = ob['asks'][:5]
        full_ob[s] = ob
        full_ob[s]['timestamp'] = full_ob[s].pop('time')
    return full_ob


def build_graph():
    pass


def append_next_currs(traj_in, adj_mat, cycle_over=False):
    curr_in = traj_in[-1]
    next_currs = np.where(adj_mat[curr_in] != 0)[0]
    trajs_out = []
    for c in next_currs:
        if cycle_over:
            if c == traj_in[0]:
                trajs_out.append(traj_in + [c])
        else:
            if c not in traj_in:
                trajs_out.append(traj_in + [c])

    return trajs_out


def find_cycles(adjacency_matrix):
    cycle_indicies = []
    adj_mat = adjacency_matrix.copy()
    for start_curr in range(len(adj_mat[0]) - 2):
        cycle_over_flag = False
        all_trajs = [[0]]
        new_trajs = append_next_currs(all_trajs[0], adj_mat)
        for t in new_trajs:
            all_trajs.append(t)
        for level in range(CYCLE_LEN - 1):
            if level == CYCLE_LEN - 2:
                cycle_over_flag = True
            for traj in all_trajs:
                if len(traj) == 2 + level:
                    new_trajs = append_next_currs(traj, adj_mat, cycle_over_flag)
                    for t in new_trajs:
                        all_trajs.append(t)

        for l in all_trajs:
            if len(l) == CYCLE_LEN + 1:
                if start_curr > 0:
                    cycle_indicies.append([x + start_curr for x in l])
                else:
                    cycle_indicies.append(l)

        adj_mat = adj_mat[1:, 1:]

    return np.array(cycle_indicies).T


def ind_for_sym():
    ind_sym = []
    for s in constants.SYMBOLS_USED:
        b, q = s.split('-')
        ind_sym.append((constants.CURRENCIES.index(b), constants.CURRENCIES.index(q)))
    return ind_sym



def find_cycles_with_symbol(cycle_indicies):
    symbols_index = ind_for_sym()
    true_list = np.zeros(shape=(len(constants.SYMBOLS_USED), len(cycle_indicies[0])))
    for sym_num, sym in enumerate(symbols_index):
        first, second = sym
        for col_num, col in enumerate(cycle_indicies.T):
            if first in col and col[list(col).index(first) + 1] == second:
                true_list[sym_num][col_num] = 1.
    tl_strd = true_list / np.expand_dims(np.sum(true_list, axis=1), axis=1)
    return tl_strd