import time, requests
from flask import Flask
import threading
from concurrent.futures import ThreadPoolExecutor

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)
@app.route('/')
def home(): return "UP-DOWN Fast Live"

def send(m):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def fetch(url):
    try: return float(requests.get(url, timeout=3).json().get('price') or requests.get(url, timeout=3).json()['data']['amount'])
    except: return None

def get_price():
    try:
        with ThreadPoolExecutor(max_workers=2) as ex:
            b = ex.submit(lambda: float(requests.get("https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT", timeout=3).json()['price']))
            c = ex.submit(lambda: float(requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=3).json()['data']['amount']))
            bv = b.result(); cv = c.result()
            if bv and cv: return (bv+cv)/2
            return bv or cv
    except: return None

def loop():
    send("✅ *Fast Bot Start - Late Fix*")
    last = get_price()
    while True:
        curr = get_price()
        if not curr or not last: time.sleep(1); continue
        diff = curr-last
        if abs(diff) > 0.5:
            icon = "🟢 UP" if diff>0 else "🔴 DOWN"
            send(f"{icon} `{last:.2f}` -> `{curr:.2f}`")
            last = curr
        time.sleep(2)

threading.Thread(target=loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
