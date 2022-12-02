import numpy as np
from pre_processing import variables

cycle_fees = np.array([(1-.0008)**3]*4)


def calc_cycle_scores(adj_mat, cycle_index_tuple, with_fee=True):
    """
    :param adj_mat: current state of the orderbook best bids and asks
    :param cycle_index_tuple: list of tuples (length of 3 if only 3-cycles) tuples represent indices of adj mat that form cycles
    :return:
    """
    cycle_lengths = len(cycle_index_tuple)
    num_cycles = len(cycle_index_tuple[0])
    step_scores = np.ones(shape=(cycle_lengths, num_cycles))
    for step in range(cycle_lengths):
        step_scores[step] = adj_mat[cycle_index_tuple[step], cycle_index_tuple[(step+1) % cycle_lengths]]

    cycle_values = np.prod(step_scores, axis=0)
    if with_fee:
        cycle_values *= cycle_fees

    return cycle_values


def order_book_to_adj_mat(order_book):
    """

    :param order_book: full order ook all
    :return: numpy matrix that is adjacency matrix for best bids and asks
    """
    ad_mat = np.zeros(shape=(variables.num_curr, variables.num_curr))
    for symbol, ob in order_book.items():
        b, q = symbol.split('-')
        x_index, y_index = (variables.currencies.index(b), variables.currencies.index(q))
        ad_mat[x_index, y_index] = float(ob['bids'][0][0])
        ad_mat[y_index, x_index] = 1 / float(ob['asks'][0][0])

    return ad_mat