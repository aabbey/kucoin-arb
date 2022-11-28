import asyncio
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient

order_book_all = {"BTC-USDT", "ETH-USDT"}


async def main():
    async def handle_msg(msg):
        print(msg)

    client = WsToken()

    ws_client = await KucoinWsClient.create(None, client, handle_msg, private=False)
    await ws_client.subscribe('/spotMarket/level2Depth5:BTC-USDT,ETH-USDT')
    while True:
        await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
