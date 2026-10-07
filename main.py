import os
import time
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

last_price = None

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except:
        pass

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        return float(r.json()['price'])
    except:
        return None

while True:
    new_price = get_price()
    if new_price is None:
        time.sleep(0.5)
        continue
    if last_price is None:
        last_price = new_price
        continue

    diff = new_price - last_price

    if abs(diff) >= 0.01:
        if diff > 0:
            msg = f"UP {last_price:.2f} -> {new_price:.2f} Diff {diff:.2f}"
        else:
            msg = f"DOWN {last_price:.2f} -> {new_price:.2f} Diff {diff:.2f}"
        print(msg)
        send_telegram(msg)
    
    last_price = new_price
    time.sleep(0.5)
