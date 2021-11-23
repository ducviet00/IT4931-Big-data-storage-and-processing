import os
import sys
import json
from asyncio import gather, get_event_loop
from datetime import datetime

import requests

# -----------------------------------------------------------------------------

this_folder = os.path.dirname(os.path.abspath("."))
root_folder = os.path.dirname(os.path.dirname(this_folder))
sys.path.append(root_folder + "/python")
sys.path.append(this_folder)

# -----------------------------------------------------------------------------

import ccxt.async_support as ccxt  # noqa: E402

# -----------------------------------------------------------------------------


print("CCXT Version:", ccxt.__version__)


def put_data(candles, index):

    headers = {
        "Content-Type": "application/json",
    }
    index = index.split("/")[0].lower()
    data_as_str = ""
    for candle in candles:
        data_as_str += json.dumps({"index": {"_index": index}}) + "\n"
        data_as_str += json.dumps(candle) + "\n"

    headers = {"Content-Type": "application/x-ndjson"}

    response = requests.post(
        "http://localhost:9200/_bulk", headers=headers, data=data_as_str
    )


def to_json(candles):
    data = []
    for ohlcv in candles:
        data.append(
            {
                "Date": datetime.fromtimestamp(ohlcv[0] // 1000).isoformat(),
                "Open": ohlcv[1],
                "High": ohlcv[2],
                "Low": ohlcv[3],
                "Close": ohlcv[4],
                "Volume": ohlcv[5],
            }
        )
    return data


async def fetch_ohlcv(exchange, symbol, timeframe, limit):
    since = exchange.parse8601("2017-08-17T00:00:00Z")
    now = exchange.milliseconds()
    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    all_ohlcv = []
    fetch_since = since
    while fetch_since < now:
        try:
            candles = await exchange.fetch_ohlcv(symbol, timeframe, fetch_since, limit)

            fetch_since = (
                (candles[-1][0] + 1) if len(candles) else (fetch_since + timedelta)
            )
            if len(candles):
                all_ohlcv = all_ohlcv + candles
                if len(all_ohlcv):
                    print(len(all_ohlcv), symbol, "candles")
            candles_json = to_json(candles)
            put_data(candles_json, symbol)
        except Exception as e:
            print(type(e).__name__, str(e))


async def main():
    exchange = ccxt.binance()
    timeframe = "1m"
    limit = 1000
    symbols = [
        "BTC/USDT",
        "ETH/USDT",
        "BNB/USDT",
        "NEAR/USDT",
        "ADA/USDT",
        "LTC/USDT",
        "ALICE/USDT",
        "SOL/USDT",
        "XRP/USDT",
        "DOT/USDT",
        "DOGE/USDT",
        "AVAX/USDT",
        "LUNA/USDT",
        "SHIB/USDT",
        "UNI/USDT",
        "BCH/USDT",
        "VET/USDT",
        "XLM/USDT",
        "LINK/USDT",
        "MATIC/USDT",
        "ATOM/USDT",
    ]
    loops = [fetch_ohlcv(exchange, symbol, timeframe, limit) for symbol in symbols]
    await gather(*loops)
    await exchange.close()


loop = get_event_loop()
loop.run_until_complete(main())
