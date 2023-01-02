import asyncio
import json
import pandas as pd

# import matplotlib.pyplot as plt
import timeit
import numpy as np
from order_book_interface import sdk_listener
import pre_processing.constants as c
from cycle_logic import cycle_logic
from pre_processing import pre_process
from machine_learning import symbol_score_prediction as ml


SYMBOLS_USED = ["BTC-USDT", "ETH-USDT", "ETH-BTC", "ADA-BTC", "ADA-USDT"]

if __name__ == "__main__":

    df = pd.read_json('symbol_scores.txt')
    print(df.head(30))
    print(len(df))
    x, y = ml.create_dataset_from_scores(df, 1220)
    x = x / np.mean(x)
    print(len(x), len(y), len(y[y != 1.]))
    print(max(x))
    x = x[np.where(x > 1.001)]
    y = y[np.where(x > 1.001)]
    x = x / np.mean(x)

    print(len(y))

    ml.training_loop(x[:, np.newaxis, np.newaxis], y[:, np.newaxis, np.newaxis])
    """plt.plot(df['am'])
    plt.show()"""



