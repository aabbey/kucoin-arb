import asyncio
import websockets
import json
import requests
from kucoin.asyncio import KucoinSocketManager
from kucoin.client import Client
import os

'''KEY = os.getenv('API_KEY')
SECRET = os.getenv('API_SECRET')
PASSPHRASE = os.getenv('API_PASSPHRASE')'''

# CLIENT = Client(KEY, SECRET, PASSPHRASE)
base_url = "https://api.kucoin.com"
ws_url = "/api/v1/bullet-public"
ws_endpoint = 'wss://ws-api.kucoin.com/endpoint'
uuid = "Hdd2033"
TICKER_ALL_API_ENDPOINT = '/market/ticker:all'


async def listen():
    async with websockets.connect('wss://ws-api.kucoin.com/endpoint?token=%s&[connectId=%s]' % (token, uuid)) as ws:
        out_msg = json.dumps({"id": "%s" % uuid,
                              "type": "subscribe",
                              "topic": "/market/level2:BTC-USDT,ETH-USDT",
                              "response": True})
        await ws.send(out_msg)
        count = 0
        while True:
            msg = await ws.recv()
            count += 1
            print(msg)


if __name__ == "__main__":
    response = json.loads(requests.post(base_url + ws_url).text)
    token = response['data']['token']
    asyncio.get_event_loop().run_until_complete(listen())
