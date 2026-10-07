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
        # BCC price - you can change symbol to BTCUSDT if your game follows BTC
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        data = requests.get(url, timeout=5).json()
        return float(data['price'])
    except:
        return None

def bot_loop():
    print("BCC BOT STARTED - 15 sec game")
    send_telegram("BCC Bot Started - 15 sec game tracking ON")
    
    while True:
        # 10 sec betting time start
        price_start = get_price()
        if price_start is None:
            time.sleep(1)
            continue
        
        print(f"BETTING START: {price_start:.2f}")
        time.sleep(10)  # 10 sec betting window

        # After 10 sec, check price for result
        price_end = get_price()
        if price_end is None:
            time.sleep(5)
            continue

        diff = price_end - price_start
        
        if diff > 0:
            result = f"RESULT: UP Green\n{price_start:.2f} -> {price_end:.2f} (+{diff:.2f})"
        elif diff < 0:
            result = f"RESULT: DOWN Red\n{price_start:.2f} -> {price_end:.2f} ({diff:.2f})"
        else:
            result = f"RESULT: SAME\n{price_start:.2f} -> {price_end:.2f}"

        print(result)
        send_telegram(result)
        
        time.sleep(5)  # 5 sec result show time

Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
