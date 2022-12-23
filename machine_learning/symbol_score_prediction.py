import numpy as np


def create_dataset_from_scores(symbol_scores, future_steps):
    """
    makes training data to fit the equation : y = (x+w1)^w2, where :
        x = symbol value at t0
        y = ratio of how much the price has changed
        w1 = small value to add to x to help fit
        w2 = raising a value close to 1 to this to get a prediction for y
    :param future_steps: int of how far to make target y in the future
    :param symbol_scores: dataframe of each symbol score over time period
    :return:
    """
