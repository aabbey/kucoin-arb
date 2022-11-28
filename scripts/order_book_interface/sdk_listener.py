import asyncio
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient

symbols_used = {"BTC-USDT", "ETH-USDT", "ETH-BTC"}
order_book_all = dict.fromkeys(symbols_used)


async def main():
    async def handle_msg(msg):
        symbol = msg['topic'].split(':', 1)[1]
        order_book_all[symbol] = msg['data']
    client = WsToken()

    ws_client = await KucoinWsClient.create(None, client, handle_msg, private=False)
    await ws_client.subscribe('/spotMarket/level2Depth5:' + ','.join(symbols_used))
    while True:
        await asyncio.sleep(1)
        print(order_book_all)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
