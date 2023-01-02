import numpy as np
from ast import literal_eval

zoom_number = 5
grid_shape = (5, 5)


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


def cost(y_pred, y_true):
  c = np.sum((y_pred - y_true) ** 2, axis=0)
  return np.unravel_index(np.argmin(c), c.shape), np.min(c)

def training_loop(x_train, y_train):
    range_1 = 0.0
    range_2 = 1.8
    mid_1 = 0.0
    mid_2 = 0.5
    for zoom in range(10):
        w1_space = np.linspace(mid_1 - range_1, mid_1 + range_1, 50)
        w2_space = np.linspace(mid_2 - range_2, mid_2 + range_2, 50)

        grid = np.array(np.meshgrid(w1_space, w2_space))

        y = np.power((x_train + grid[np.newaxis, :][:, 0]), grid[np.newaxis, :][:, 1])

        cost_args, c = cost(y, y_train)
        print(grid[:, cost_args[0], cost_args[1]], c)
        range_1 /= 1.7
        range_2 /= 1.7
        mid_1 = grid[0, cost_args[0], cost_args[1]]
        mid_2 = grid[1, cost_args[0], cost_args[1]]


