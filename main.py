import time, requests
from flask import Flask
import threading

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)
@app.route('/')
def home():
    return "BC 5s FULL Price Bot Live"

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        return float(r['price'])
    except:
        return None

def loop():
    send("✅ *BC 5s FULL BTC Price Bot Start!*\nProti 5s e puro dam + koto up/down bolbe!")
    last = None
    while True:
        price = get_price()
        if price:
            if last is not None:
                diff = price - last
                if diff > 0:
                    send(f"🟢 *5s UP* `{time.strftime('%H:%M:%S')}`\n💰 Price: `{price:.2f} USDT`\n📈 `+{diff:.2f}` upore gelo\n🔓 Open: `{last:.2f}`\n🔒 Close: `{price:.2f}`")
                elif diff < 0:
                    send(f"🔴 *5s DOWN* `{time.strftime('%H:%M:%S')}`\n💰 Price: `{price:.2f} USDT`\n📉 `{diff:.2f}` niche elo\n🔓 Open: `{last:.2f}`\n🔒 Close: `{price:.2f}`")
                else:
                    send(f"⚪ *DOJI* `{price:.2f}` - `{time.strftime('%H:%M:%S')}`")
            last = price
        time.sleep(5)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
