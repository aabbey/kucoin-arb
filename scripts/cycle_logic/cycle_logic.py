import numpy as np


def calc_cycle_scores(adj_mat, cycle_index_tuple):
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

    return cycle_values


def order_book_to_adj_mat(order_book):
    """

    :param order_book: full order ook all
    :return: numpy matrix that is adjacency matrix for best bids and asks
    """


    return 3