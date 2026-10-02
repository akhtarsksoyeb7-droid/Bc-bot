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
    # 3 ta source, ekta fail hole arekta cholbe
    try:
        r = requests.get("https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        return float(r['price'])
    except: pass
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=10).json()
        return float(r['data']['amount'])
    except: pass
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10).json()
        return float(r['bitcoin']['usd'])
    except:
        return None

def loop():
    send("✅ *BC 5s FULL Bot Fixed! Ebar UP/DOWN asbe!*")
    last = None
    while True:
        curr = get_price()
        if curr:
            if last is not None:
                diff = curr - last
                if diff > 0:
                    send(f"🟢 *5s UP* `{time.strftime('%H:%M:%S')}`\n💰 Price: `{curr:.2f}`\n📈 `+{diff:.2f}` up\nOpen `{last:.2f}` -> Close `{curr:.2f}`")
                elif diff < 0:
                    send(f"🔴 *5s DOWN* `{time.strftime('%H:%M:%S')}`\n💰 Price: `{curr:.2f}`\n📉 `{diff:.2f}` down\nOpen `{last:.2f}` -> Close `{curr:.2f}`")
                else:
                    send(f"⚪ DOJI `{curr:.2f}`")
            last = curr
        time.sleep(5)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
