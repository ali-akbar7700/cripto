import requests

API_TOKEN = "7701492103:AAHzyTt77VQEhTUfBnsEl7qGkzFI5KfYUiQ"

response = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getMe")
print(response.status_code)
print(response.json())
