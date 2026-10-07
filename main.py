from flask import Flask
from threading import Thread
import os, time, requests

# 1. Keep Render Alive
app = Flask('')
@app.route('/')
def home(): 
    return "Bot is Live"
def run(): 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive(): 
    Thread(target=run).start()
keep_alive()

# 2. Bot Code
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"  # <-- এখানে তোমার CHAT_ID বসাও

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

def start_bot():
    global last_price
    while True:
        new_price = get_price()
        if new_price is None:
            time.sleep(0.5)
            continue
        if last_price is None:
            last_price = new_price
        else:
            diff = new_price - last_price
            if abs(diff) >= 0.01:
                if diff > 0:
                    msg = f"🟢 UP\n{last_price:.2f} -> {new_price:.2f}\nDiff: +{diff:.2f}"
                else:
                    msg = f"🔴 DOWN\n{last_price:.2f} -> {new_price:.2f}\nDiff: {diff:.2f}"
                print(msg)
                send_telegram(msg)
        last_price = new_price
        time.sleep(0.5)

Thread(target=start_bot).start()
