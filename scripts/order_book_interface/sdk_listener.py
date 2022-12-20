import asyncio
import numpy as np
import timeit
from cycle_logic import cycle_logic
from pre_processing import pre_process
import pre_processing.constants as c
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient

# order_book_all = pre_process.init_order_book()
# client = WsToken(pre_process.config)


async def main(order_book_all, client, cycle_indicies, cycles_with_symbol):
    async def handle_msg(msg):
        s = timeit.default_timer()
        symbol = msg['topic'].split(':', 1)[1]
        order_book_all[symbol] = msg['data']
        am = cycle_logic.order_book_to_adj_mat(order_book_all)
        cv = cycle_logic.calc_cycle_scores(am, cycle_indicies, False)
        cv_av_per_symbol = np.dot(cycles_with_symbol, cv)
        print(timeit.default_timer() - s)


    ws_client = await KucoinWsClient.create(None, client, handle_msg, private=False)
    await ws_client.subscribe('/spotMarket/level2Depth5:' + ','.join(c.SYMBOLS_USED))
    while True:
        await asyncio.sleep(1)


"""async def scanning_loop():
    scanning_task = asyncio.create_task(main())
    await scanning_task"""


"""if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())"""
