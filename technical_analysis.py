# technical_analysis.py

import requests
import pandas as pd
import numpy as np

def fetch_ohlcv(symbol="BTCUSDT", interval="15m", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    res = requests.get(url, params=params)
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
    # استراتژی ساده: اگر قیمت آخر بیشتر از قیمت باز شدن باشه → سیگنال خرید
    last_candle = df.iloc[-1]
    signal = "🔴 فروش" if last_candle["close"] < last_candle["open"] else "🟢 خرید"

    percent_change = ((last_candle["close"] - last_candle["open"]) / last_candle["open"]) * 100
    return signal, round(percent_change, 2)

if __name__ == "__main__":
    df = fetch_ohlcv("BTCUSDT", "15m")
    signal, change = simple_strategy(df)
    print(f"نتیجه تحلیل: {signal} | تغییرات: {change}%")
