import asyncio
import json
import pandas as pd

import matplotlib.pyplot as plt
import timeit
import numpy as np
from order_book_interface import sdk_listener
import pre_processing.constants as c
from cycle_logic import cycle_logic
from pre_processing import pre_process


SYMBOLS_USED = ["BTC-USDT", "ETH-USDT", "ETH-BTC", "ADA-BTC", "ADA-USDT"]

if __name__ == "__main__":

    df = pd.read_json('cycle_values.txt')
    print(df.head())
    print(len(df))

    plt.plot(df['[2 5 4 2]'])
    plt.show()



