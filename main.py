import time, requests
from flask import Flask
import threading
from datetime import datetime

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)
@app.route('/')
def home(): return "UP-DOWN Bot Live"

def send(m):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# --- তোমার নতুন ভালো get_price() টা ---
def get_price():
    try:
        b = float(requests.get("https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()['price'])
        c = float(requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=5).json()['data']['amount'])
        avg = (b + c) / 2
        return avg
    except:
        return None

def loop():
    send("✅ *UP-DOWN Bot Start with Avg Price*\nEbar BC Game er sathe dam milbe")
    last_price = get_price()
    
    while True:
        curr = get_price()
        if not curr or not last_price:
            time.sleep(2)
            continue
            
        diff = curr - last_price
        
        if diff > 0.5: # 0.5$ er beshi barle UP
            send(f"🟢 *UP* `{last_price:.2f}` -> `{curr:.2f}` `+{diff:.2f}`")
            last_price = curr
        elif diff < -0.5: # 0.5$ er beshi komle DOWN
            send(f"🔴 *DOWN* `{last_price:.2f}` -> `{curr:.2f}` `{diff:.2f}`")
            last_price = curr
            
        time.sleep(3) # 3 sec por por check

threading.Thread(target=loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
