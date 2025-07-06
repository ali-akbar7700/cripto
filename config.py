# config.py
BINANCE_API_URL = "https://api.binance.com"
import os

BOT_TOKEN = os.getenv("7701492103:AAHzyTt77VQEhTUfBnsEl7qGkzFI5KfYUiQ")
GPT_API_KEY = os.getenv("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")
DOLLAR_RATE = int(os.getenv("DOLLAR_RATE", 91600))  # اگر نبود 60000 استفاده می‌کنه
