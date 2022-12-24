import numpy as np
from ast import literal_eval


def create_dataset_from_scores(symbol_scores, future_steps):
    """
    makes training data to fit the equation : y = (x+w1)^w2, where :
        x = symbol value at t0
        y = ratio of how much the price has changed
        w1 = small value to add to x to help fit
        w2 = raising a value close to 1 to this to get a prediction for y
    :param future_steps: int of how far to make target y in the future
    :param symbol_scores: dataframe of each symbol score over time period
    :return: x and y training data
    """
    tot_len = len(symbol_scores)
    if future_steps >= tot_len:
        return 'sample too small'

    a1 = list(symbol_scores.columns.values)
    a2 = symbol_scores.drop('am', axis=1).to_numpy()
    a1 = [literal_eval(x) for x in a1[:-1]]
    a3 = symbol_scores['am'].to_list()
    a3 = np.array(a3)
    a1 = np.asarray(a1)
    top_slice = slice(0, tot_len-future_steps)
    bottom_slice = slice(future_steps, tot_len)

    x = a2[top_slice].flatten()
    y = a3[bottom_slice, a1[:, 0], a1[:, 1]] / a3[top_slice, a1[:, 0], a1[:, 1]]
    y = y.flatten()
    return x, y
