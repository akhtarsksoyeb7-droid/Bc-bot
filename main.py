import time, requests
from flask import Flask
import threading

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Live"

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def get_price():
    try:
        # 2 ta source, ekta fail korle arekta
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", headers={"User-Agent":"Mozilla/5.0"}, timeout=10).json()
        return float(r['price'])
    except:
        try:
            r = requests.get("https://price.binance.com/api/v3/tickerPrice?symbol=BTCUSDT", timeout=10).json()
            return float(r['price'])
        except:
            return None

def loop():
    send("✅ *BC 5s FULL BTC Bot Start!*")
    last = get_price()
    time.sleep(5)
    while True:
        curr = get_price()
        if curr and last:
            diff = curr - last
            if diff > 0:
                send(f"🟢 *5s UP* `{time.strftime('%H:%M:%S')}`\n💰 `{curr:.2f} USDT`\n📈 `+{diff:.2f}` upore\nOpen `{last:.2f}` -> Close `{curr:.2f}`")
            elif diff < 0:
                send(f"🔴 *5s DOWN* `{time.strftime('%H:%M:%S')}`\n💰 `{curr:.2f} USDT`\n📉 `{diff:.2f}` niche\nOpen `{last:.2f}` -> Close `{curr:.2f}`")
            else:
                send(f"⚪ DOJI `{curr:.2f}`")
            last = curr
        time.sleep(5)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
