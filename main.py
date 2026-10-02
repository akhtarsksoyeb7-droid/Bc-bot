import time, requests
from flask import Flask
import threading

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)
@app.route('/')
def home():
    return "BC Game Direct Bot Running"

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def bc_game_price():
    # BC Game crash er price asole BTC er price er upor base kore, but amra choto format e nebo
    try:
        # BC Game er moto choto price - last 4 digit niye BC style banabo
        data = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        full = float(data['price'])  # 115234.56
        # BC Game e je 5s er chart dekhay ota last er choto movement
        small = full % 100  # 34.56 er moto choto korbe, hajar thakbe na
        return small, full
    except:
        return None, None

def loop():
    send("✅ *BC Game Direct Bot Connect Holo!*\nEbar BC Game er moto choto 5s candle asbe, hajar thakbe na!")
    last_small = None
    last_full = None
    
    while True:
        try:
            small, full = bc_game_price()
            if small is None:
                time.sleep(5)
                continue
            
            if last_small is not None:
                if small > last_small:
                    send(f"🟢 *5s UP* `{time.strftime('%H:%M:%S')}`\n🔓 Open: `{last_small:.2f}`\n🔒 Close: `{small:.2f}`\n💹 Full BTC: `{full:.2f}`\n👉 BC Game e *UP* maro!")
                elif small < last_small:
                    send(f"🔴 *5s DOWN* `{time.strftime('%H:%M:%S')}`\n🔓 Open: `{last_small:.2f}`\n🔒 Close: `{small:.2f}`\n💹 Full BTC: `{full:.2f}`\n👉 BC Game e *DOWN* maro!")
                else:
                    send(f"⚪ *DOJI* `{small:.2f}` - {time.strftime('%H:%M:%S')}")
            
            last_small = small
            last_full = full
            
        except Exception as e:
            print(e)
        time.sleep(5)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
