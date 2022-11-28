import asyncio
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient

async def main():
    async def handle_msg(msg):
        print(msg['data'])

    client = WsToken()

    ws_client = await KucoinWsClient.create(None, client, handle_msg, private=False)
    await ws_client.subscribe('/market/level2:BTC-USDT,ETH-USDT')
    while True:
        await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())