import requests
import time
import json
import websocket
import threading
from flask import Flask
import os

TELEGRAM_TOKEN = "8782432244:AAF4mlrFhI62DqoFv_4QityqX_J5uqIH0hA"
CHAT_ID = "6601590106"

live_price = 0
last_sent_price = 0

app = Flask(__name__)
@app.route('/')
def home():
    return "BC Bot is Live 24h!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def tg_send(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except:
        pass

def on_message(ws, message):
    global live_price
    try:
        data = json.loads(message)
        live_price = float(data['p'])
    except:
        pass

def send_every_5_sec():
    global live_price, last_sent_price
    while True:
        time.sleep(5)
        if live_price == 0:
            continue
        now = time.strftime('%H:%M:%S')
        if last_sent_price == 0:
            msg = f"⚡ BC START {now}\nPrice: {live_price:.2f}"
        elif live_price > last_sent_price:
            msg = f"🟢 5s UP {now}\n{live_price:.2f} 🔼\n👉 BC te UP maro"
        elif live_price < last_sent_price:
            msg = f"🔴 5s DOWN {now}\n{live_price:.2f} 🔽\n👉 BC te DOWN maro"
        else:
            msg = f"⚪ 5s SAME {now}\n{live_price:.2f}"
        print(msg)
        tg_send(msg)
        last_sent_price = live_price

print("BOT STARTED")
tg_send("✅ Bot Chalu Bhai - 5 sec por por signal asbe")

threading.Thread(target=run_server, daemon=True).start()
threading.Thread(target=send_every_5_sec, daemon=True).start()

ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@trade", on_message=on_message)
ws.run_forever()
