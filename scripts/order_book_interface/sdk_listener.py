import asyncio
import numpy as np
from scripts import pre_process
from scripts.trading_scripts import trading
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient

order_book_all = pre_process.init_order_book()
client = WsToken(pre_process.config)


async def main():
    async def handle_msg(msg):
        symbol = msg['topic'].split(':', 1)[1]
        order_book_all[symbol] = msg['data']


    ws_client = await KucoinWsClient.create(None, client, handle_msg, private=False)
    await ws_client.subscribe('/spotMarket/level2Depth5:' + ','.join(pre_process.symbols_used))
    while True:
        await asyncio.sleep(1)
        print(order_book_all['BTC-USDT'])


async def scanning_loop():
    scanning_task = asyncio.create_task(main())
    await scanning_task


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
