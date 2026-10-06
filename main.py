import time, requests, os, threading
from flask import Flask
from collections import deque

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "6601590106"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Running"
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

prices = deque(maxlen=15)

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=3)
        return float(r.json()['price'])
    except:
        return None

def send(t):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": t}, timeout=5)
    except:
        pass

def bot_loop():
    send("30s BC Filter Bot Started")
    while True:
        p = get_price()
        if p:
            prices.append(p)

        if len(prices) >= 10:
            diff = prices[-1] - prices[0]
            # Strong move filter - only big move
            if diff > 6:
                send(f"UP {diff:.2f}")
                time.sleep(20)
                prices.clear()
                continue
            elif diff < -6:
                send(f"DOWN {diff:.2f}")
                time.sleep(20)
                prices.clear()
                continue
            # else SKIP - send only 1 time in 3 rounds to avoid spam
            else:
                if len(prices) % 3 == 0:
                    send(f"SKIP {diff:.2f}")

        time.sleep(5)

threading.Thread(target=run_flask, daemon=True).start()
bot_loop()
