import time
import os
from kucoin.client import Market
import asyncio
from kucoin.ws_client import KucoinWsClient
from kucoin.client import WsToken
import queue
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
import uuid
import sys
import logging

lock = RLock()

logging.basicConfig(level=logging.INFO)  # level INFO
logger = logging.getLogger(__name__)

product_config = {
    "key": os.getenv('API_KEY'),
    "secret": os.getenv('API_SECRET'),
    "passphrase": os.getenv('API_PASSPHRASE'),
    "is_sandbox": False,
}


def get_uuid():
    return str(uuid.uuid4().hex)


def get_full_order_book(config, symbol):
    client = Market(**config)
    logger.info('init now')
    _book = client.get_aggregated_orderv3(symbol=symbol)
    update_time = _book['time']
    sequence = _book['sequence']
    update_bids = _book['bids']
    update_asks = _book['asks']
    logger.debug(sequence)
    logger.debug(len(update_bids))
    logger.debug(update_time)
    logger.debug(len(update_asks))
    logger.info('init api okay')
    return int(sequence), _book


def init_order_book(_order_book, config, update_info, symbol):
    """Start to pull orderbook"""
    while True:
        _order_book.clear()  # Ensure that the program runs consistently, clean up the data first
        sequence, init_book_data = get_full_order_book(config, symbol)  # Pull the full amount of data from the API once
        order_book(sequence, init_book_data, _order_book, update_info)
        logger.info('Need to re-pull data- so sleep 1s')
        time.sleep(1)


def order_book(_sequence, init_book_data, _order_book, update_info):
    _order_book.update(init_book_data)
    # If the data is not received within the specified time, an exception will be thrown over time
    latest = update_info.get(timeout=60)

    # Determine whether the serial number in the message is greater than the serial number in the order book
    if latest['data']['sequenceStart'] > _sequence:
        logger.info('Need to reinitialize')
    else:
        while True:
            sequence_start = latest['data']['sequenceStart']
            sequence = int(_order_book['sequence']) if _order_book else int(_sequence)
            # good! serial number in the message is equal the serial number in the order book
            if sequence_start == sequence:
                logger.info(str(_order_book)[0:100])  # Just print to look at a partial snapshot
                logger.info('good! serial number in the message is equal the serial number in the order book')

            elif sequence_start > sequence:
                # Must determine whether the serial number is connected
                if _order_book and int(_order_book['sequence']) + 1 == sequence_start:
                    logger.debug(f'{sequence_start} => Serial numbers are consecutive')
                    _order_book['sequence'] = sequence_start

                    for k, v in latest['data']['changes'].items():
                        if not v:
                            continue

                        old = _order_book[k]
                        logger.debug(f'before: {k} {len(old)}')
                        # 'bids'  # Sort from big to small
                        # 'asks' # Sort from small to large

                        for vi in v:  # Iterate over the changed data
                            vi_price = vi[0]
                            if vi_price == '0':
                                continue

                            vi_size = vi[1]
                            _match = False
                            for index, (price, size) in enumerate(old):
                                if vi_price == price:  # Same price
                                    logger.debug(f'Replace the new price：{vi}')
                                    old[index] = [vi_price, vi_size]  # Replace the new price
                                    _match = True
                                    break

                                # From big to small, the bigger the front.
                                if float(price) < float(vi_price) and k == 'bids':
                                    logger.debug(f'Insert new price{[vi_price, vi_size]}')
                                    old.insert(index, [vi_price, vi_size])
                                    _match = True
                                    break

                                # From small to large, the smaller the more advanced.
                                elif float(price) > float(vi_price) and k == 'asks':
                                    logger.debug(f'Insert new price{[vi_price, vi_size]}')
                                    old.insert(index, [vi_price, vi_size])
                                    _match = True
                                    break

                            if not _match:  # From big to small, the bigger the front.
                                logger.debug(f'End-insert new price{[vi_price, vi_size]}')
                                old.append([vi_price, vi_size])

                        # There may be a default value of 0
                        _order_book[k] = list(filter(lambda _v: float(_v[1]) > 0, old))

                        logger.debug(f'after: {k} {len(_order_book[k])}')
                else:
                    logger.info(f'{sequence_start} {sequence} {latest}')
                    logger.info('There is a message sequence number missing')
                    return
            else:
                logger.debug(f'Matching {sequence_start} /= {sequence}')

            latest = update_info.get(timeout=60)


async def product_deal_msg(msg):
    product_update_info.put_nowait(msg)


async def subscribe(token, topic, private=False, run_time=10, deal_msg=product_deal_msg):
    ws_client = await KucoinWsClient.create(None, token, deal_msg, private=private)
    await ws_client.subscribe(topic)
    await asyncio.sleep(run_time)  # How long to run


def thread_pool_callback(worker):
    print(f'{worker} Finish.')
    worker_exception = worker.exception()
    if worker_exception:
        logging.exception(worker_exception)
        sys.exit(-1)


def monitor_print_msg(data):
    """Just print the query data at regular intervals"""
    while True:
        if data:
            print(data['bids'][0:10])
            print(data['asks'][0:10])
        time.sleep(2)


product_order_book = dict()

product_update_info = queue.Queue()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor(max_workers=8)

    symbol = 'BTC-USDT'  # Configure trading pairs

    # orderbook
    future = pool.submit(init_order_book, product_order_book, product_config, product_update_info, symbol)
    future.add_done_callback(thread_pool_callback)

    # View orderbook data, or your own processing logic
    future = pool.submit(monitor_print_msg, product_order_book)
    future.add_done_callback(thread_pool_callback)

    loop.run_until_complete(
        subscribe(WsToken(**product_config), topic=f'/market/level2:{symbol}', deal_msg=product_deal_msg,
                  run_time=1000000)
    )
    loop.run_forever()