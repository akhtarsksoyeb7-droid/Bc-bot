from flask import Flask
from threading import Thread
import os
import time
import requests

app = Flask('')

@app.route('/')
def home():
    return "BCC Game Bot Live"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"TELEGRAM: {r.text}")
    except Exception as e:
        print(f"Telegram Error: {e}")

def get_price():
    try:
        # Using Coingecko - more stable than Binance on Render
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        data = requests.get(url, timeout=10).json()
        return float(data['bitcoin']['usd'])
    except Exception as e:
        print(f"Price fetch error: {e}")
        return None

def bot_loop():
    print("BCC 15 SEC BOT STARTED")
    send_telegram("BCC Bot Started - 15 sec game tracking ON")
    
    while True:
        try:
            price_start = get_price()
            if price_start is None:
                send_telegram("Price fetch failed, retrying in 5 sec...")
                time.sleep(5)
                continue

            print(f"BETTING OPEN: {price_start}")
            time.sleep(10)

            price_end = get_price()
            if price_end is None:
                price_end = price_start

            diff = price_end - price_start

            if diff > 0:
                result = f"UP GREEN ⬆️\n{price_start:.2f} -> {price_end:.2f} (+{diff:.2f})"
            elif diff < 0:
                result = f"DOWN RED ⬇️\n{price_start:.2f} -> {price_end:.2f} ({diff:.2f})"
            else:
                result = f"SAME ⚪\n{price_start:.2f} -> {price_end:.2f}"

            print(result)
            send_telegram(result)
            time.sleep(5)

        except Exception as e:
            print(f"Loop crash: {e}")
            time.sleep(5)

Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
