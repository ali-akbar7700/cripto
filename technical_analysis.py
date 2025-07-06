# technical_analysis.py

import requests
import pandas as pd
from config import BINANCE_API_URL

def fetch_ohlcv(symbol="BTCUSDT", interval="30m", limit=100):
    url = f"{BINANCE_API_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise Exception(f"خطا در دریافت داده برای {symbol}")
    raw_data = res.json()

    df = pd.DataFrame(raw_data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    return df

def simple_strategy(df):
    last_candle = df.iloc[-1]
    open_price = last_candle["open"]
    close_price = last_candle["close"]
    signal = "🟢 خرید" if close_price > open_price else "🔴 فروش"
    change = ((close_price - open_price) / open_price) * 100
    return signal, round(change, 2)

def analyze_symbol(symbol):
    try:
        df = fetch_ohlcv(symbol)
        signal, change = simple_strategy(df)
        result = {
            "symbol": symbol,
            "signal": signal,
            "profit_chance": abs(change) if change > 0 else 0,
            "loss_chance": abs(change) if change < 0 else 0,
            "price": df.iloc[-1]["close"]
        }
        return result
    except Exception as e:
        print(f"❌ خطا در تحلیل {symbol}: {e}")
        return None

def get_usdt_pairs():
    url = f"{BINANCE_API_URL}/api/v3/exchangeInfo"
    res = requests.get(url).json()
    pairs = [s["symbol"] for s in res["symbols"] if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"]
    return pairs

def analyze_all():
    results = []
    symbols = get_usdt_pairs()
    for symbol in symbols:
        result = analyze_symbol(symbol)
        if result and result["profit_chance"] >= 1:
            results.append(result)
    return results
