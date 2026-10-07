from flask import Flask
from threading import Thread
import os, time, requests

app = Flask('')
@app.route('/')
def home(): return "Bot is Live"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"Telegram says: {r.text}")
    except Exception as e:
        print(f"Telegram Error: {e}")

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10)
        return float(r.json()['price'])
    except Exception as e:
        print(f"Price Error: {e}")
        return None

def start_bot():
    print("Bot Started...")
    last_price = None
    while True:
        price = get_price()
        if price is None:
            time.sleep(2)
            continue
        if last_price is None:
            last_price = price
            print(f"First price locked: {price}")
        else:
            diff = price - last_price
            if abs(diff) >= 1.0:
                if diff > 0:
                    msg = f"UP {last_price:.2f} -> {price:.2f} (+{diff:.2f})"
                else:
                    msg = f"DOWN {last_price:.2f} -> {price:.2f} ({diff:.2f})"
                print(msg)
                send_telegram(msg)
            last_price = price
        time.sleep(1)

# দুটোই একসাথে চালু হবে
Thread(target=run_flask).start()
Thread(target=start_bot, daemon=True).start()
