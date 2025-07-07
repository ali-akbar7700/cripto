import os

BINANCE_API_URL = "https://api.binance.com"
BOT_TOKEN = os.getenv("BOT_TOKEN")
GPT_API_KEY = os.getenv("GPT_API_KEY")
DOLLAR_RATE = int(os.getenv("DOLLAR_RATE", "91600"))
