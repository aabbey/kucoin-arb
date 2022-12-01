


async def make_trade_from_queue(queue):
    msg = await queue.get()
    print(f"Got {msg}. Posting {msg.symbol=}")
    data = {
        'symbol': msg.symbol,
        'type': 'market',
        'clientOid': str(uuid.uuid4()).replace('-', '')
    }
    if msg.in_order:
        data['funds'] = round(msg.amount, msg.decimal_places)
        data['side'] = 'sell'
    else:
        data['size'] = round(msg.amount, msg.decimal_places)
        data['side'] = 'buy'
    r = await api_endpoints.post_order(data)
    queue.task_done()